# VAS

__Virtual Addressd Space__
- When a program runs, it doesn’t directly access `physical memory (RAM)`.
- The operating system and hardware (via the Memory Management Unit, MMU) give the program the illusion that it has its own large, private memory area.
- This illusion called the `Virtual Address Space`.
    - `Virtual address`: the address your program thinks it is using.
    - `Physical address`: the actual location in RAM.
- The OS + MMU translate virtual addresses into physical addresses using a structure called a page table.
    - Virtual Address Space = the set of all possible memory addresses a process can use.

__Simple Example for 32 bit process__
- 32-bit addresses → each address is 4 bytes → maximum addressable memory = 2³² bytes = 4 GB virtual address space.
- Even if the computer only has 2 GB of RAM, the program still thinks it has 4 GB.

__Layout__
```text
+-------------------------+  High addresses
| Kernel space            |  (protected, only OS can access)
+-------------------------+
| Stack                   |  (grows downward)
|                         |
|                         |
| Heap (malloc, new)      |  (grows upward)
+-------------------------+
| BSS (uninitialized data)|
| Data (global variables) |
+-------------------------+
| Text (code, read-only)  |
+-------------------------+  Low addresses

Text segment → compiled instructions (code).

Data segment → global/static variables initialized with values.

BSS segment → uninitialized globals (set to 0 by default).

Heap → dynamic memory (malloc/new).

Stack → function calls, local variables.
```

__Code Explaination__

```c
#include <stdio.h>
#include <stdlib.h>

int global_var = 42;        // Data segment
int uninit_var;             // BSS segment

int main() {
    int local_var = 10;     // Stack
    int *heap_var = malloc(sizeof(int)); // Heap
    *heap_var = 99;

    printf("Code addr:  %p\n", main);          // Text segment
    printf("Global addr: %p\n", &global_var);  // Data segment
    printf("Uninit addr: %p\n", &uninit_var);  // BSS
    printf("Local addr:  %p\n", &local_var);   // Stack
    printf("Heap addr:   %p\n", heap_var);     // Heap

    free(heap_var);
    return 0;
}
```
What happend:
- `main` (the function) lives in the text/code segment.
- `global_var` lives in data.
- `uninit_var` lives in BSS.
- `local_var` goes to the stack.
- `heap_var` points to memory in the heap.


## Virtual Address Space layout of a Linux process
![img](./img/Screenshot%202025-09-15%20153803.png)

__Top (High Address)__
- ENV | ARGS
    - This is ehre the environment variables and command-line argumments are placed when the process starts
    - Example: If you run `./a out hello world`, `"hello world"` get starts here
- Stack
    - Grows downward (from high address to lower address)
    - Stores function calles, local variables, return addresses, saved registers
    - Each thread has its own stack

__MMAP region (Memory-mapped files / shared libraries)__
- Used by
    - `mmap()` system call
    - `shared libraries` (dynamic `.so` files)
    - `anonymous mapping` (for large memory allocations like `malloc` and exceed `brk`-heap)
- Grows downward

__Dynanmic Libiaries(DYN - ELF)__
- These are the shared objects (.so) dynamically loaded by the program.
- Example: when you use printf(), it comes from libc.so.

__Heap__
- Grows upward.
- Allocated with `malloc()`,` calloc()`, `new` in C++.
    - `brk()` system call → moves the "program break".
    - `mmap()` when allocation is large.

__Thread Stack__
- Each thread gets its own stack separate from the main thread
- Typically allocated inside the mmap region

__BSS (Block Started by Symbol)__
- For uninitialized global and static variables

__Data segment__
- For initialized global/static variables.

__Text / Code segment (EXEC ELF)__
- Lowest region (near address 0).
- Contains compiled machine code from the executable (ELF file).
- Usually read-only and often marked executable.

__Difference between Heap and mmap__
- Heap
    - Tradtional area of memory used by malloc()/new for dynamic allocation
    - Implemented using brk/sbrk system calls, wihch move the "program break" (the end of the data segment) up or down
    - Grows upward in virtual memory
- mmap region
    - A more general mechanism for mapping memory into a process's address space
    - Can map files (e.g. shared libraries, memory-mapped I/O) or annomymous pages (used for memory allocations)
    - Grows downward from high address
- When malloc uses Heap vs. mmap?
    - for small/medium adllocations: malloc ususally takes memory from the heap(via `sbrk`)
    - for large allocation (typlically > 128KB)
        - mmap lets the kernal give you memory aligned to a page boundary
        - it can easily be released back to the OS with `munmap()`
        - avoids fragmenting the heap
- Example:
    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int main() {
        // Small allocation -> likely from heap (brk)
        char *p1 = malloc(1000);

        // Large allocation -> likely from mmap
        char *p2 = malloc(200000);

        strcpy(p1, "heap allocation");
        strcpy(p2, "mmap allocation");

        printf("%s at %p\n", p1, p1);
        printf("%s at %p\n", p2, p2);

        free(p1);
        free(p2);
        return 0;
    }
    ```

__Waht is shared libraries?__
- A shared library is a collection of compiled code (functions, classes, variables) stored in a file that can be loaded into memory at runtime and used by multiple programs.
- In Linux/Unix, these files usually end with .so (stands for Shared Object).
- Example: Imagine you write a program that uses `printf()`.
    - That function lives in __glibc__, the GNU C Library.
    - On Linux, glibc is usually a shared library like `/lib/x86_64-linux-gnu/libc.so.6`.
    - Your program’s executable doesn’t carry the machine code for printf — it just says “I need printf from `libc.so`”.
    - At runtime, the __dynamic linker__ (`ld.so`) finds and maps libc.so into memory.

## Process vs. Thread

__Overview__
- Process = a running program with its own virtual address space.
- Thread = a lightweight unit of execution inside a process, sharing the process’s address space.
- Think:
    - Process = the container (the house).
    - Thread = the workers inside the house, all sharing the same kitchen, living room, etc.

__What they share and don't share__
- Process has
    - Its own Virtual Address Space (VAS)
    - Its own heap, stack, globals, code
    - Its own file descriptors (sometimes shared via fork+exec but generally separate)
    - Its own PCB (Process Control Block) in OS
    - Processes are isolated → one can’t easily corrupt another’s memory.
- Threads (inside one process)
    - Thread share with (things belong to process):
        - Virtual address space (heap, globals, code segment)
        - File descriptors (open files, sockets)
    - Each thread has its own:
        - Stack (local variables, function calls)
        - Thread Control Block (TCB)
        - Registers / program counter
    - Threads are lightweight → switching between them is faster than between processes.