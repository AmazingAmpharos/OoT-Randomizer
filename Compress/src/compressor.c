#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include "bSwap.h"
#include "yaz0.c"
#include "crc.c"

#ifdef _WIN32
#include <Windows.h>
#endif

#define UINTSIZE 0x1000000
#define COMPSIZE 0x2000000
#define DCMPSIZE 0x4000000

/* Structs */
typedef struct
{
    uint32_t startV;
    uint32_t   endV;
    uint32_t startP;
    uint32_t   endP;
}
table_t;

typedef struct
{
    table_t table;
    uint8_t* data;
    uint8_t  comp;
    uint32_t size;
}
output_t;

typedef struct
{
    uint32_t fileCount;
    uint32_t*  refSize;
    uint32_t*  srcSize;
    uint8_t**      ref;
    uint8_t**      src;
}
archive_t;

/* Functions */
uint32_t findTable(uint8_t*);
void     getTableEnt(table_t*, uint32_t*, uint32_t);
void*    threadFunc(void*);
void     errorCheck(int, char**);
void     makeArchive();
int32_t  getNumCores();
int32_t  getNext();

/* Globals */
char* name;
uint8_t* inROM;
uint8_t* outROM;
uint8_t* refTab;
pthread_mutex_t filelock;
pthread_mutex_t countlock;
int32_t numFiles, nextFile, arcCount;
int32_t junk;
uint32_t* fileTab;
archive_t* archive;
output_t* out;

int main(int argc, char** argv)
{
    FILE* file;
    int32_t tabStart, tabSize, tabCount;
    volatile int32_t prev; //prevComp;
    int32_t i, j, size, numCores, tempSize;
    pthread_t* threads;
    table_t tab;

    errorCheck(argc, argv);
    printf("Zelda64 Compressor, Version 2\n");
    fflush(stdout);

    /* Open input, read into inROM */
    file = fopen(argv[1], "rb");
    inROM = calloc(DCMPSIZE, sizeof(uint8_t));
    junk = fread(inROM, DCMPSIZE, 1, file);
    fclose(file);

    /* Read archive if it exists*/
    file = fopen("ARCHIVE.bin", "rb");
    if(file != NULL)
    {
        /* Get number of files */
        printf("Loading Archive.\n");
        fflush(stdout);
        archive = malloc(sizeof(archive_t));
        junk = fread(&(archive->fileCount), sizeof(uint32_t), 1, file);
        
        /* Allocate space for files and sizes */
        archive->refSize = malloc(sizeof(uint32_t) * archive->fileCount);
        archive->srcSize = malloc(sizeof(uint32_t) * archive->fileCount);
        archive->ref = malloc(sizeof(uint8_t*) * archive->fileCount);
        archive->src = malloc(sizeof(uint8_t*) * archive->fileCount);

        /* Read in file size and then file data */
        for(i = 0; i < archive->fileCount; i++)
        {
            /* Decompressed "Reference" file */
            junk = fread(&tempSize, sizeof(uint32_t), 1, file);
            archive->ref[i] = malloc(tempSize);
            archive->refSize[i] = tempSize;
            junk = fread(archive->ref[i], 1, tempSize, file);

            /* Compressed "Source" file */
            junk = fread(&tempSize, sizeof(uint32_t), 1, file);
            archive->src[i] = malloc(tempSize);
            archive->srcSize[i] = tempSize;
            junk = fread(archive->src[i], 1, tempSize, file);
        }
        fclose(file);
    }
    else
    {
        printf("No archive found, this could take a while.\n");
        fflush(stdout);
        archive = NULL;
    }

    /* Find the file table and relevant info */
    tabStart = findTable(inROM);
    fileTab = (uint32_t*)(inROM + tabStart);
    getTableEnt(&tab, fileTab, 2);
    tabSize = tab.endV - tab.startV;
    tabCount = tabSize / 16;

    /* Allocate space for the exclusion list */
    /* Default to 1 (compress), set exclusions to 0 */
    file = fopen("dmaTable.dat", "r");
    size = tabCount - 1;
    refTab = malloc(sizeof(uint8_t) * size);
    memset(refTab, 1, size);

    /* The first 3 files are never compressed */
    /* They should never be given to the compression function anyway though */
    refTab[0] = refTab[1] = refTab[2] = 0;
    
    /* Read in the rest of the exclusion list */
    for(i = 0; fscanf(file, "%d", &j) == 1; i++)
    {
        /* Bounds check */
        if(j > size)
        {
            fprintf(stderr, "Error: Entry %d in dmaTable.dat is out of bounds\n", i);
            exit(1);
        }

        /* If j was negative, the file shouldn't exist */
        /* Otherwise, set file to not compress */
        if(j < 0)
            refTab[(j * -1)] = 2;
        else
            refTab[j] = 0;
    }
    fclose(file);

    /* Initialise some stuff */
    out = malloc(sizeof(output_t) * tabCount);
    pthread_mutex_init(&filelock, NULL);
    pthread_mutex_init(&countlock, NULL);
    numFiles = tabCount;
    nextFile = 3;
    arcCount = 0;

    /* Get CPU core count */
    numCores = getNumCores();
    threads = malloc(sizeof(pthread_t) * numCores);
    printf("Detected %d cores.\n", (numCores));
    printf("Starting compression.\n");
    fflush(stdout);

    /* Create all the threads */
    for(i = 0; i < numCores; i++)
        pthread_create(&threads[i], NULL, threadFunc, NULL);

    /* Wait for all of the threads to finish */
    for(i = 0; i < numCores; i++)
        pthread_join(threads[i], NULL);

    /* Setup for copying to outROM */
    printf("\nFiles compressed, writing new ROM.\n");
    outROM = calloc(COMPSIZE, sizeof(uint8_t));
    memcpy(outROM, inROM, tabStart + tabSize);
    prev = tabStart + tabSize;
    /* prevComp = refTab[2]; */
    tabStart += 0x20;

    /* Free some stuff */
    pthread_mutex_destroy(&filelock);
    pthread_mutex_destroy(&countlock);
    if(archive != NULL)
    {
        free(archive->ref);
        free(archive->src);
        free(archive->refSize);
        free(archive->srcSize);
        free(archive);
    }
    free(threads);
    free(refTab);

    /* Copy to outROM loop */
    for(i = 3; i < tabCount; i++)
    {
        tab = out[i].table;
        size = out[i].size;
        tabStart += 0x10;

        /* Finish table and copy to outROM */
        if(tab.startV != tab.endV)
        {
            tab.startP = prev;
            if(out[i].comp == 1)
                tab.endP = tab.startP + size;
            else if(out[i].comp == 2)
                tab.startP = tab.endP = 0xFFFFFFFF;

            if(tab.endP != -1 && tab.endP > COMPSIZE)
            {
                fprintf(stderr, "Warning: File %d has gone out of bounds\n", i);
                fprintf(stderr, "         tab.startV = %8d | 0x%08x\n", tab.startV, tab.startV);
                fprintf(stderr, "         tab.endV   = %8d | 0x%08x\n", tab.endV, tab.endV);
                fprintf(stderr, "         tab.startP = %8d | 0x%08x\n", tab.startP, tab.startP);
                fprintf(stderr, "         tab.endP   = %8d | 0x%08x\n", tab.endP, tab.endP);
                fprintf(stderr, "         size       = %8d | 0x%08x\n", size, size);
            }

            /* If the file existed, write it */
            if(tab.startP != 0xFFFFFFFF)
                memcpy(outROM + tab.startP, out[i].data, size);
            
            /* Write the table entry */
            tab.startV = bSwap_32(tab.startV);
			tab.endV   = bSwap_32(tab.endV);
			tab.startP = bSwap_32(tab.startP);
			tab.endP   = bSwap_32(tab.endP);
            memcpy(outROM + tabStart, &tab, sizeof(table_t));
        }

        
        prev += size;
        /* prevComp = out[i].comp; */
        
        if(out[i].data != NULL)
            free(out[i].data);
    }
    free(out);

    /* Fix the CRC before writing the ROM */
    fix_crc(outROM);
    
    /* Make and fill the output ROM */
    file = fopen(name, "wb");
    fwrite(outROM, COMPSIZE, 1, file);
    fclose(file);

    /* Make the archive if needed */
    if(archive == NULL)
    {
        printf("Creating archive.\n");
        makeArchive(argv[1], name);
    }

    printf("Compression complete.\n");
    if(argc != 3)
        free(name);
    free(inROM);
    free(outROM);
    return(0);
}

uint32_t findTable(uint8_t* argROM)
{
    uint32_t i;
    uint32_t* tempROM;

    tempROM = (uint32_t*)argROM;

    /* Start at the end of the makerom (0x10600000) */
    /* Look for dma entry for the makeom */
    /* Should work for all Zelda64 titles */
    for(i = 1048; i+4 < UINTSIZE; i += 4)
    {
        if(tempROM[i] == 0x00000000)
            if(tempROM[i+1] == 0x60100000)
                return(i * 4);
    }

    fprintf(stderr, "Error: Couldn't find dma table in ROM!\n");
    exit(1);
}

void getTableEnt(table_t* tab, uint32_t* files, uint32_t i)
{
	tab->startV = bSwap_32(files[i*4]);
	tab->endV   = bSwap_32(files[(i*4)+1]);
	tab->startP = bSwap_32(files[(i*4)+2]);
	tab->endP   = bSwap_32(files[(i*4)+3]);
}

void* threadFunc(void* null)
{
    uint8_t* src;
    uint8_t* dst;
    table_t    t;
    int32_t i, nextArchive, size, srcSize;

    while((i = getNext()) != -1)
    {
        /* Setup the src */
        getTableEnt(&(t), fileTab, i);
        srcSize = t.endV - t.startV;
        src = inROM + t.startV;

        /* If refTab is 1, compress */
        /* If refTab is 2, file shouldn't exist */
        /* Otherwise, just copy src into out */
        if(refTab[i] == 1)
        {
            pthread_mutex_lock(&countlock);
            nextArchive = arcCount++;
            pthread_mutex_unlock(&countlock);

            /* If uncompressed is the same as archive, just copy/paste the compressed */
            /* Otherwise, compress it manually */
            if((archive != NULL) && (memcmp(src, archive->ref[nextArchive], archive->refSize[nextArchive]) == 0))
            {
                out[i].comp = 1;
                size = archive->srcSize[nextArchive];
                out[i].data = malloc(size);
                memcpy(out[i].data, archive->src[nextArchive], size);
            }
            else
            {
                size = srcSize + 0x250;
                dst = calloc(size, sizeof(uint8_t));
                yaz0_encode(src, srcSize, dst, &(size));
                out[i].comp = 1;
                out[i].data = malloc(size);
                memcpy(out[i].data, dst, size);
            }
            
            if(archive != NULL)
            {
                free(archive->ref[nextArchive]);
                free(archive->src[nextArchive]);
            }
        }
        else if(refTab[i] == 2)
        {
            out[i].comp = 2;
            size = 0;
            out[i].data = NULL;
        }
        else
        {
            out[i].comp = 0;
            size = srcSize;
            out[i].data = malloc(size);
            memcpy(out[i].data, src, size);
        }

        /* Set up the table entry and size */
        out[i].table = t;
        out[i].size = size;
    }

    return(NULL);
}

void makeArchive()
{
    table_t tab;
    uint32_t tabSize, tabCount, tabStart;
    uint32_t fileSize, fileCount, i;
    FILE* file;

    /* Find DMAtable info */
    tabStart = findTable(outROM);
    fileTab = (uint32_t*)(outROM + tabStart);
    getTableEnt(&tab, fileTab, 2);
    tabSize = tab.endV - tab.startV;
    tabCount = tabSize / 16;
    fileCount = 0;

    /* Find the number of compressed files in the ROM */
    /* Ignore first 3 files, as they're never compressed */
    for(i = 3; i < tabCount; i++)
    {
        getTableEnt(&tab, fileTab, i);

        if(tab.endP != 0 && tab.endP != 0xFFFFFFFF)
            fileCount++;
    }

    /* Open output file */
    file = fopen("ARCHIVE.bin", "wb");
    if(file == NULL)
    {
        perror("ARCHIVE.bin");
        fprintf(stderr, "Error: Could not create archive\n");
        return;
    }

    /* Write the archive data */
    fwrite(&fileCount, sizeof(uint32_t), 1, file);
    
    /* Write the fileSize and data for each ref & src */
    for(i = 3; i < tabCount; i++)
    {
        getTableEnt(&tab, fileTab, i);

        if(tab.endP != 0 && tab.endP != 0xFFFFFFFF)
        {
            /* Write the size and data for the decompressed portion */
            fileSize = tab.endV - tab.startV;
            fwrite(&fileSize, sizeof(uint32_t), 1, file);
            fwrite(inROM + tab.startV, 1, fileSize, file);

            /* Write the size and data for the compressed portion */
            fileSize = tab.endP - tab.startP;
            fwrite(&fileSize, sizeof(uint32_t), 1, file);
            fwrite((outROM + tab.startP), 1, fileSize, file);
        }
    }

    fclose(file);
}

int32_t getNumCores()
{
    /* Windows */
    #ifdef _WIN32

        SYSTEM_INFO info;
        GetSystemInfo(&info);
        return(info.dwNumberOfProcessors);

    /* Mac */
    #elif MACOS

        int nm[2];
        size_t len;
        uint32_t count;

        len = 4;
        nm[0] = CTL_HW;
        nm[1] = HW_AVAILCPU;
        sysctl(nm, 2, &count, &len, NULL, 0);

        if (count < 1)
        {
            nm[1] = HW_NCPU;
            sysctl(nm, 2, &count, &len, NULL, 0);
            if (count < 1)
                count = 1;
        }
        return(count);

    /* Linux */
    #else

        return(sysconf(_SC_NPROCESSORS_ONLN));

    #endif
}

int32_t getNext()
{
    int32_t file, temp;

    pthread_mutex_lock(&filelock);
    
    file = nextFile++;

    /* Progress tracker */
    if (file < numFiles)
    {
	temp = numFiles - (file + 1);
        printf("%d files remaining\n", temp);
        fflush(stdout);
    }
    else
    {
        file = -1;
    }
    
    pthread_mutex_unlock(&filelock);

    return(file);
}

void errorCheck(int argc, char** argv)
{
    int i;
    FILE* file;

    /* Check for arguments */
    if(argc < 2 || argc > 3)
    {
        fprintf(stderr, "Usage: %s [Input ROM] <Output ROM>\n", argv[0]);
        exit(1);
    }

    /* Check that input ROM exists */
    file = fopen(argv[1], "rb");
    if(file == NULL)
    {
        perror(argv[1]);
        exit(1);
    }

    /* Check that input ROM is correct size */
    fseek(file, 0, SEEK_END);
    i = ftell(file);
    fclose(file);
    if(i != DCMPSIZE)
    {
        fprintf(stderr, "Error: Invalid input ROM size!\n");
        exit(1);
    }

    /* Check that dmaTable.dat exists */
    file = fopen("dmaTable.dat", "r");
    if(file == NULL)
    {
        perror("dmaTable.dat");
        fprintf(stderr, "Please make a dmaTable.dat file first\n");
        exit(1);
    }

    /* Check that output ROM is writeable */
    /* Create output filename if needed */
    if(argc == 2)
    {
        i = strlen(argv[1]) + 6;
        name = malloc(i);
        strcpy(name, argv[1]);
        for(; i >= 0; i--)
        {
            if(name[i] == '.')
            {
                name[i] = '\0';
                break;
            }
        }
        strcat(name, "-comp.z64");
        file = fopen(name, "wb");
        if(file == NULL)
        {
            perror(name);
            free(name);
            exit(1);
        }
        fclose(file);
    }
    else
    {
        file = fopen(argv[2], "wb");
        if(file == NULL)
        {
            perror(argv[2]);
            exit(1);
        }
        fclose(file);
        name = argv[2];
    }
}
