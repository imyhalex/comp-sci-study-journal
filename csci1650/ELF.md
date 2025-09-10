# ELF
- Executable and Linkable Format.
- It’s the standard file format for executables, object code, shared libraries, and core dumps on Unix-like systems (Linux, BSD, Solaris, etc.).

    ```bash
    gcc hello.c -o hello

    The output binary `hello` is stored in ELF format
    ```

Think of ELF as a container/blueprint that tells the operating system:
- What kind of file this is (executable, library, or object file).
- Where the program should start execution.
- Where the code, data, and dynamic linking info live in the file.

__ELF File type__: An ELF file can be:
- Relocatable (.o): object files produced by the compiler, not yet linked.
- Executable: runnable programs.
- Shared object (.so): dynamically linked libraries.
- Core dump: snapshot of a crashed process’s memory.

__Structure of an ELF file__: An ELF file is divided into headers + sections/segments.
- ELF Header: at the very beginning, contains metadata:
    - File type (executable, object, etc.)
    - Architecture (x86, ARM, etc.)
    - Entry point (address where execution starts)
- Program headers (segments): tell the OS how to load the program into memory.
    - Code segment, data segment, dynamic linking info.
- Section headers (sections): used mostly at compile/link time.
    - `.text` → machine code
    - `.data` → initialized global variables/data
    - `.bss` → uninitialized globals data
    - `.rodata` → constants/strings
    - `.symtab` → symbol table (functions/variables)
    - `.strtab` → string table (names of symbols)E
- Imagin a Book:
    - Table of contents → ELF header
    - Chapters → sections
    - How to read chapters in order → program headers

__What is Dynamic Linking__
- When you compile a program, you need to connect your code with libraries (like `printf` from the C standard library).
- There are two ways this can happend:
    - Static linking: all library code is copied directly into your executable.
    - Dynamic linking: your program just stores references to external libraries, and the actual library code is loaded at runtime (when the program starts).
- Analogy:
    - Static linking = you copy whole chapters from reference books into your own report. Your report is big, but it’s self-contained.
    - Dynamic linking = you cite references (“see page 25 in libc”), and at runtime the librarian brings you the books. Your report is smaller, but it won’t work without the library.

- Example:
    ```c
    // hello.c
    #include <stdio.h>
    int main() {
        printf("Hello dynamic linking!\n");
        return 0;
    }

    Static Linking:
    gcc hello.c -static -o hello_static
    
    This will do:
    - The entire printf implementation (from glibc) is copied into the binary.
    - ls -lh hello_static → file size is HUGE (~1–2 MB).
    - You can run it even if no libc is installed, because everything is self-contained.

    Dynamic Linking:
    gcc hello.c -o hello_dynamic

    This will do:
    Only a reference to printf is stored in the ELF binary.
    - At runtime, the dynamic linker/loader (ld-linux.so) loads libc.so into memory.
    - ls -lh hello_dynamic → much smaller (~15 KB).
    - But if libc.so is missing, the program won’t run.
    ```