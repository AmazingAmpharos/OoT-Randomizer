To load custom sequences, you need to have a raw N64 sequence file with a `.seq` file extension and a corresponding file with the same name but with a `.meta` file extension. The `.meta` file should be a plaintext file with two lines. The first line is the name of the sequence to be displayed in the cosmetic log, and the second line is the instrument set number, in base 16.

For example, if there is a sequence file `Foo.seq` then you need a meta file `Foo.meta` that could contain
```
Awesome Name
C
```
