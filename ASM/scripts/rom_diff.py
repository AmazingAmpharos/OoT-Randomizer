import json
import sys

def main():
    if len(sys.argv) < 4:
        raise RuntimeError("Usage: python rom_diff.py BASE_FILE COMPARISON_FILE OUTPUT_FILE")

    base_path = sys.argv[1]
    compare_path = sys.argv[2]
    output_path = sys.argv[3]
    create_diff(base_path, compare_path, output_path)
    
def unequal_chunks(file1, file2):
    chunk_size = 2048
    i = 0
    while True:
        chunk1 = file1.read(chunk_size)
        chunk2 = file2.read(chunk_size)
        if not chunk1:
            return
        if chunk1 != chunk2:
            yield (i * chunk_size, chunk1, chunk2)
        i += 1

def create_diff(base_path, compare_path, output_path):
    diffs = []
    with open(base_path, 'rb') as base_f, open(compare_path, 'rb') as comp_f:
        for (i, base_c, comp_c) in unequal_chunks(base_f, comp_f):
            for j in range(len(base_c)):
                if comp_c[j] != base_c[j]:
                    diffs.append((i + j, comp_c[j]))

    with open(output_path, 'w') as out_f:
        for (i, b) in diffs:
            out_f.write('{0:x},{1:x}\n'.format(i, b))

if __name__ == '__main__':
    main()