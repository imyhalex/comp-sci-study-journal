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

## VAS & RAM
![img](./img/Screenshot%202025-09-17%20at%2015.08.03.png)
__Explaination:__
- Two processes: P1 and P2
- Each has its own VAS (on the left, 4 GB split into 3 GB user + 1 GB kernel).
- The physical RAM is in the middle.
- Colored arrows show that:
    - Different virtual pages from P1 and P2 can map to different physical frames.
    - They can also map to the same physical frame (shared memory).
- Key Ideas:
    - Each process thinks it has a private 0x0 → 4 GB address range.
    - But in reality, the OS translates those virtual pages to actual physical frames in RAM.
    - That’s why virtual addresses can overlap across processes (both P1 and P2 can have a page at 0x0), but they end up at different places in RAM.

![img](./img/Screenshot%202025-09-17%20at%2015.08.09.png)
__What it adds:__
- Now you’ve drawn page tables at the bottom (yellow boxes).
- Each process has its own page table:
    - P1 Page Table: maps virtual page 0x0 → physical frame 0xB000
    - P2 Page Table: maps virtual page 0x0 → physical frame 0xC000
- CPU uses a Memory Management Unit (MMU) to perform this translation.
- The MMU consults the page table (with help from hardware caches like the TLB) to resolve every memory access.
- Key Ideas:
    - The OS maintains a separate page table per process.
    - On a context switch, the OS updates the CPU’s page table base register (e.g., CR3 on x86).
    - That’s how the CPU knows whether 0x0 means P1’s 0xB000 frame or P2’s 0xC000 frame.



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
- What you labeled as "Heap" above “Thread-Stack” likely refers to mmap-based heap allocations.
- Modern allocators (glibc malloc) don’t only use `brk`; they also allocate large chunks with mmap().
- Grows upward.
- Allocated with `malloc()`,` calloc()`, `new` in C++.
    - `brk()` system call → moves the "program break".
    - `mmap()` when allocation is large.

__BRK(Heap)__
- The classic heap region that starts just above your data/bss.
- Managed by the kernel’s brk()/sbrk() system calls.
- These appear as “anonymous mmap” regions elsewhere in the VAS.
- So:
    - BRK (Heap) = contiguous region grown via `brk`.
    - Heap (mmap) = separate chunks allocated with `mmap`.
- Used by `malloc()` for small/medium allocations.
- Grows upward (toward higher addresses).

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
### 1. **Address Space Range**

* On a **32-bit machine**, the entire VAS is `0x00000000` → `0xffffffff` (4 GB).
* This space is **split between user space and kernel space**.

  * By default (on Linux):

    * **User space**: `0x00000000` → `0xbfffffff` (3 GB)
    * **Kernel space**: `0xc0000000` → `0xffffffff` (1 GB, reserved, not accessible from user processes)

So **user space starts at `0x00000000`**, not at `0xbfffffff`.
The address `0xbfffffff` is actually the **top of user space**, where the **stack grows downward**.

---

### 2. **What the Diagram Shows**

From **top to bottom** (high addresses → low addresses):

* **Environment variables & arguments (ENV | ARGS)**: placed near the very top of user space, just below `0xc0000000`.
* **Stack**: starts near `0xbfffffff` and grows downward.

  * In your diagram, default `ulimit -s` = 8 MB means the stack can extend down from the top.
* **MMAP region**: used for `mmap()` calls, shared libraries, memory-mapped files.
* **Dynamic libraries (ld.so, libc.so, etc.)**: loaded into the mmap area, addresses randomized (ASLR can shift them).
* **Heap**: grows upward, starting after the BSS/data segment of the main program (brk area).
* **Executable segments (ELF)**: at the bottom region (`0x08048000` typically, historically). Contains `.text`, `.data`, `.rodata`, etc.

---

### 3. **Key Point About Your Question**

> *“So what does this 32-bit machine VAS anatomy mean? The user space start from `0xbfffff`?”*

No —

* **User space starts at `0x00000000`**.
* **User space ends at `0xbfffffff`**.
* The **stack starts at the very top (`0xbfffffff`)** and grows downward, which is why many diagrams show it starting “from 0xbfffffff.”

So the confusion is that `0xbfffffff` is not the *start of user space*, but the *end (top) of user space* where the stack begins.

---

**Summary**:
On a 32-bit Linux machine with the 3G/1G split:

* User space = `0x00000000` → `0xbfffffff`
* Kernel space = `0xc0000000` → `0xffffffff`
* The diagram shows how different segments (stack, heap, libraries, code) are arranged within user space.

## 1. Why is each VAS 4 GB on a 32-bit machine?

* A **32-bit CPU** uses 32-bit pointers (virtual addresses).
* That means the maximum number of distinct addresses is:
  [
  2^{32} = 4,294,967,296 \text{ bytes} = 4 \text{ GB}
  ]
* So, the **total virtual address space per process = 4 GB**, regardless of how much physical RAM the machine has.
* Each process gets its **own** 4 GB virtual address space (thanks to page tables and MMU). They are isolated from one another.

---

## 2. Why split 3 GB user / 1 GB kernel?

The kernel must always be accessible in any process context. But we don’t want user processes messing with kernel memory directly.

So the OS designers **divide the 4 GB VAS**:

* **Lower 3 GB (0x00000000 → 0xbfffffff)**

  * Mapped to **user space**.
  * Each process has its own mappings here.

* **Upper 1 GB (0xc0000000 → 0xffffffff)**

  * Mapped to the **kernel’s address space**.
  * This region is **the same in all processes** (so the kernel can run regardless of which process is active).
  * User processes cannot access it (privilege checks prevent that).

This design has some benefits:

* Kernel can be mapped into every process’s VAS → **no need to switch page tables** when entering kernel mode.
* Keeps user and kernel memory separated for protection.

---

## 3. Could we change the split?

Yes — Linux allows different splits:

* **3G/1G (default)**: 3 GB user, 1 GB kernel.
* **2G/2G split**: gives kernel more virtual space, useful for systems with huge kernel memory demands.
* **4G/4G patches** (rare): experimental, kernel and user each get full 4 GB, but very complex.

 **Summary**

* **Each process gets 4 GB VAS** because 32-bit addresses = 4 GB max.
* It’s split (typically 3G/1G) so both user code and kernel can coexist in the same address space.
* Kernel part is shared across all processes and always mapped; user part is private per process.


## 1. Theoretical maximum (64-bit addressing)

* With 64-bit pointers, in theory the CPU could address:
  [
  2^{64} = 16 \text{ exabytes (EB)} = 16,777,216 \text{ TB}
  ]
* That’s way more than any real hardware or OS needs today.


## 2. Practical limits (canonical addresses)

* On **x86-64** (AMD64), current CPUs don’t use the full 64 bits.
* They use **48 bits of virtual addressing** (sometimes 57 bits in newer CPUs).

  * With **48 bits**:
    [
    2^{48} = 256 \text{ TB of virtual address space per process}
    ]
  * With **57 bits** (newer Intel/AMD):
    [
    2^{57} = 128 \text{ PB}
    ]

---

## 3. OS split (Linux/Windows convention)

* Just like 32-bit had **3G user / 1G kernel**, 64-bit has its own split:

  * **Linux x86-64 (48-bit VAS)**:

    * **128 TB user space** (lower half)
    * **128 TB kernel space** (upper half)
  * Each process gets this entire user-space range. Kernel is mapped separately and protected.

---

## 4. Key difference from 32-bit

* On **32-bit**: Each process only got 4 GB VAS. That became a limitation.
* On **64-bit**: Each process gets **128 TB (or more)**, which is effectively unlimited for today’s applications.

So: Not 16 GB. On common 64-bit CPUs today, it’s **128 TB of user-space VAS per process** (with a matching 128 TB kernel space).


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

##  Executable Binary within EXEC (ELF)
![img](./img/Screenshot%202025-09-17%20at%2015.20.22.png)
- The bottom part labeled EXEC (ELF) is the memory region where your executable binary is mapped into the process’s address space.
- The ELF has different sections, and the loader (`ld-linux.so`) maps those into memory at fixed virtual addresses.

__Segments under the EXEC (ELF)__
1. **.text** (Code segment)

   * Contains the program’s **machine code** (compiled instructions).
   * Usually marked **read-only + executable (r-x)**.
   * Example: where your `main()` function lives.

2. **.rodata** (Read-only data)

   * Constants, string literals.
   * Example: `"Hello, world!\n"`.

3. **.data** (Initialized global variables)

   * Global/static variables with initial values.
   * Example:

     ```c
     int g = 42;   // goes into .data
     ```

4. **.bss** (Uninitialized globals)

   * Global/static variables initialized to 0 or left uninitialized.
   * Example:

     ```c
     int counter;  // goes into .bss
     ```
   * BSS does not take up space in the executable file — the loader just reserves zeroed memory.

5. **.interp** (Interpreter)

   * Stores the path to the **dynamic linker/loader** (e.g., `/lib/ld-linux.so.2` or `/lib64/ld-linux-x86-64.so.2`).
   * This tells the kernel: “to run this binary, first load this program (dynamic loader).”

6. **Other ELF sections** (not always visible in runtime maps, but present in the ELF file):

   * `.symtab` (symbol table)
   * `.strtab` (string table)
   * `.debug` (debug info, if compiled with `-g`)
   * These are usually not mapped into memory for runtime execution.


__Address Ranges__

* **EXEC ELF starts \~0x08048000**

  * Typical for 32-bit Linux executables (unless ASLR randomizes it).
* **Ends \~0x0804bfff**

  * Contains text, data, bss, rodata.

__Memory Protection__

Each section has specific permissions:

* `.text` → **r-x** (read, execute)
* `.rodata` → **r--** (read only)
* `.data` and `.bss` → **rw-** (read, write)

- This separation enforces safety: you can’t accidentally overwrite your code or execute data.

__Example (using `readelf`)__

```bash
readelf -S ./a.out
```

You’ll see section headers like:

```
  [13] .text     PROGBITS  08048400  00000400  0000017d  AX  0  0  4
  [14] .rodata   PROGBITS  08048580  00000580  00000034  A   0  0  4
  [15] .data     PROGBITS  08049f00  00001f00  00000010  WA  0  0  4
  [16] .bss      NOBITS    08049f10  00001f10  00000004  WA  0  0  4
  [17] .interp   PROGBITS  08048234  00000234  00000013  A   0  0  1
```

