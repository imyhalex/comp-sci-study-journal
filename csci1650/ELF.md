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

## Compilation Processes

__Compilation = 4 stages → Preprocess → Compile → Assemble → Link.__
- One command from source code to executable: __gcc -o esrv esrv.c__
- Preprocess:
    - Expands `#include`, `#define`, macros, conditional compliation (`#ifdef`)
    - Removes commands
    - Produces a pure C file with everything "inline"
    - Command:
        ```bash
        gcc -E esrv.c -o esrv.i
        ```
- Compilation (`cc1`)
    - Converts preprocessed C into assembly code for your architecture
    - Performs parsing, semantic analysis, optimizations
    - Produces `.s` (assembly file)
    - Command:
        ```bash
        gcc -S esrv.i -o esrv.s
        ```
- Assmemble (`as`)
    - Converts human-readable `.s` into machine code (object file)
    - Produces `.o` (ELF relocateable object file)
    - Contains machine code + relocation info + symbol tables. but not yet linked.
    - Command:
        ```bash
        gcc -c esrv.s -o esrv.o

        # directly from source
        gcc -c esrv.c -o esrv.o
        ```
- Linking (`ld`)
    - Combines multiple `.o` files + libraries into a final executable
    - Resolves symbols references (e.g. you `main` calls `printf`, which lives in libc)
    - Produces and ELF __executable__ (or shared object `.so` if `-shared`)
    - Command:
        ```bash
        gcc esrv.o -o esrv
        ```

## ELF Anatomy with Example[[Link](https://en.wikipedia.org/wiki/Executable_and_Linkable_Formats)]
![img](./img/Screenshot%202025-09-24%20131324.png)

1. ELF Header (the "Identity card")
    - First 64 bytes (ELF64), for ELF32, it is first 52 bytes
    - Magic: `0x7f 45 4c 46` (`\x7fELF`).
    - Specifies:
        - Class (32 vs 64 bit)
        - Endianess (little vs big)
        - ABI
        - Entry point address
        - Locations of __Program Header (Segment Table)__ and __Section Header Table__
    - Command:
        ```bash
        readelf -h esrv
        ```
2. Program Header Table (= Segment Table): Loader's View
    - Tells the __kernal how to map the file into memory__ when you `execve()`
    - Each entry = a segment (continious chunk)
    - Key types:
        - PT_LOAD -> load segment (code, data)
        - PT_DYNAMIC -> Dynamic Linking Info
        - PT_INTERP -> path interperter (like `/lib64/ld-linux-x86-64.so.2`)
        - PT_NOTE -> auxiliary notes
    - Segments are what you seen in `/proc/<pid>/maps`
    - Command:
        ```bash
        readelf -l esrv
        ```
3. Section Header Table (Linker's View)
    - Each section is for linking/debugging, not for runtime execution
    - Examples:
        - `.text` → executable machine code
        - `.rodata` → read-only constants, string literals
        - `.data` → initialized global/static vars
        - `.bss` → uninitialized vars (just space)
        - `.plt` / `.got` → dynamic linking stubs
        - `.symtab` / `.dynsym` → symbol tables
        - `.strtab` → string table (names of symbols)
    - Sections are usually stripped in production binaries
    - Command:
        ```bash
        readelf -S esrv
        ```

4. Symbols (Names -> Addresses)
    - Two main tables:
        - `.symtab` → full symbol table (may be stripped).
        - `dynsym` → symbols needed for dynamic linking.
    - Each symbol entry:
        - Name (index into .strtab)
        - Value (address / offset)
        - Size (bytes)
        - Binding (local/global)
        - Type (func, object)
    - Command:
        ```bash
        readelf -s esrv
        ```

5. Relocations (Glue for linking)
    - When code refers to things whose addresses aren't know until link/load time:
        - `R_X86_64_PC32`, `R_X86_64_GLOB_DAT`, etc.
        - Common in dynamically linked binaries (`printf`, `malloc`).
        - Resolved at runtime via the PLT (Procedure Linkage Table) and GOT (Global Offset Table).
    - Command:
        ```bash
        readelf -r esrv
        ```

6. Dynamic Section (If dynamically linked)
    - Holds runtime loader info:
        - Needed Shared libs (`DT_NEEDED`)
        - Address of symbol hash tables
        - Relocation Tables
        - Init/fini function pointers
    - Command:
        ```bash
        readelf -d esrv
        ```
7. Real Memory Layout (when loaded)
    - Example:
        ```text
        0x400000 ─► [ ELF headers / read-only ]
        0x401000 ─► [ .text   (instructions)  R-X ]
        0x406000 ─► [ .rodata (constants)     R-- ]
        0x407000 ─► [ .data   (initialized)   RW- ]
        0x408000 ─► [ .bss    (zero-fill)     RW- ]
        0x7fff... ─► [ stack ]
        0x5555... ─► [ heap ]
        ```
8. `-e` option in `readelf`
    - Example
        ```bash
        readelf -e esrv
        ```
    - You’ll get in one go:
        - The ELF identity card (architecture, entry point, offsets)
        - The segment table (what kernel maps into memory)
        - The section table (all the named sections like `.text`, `.data`, `.bss`, .`rodata`, `.symtab`, etc.)
    - Useful for _reverse engineering_ when you want a big picture of the file layout.
        - Instead of calling readelf `-h`, then `-l`, then `-S`, you see all three in one output.
        - After that, you can drill down with:
            - `-s` (symbols)
            - `-r` (relocations)
            - `-d` (dynamic section)
            - `-x` (hex dump of a section)