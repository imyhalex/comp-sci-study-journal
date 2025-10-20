# Basics [ELF, VAS, $gdb `info proc mappings`, Stack registers (antanomy and offsets calculations)]

## ELF dump `readelf -e esrv`
```bash
debpool07 ~/l05 $ readelf -e esrv
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Intel 80386
  Version:                           0x1
  Entry point address:               0x8049140
  Start of program headers:          52 (bytes into file)
  Start of section headers:          82380 (bytes into file)
  Flags:                             0x0
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         10
  Size of section headers:           40 (bytes)
  Number of section headers:         36
  Section header string table index: 35

Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            00000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        08048174 000174 000013 00   A  0   0  1
  [ 2] .note.gnu.bu[...] NOTE            08048188 000188 000024 00   A  0   0  4
  [ 3] .note.ABI-tag     NOTE            080481ac 0001ac 000020 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        080481cc 0001cc 000024 04   A  5   0  4
  [ 5] .dynsym           DYNSYM          080481f0 0001f0 000150 10   A  6   1  4
  [ 6] .dynstr           STRTAB          08048340 000340 0000c1 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          08048402 000402 00002a 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         0804842c 00042c 000030 00   A  6   1  4
  [ 9] .rel.dyn          REL             0804845c 00045c 000010 08   A  5   0  4
  [10] .rel.plt          REL             0804846c 00046c 000088 08  AI  5  22  4
  [11] .init             PROGBITS        08049000 001000 000020 00  AX  0   0  4
  [12] .plt              PROGBITS        08049020 001020 000120 04  AX  0   0 16
  [13] .text             PROGBITS        08049140 001140 0004dd 00  AX  0   0 16
  [14] .fini             PROGBITS        08049620 001620 000014 00  AX  0   0  4
  [15] .rodata           PROGBITS        0804a000 002000 00010c 00   A  0   0  4
  [16] .eh_frame_hdr     PROGBITS        0804a10c 00210c 00003c 00   A  0   0  4
  [17] .eh_frame         PROGBITS        0804a148 002148 0000f8 00   A  0   0  4
  [18] .init_array       INIT_ARRAY      0804b240 002240 000004 04  WA  0   0  4
  [19] .fini_array       FINI_ARRAY      0804b244 002244 000004 04  WA  0   0  4
  [20] .dynamic          DYNAMIC         0804b248 002248 0000e8 08  WA  6   0  4
  [21] .got              PROGBITS        0804b330 002330 000004 04  WA  0   0  4
  [22] .got.plt          PROGBITS        0804b334 002334 000050 04  WA  0   0  4
  [23] .data             PROGBITS        0804b384 002384 000008 00  WA  0   0  4
  [24] .bss              NOBITS          0804b38c 00238c 000008 00  WA  0   0  4
  [25] .comment          PROGBITS        00000000 00238c 000027 01  MS  0   0  1
  [26] .debug_aranges    PROGBITS        00000000 0023b3 000020 00      0   0  1
  [27] .debug_info       PROGBITS        00000000 0023d3 000709 00      0   0  1
  [28] .debug_abbrev     PROGBITS        00000000 002adc 0001e8 00      0   0  1
  [29] .debug_line       PROGBITS        00000000 002cc4 0002ff 00      0   0  1
  [30] .debug_str        PROGBITS        00000000 002fc3 00d445 01  MS  0   0  1
  [31] .debug_line_str   PROGBITS        00000000 010408 000454 01  MS  0   0  1
  [32] .debug_macro      PROGBITS        00000000 01085c 0031e3 00      0   0  1
  [33] .symtab           SYMTAB          00000000 013a40 000360 10     34  20  4
  [34] .strtab           STRTAB          00000000 013da0 0002ce 00      0   0  1
  [35] .shstrtab         STRTAB          00000000 01406e 00015e 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  D (mbind), p (processor specific)

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  PHDR           0x000034 0x08048034 0x08048034 0x00140 0x00140 R   0x4
  INTERP         0x000174 0x08048174 0x08048174 0x00013 0x00013 R   0x1
      [Requesting program interpreter: /lib/ld-linux.so.2]
  LOAD           0x000000 0x08048000 0x08048000 0x004f4 0x004f4 R   0x1000
  LOAD           0x001000 0x08049000 0x08049000 0x00634 0x00634 R E 0x1000
  LOAD           0x002000 0x0804a000 0x0804a000 0x00240 0x00240 R   0x1000
  LOAD           0x002240 0x0804b240 0x0804b240 0x0014c 0x00154 RW  0x1000
  DYNAMIC        0x002248 0x0804b248 0x0804b248 0x000e8 0x000e8 RW  0x4
  NOTE           0x000188 0x08048188 0x08048188 0x00044 0x00044 R   0x4
  GNU_EH_FRAME   0x00210c 0x0804a10c 0x0804a10c 0x0003c 0x0003c R   0x4
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x10

 Section to Segment mapping:
  Segment Sections...
   00
   01     .interp
   02     .interp .note.gnu.build-id .note.ABI-tag .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rel.dyn .rel.plt
   03     .init .plt .text .fini
   04     .rodata .eh_frame_hdr .eh_frame
   05     .init_array .fini_array .dynamic .got .got.plt .data .bss
   06     .dynamic
   07     .note.gnu.build-id .note.ABI-tag
   08     .eh_frame_hdr
   09

debpool07 ~/l05 $ ldd ./esrv
        linux-gate.so.1 (0xf7f9d000)
        libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7d2f000)
        /lib/ld-linux.so.2 (0xf7f9f000)
```
1. Quick Metadata (what kind of binary it is)
	- `readelf -h esrv` -> shows `ELF32` and `Type: EXEC`.
		- __Meaning__: 32-bit executable with fixed virtual address (non-PIE). You can trust the addresses in the headers as the addresses the loader will use for this binary itself
	- `Entry point address`: the location of your first instruction
    - Q: Is it a DSO (Dynamic shared object)?
        - No, since `Type: EXEC (Executable file)`
        - If `Type: DYN/ET_DYN`, then yes

2. Which segments are mapped where (the loader's view)
	- `readelf -l esrv` (Program Header)
		- __Why__: Program header (`LOAD` entries) tell you exactly which parts of the file will be mapped into the process virtual memory and __at what virtual addresses__ (the `VirtAddr` column).
	- Example from this output:
		- `LOAD` at `VirtAddr 0x08049000` (R E) — that contains `.text (code)`.
		- `LOAD` at `VirtAddr 0x0804b240` (RW) — data, `.got`, `.data`, `.bss`
			- General Rule of Thumb:
				- Executable (R E) -> contains `.text`, `.plt`, `.init`, `.fini`
				- Writable LOAD (RW) → contains `.data`, `.bss`, `.got`, `.dynamic`
				- Read-only (R only) -> contains `.rodata`, `.eh_frame`
		- `GUN_STACK` with `RWE` -> the binary requests an executatble stack
	- __Bottom line:__ For ET_EXEC (non-PIE) binaries the VirtAddr values are the actual addresses the process will have for those segments when run (unless the kernel remaps for weird reasons). So without running, you already know where `.text`, `.data`, `.got.plt`, `.bss`, etc. will live.

3. Where secionts live inside the mapped segments
	- `readelf -S esrv` (Section Header)
	- __Why:__ Sections (like .text, .rodata, .got.plt) show their addresses (Addr column) and file offsets (Off). Use these to map specific addresses (e.g., .text starts at 0x08049140) to instructions or data.

4. Is this dynamically linked? who is the dynamic loader?
	- Look for a Program Header `INTERP`, it prints: `[Requesting program interpreter: /lib/ld-linux.so.2]`
	- __Meaning:__ Yes - dynamic linkning is used. The interpreter (dynamic linker/loader) name is `/lib/ld-linux.so.2`. That is the path the loader will ask for on the target system
	- To list runtime libary dependencies (the shared libs required):
		- `readelf -d esrv | grep NEEDED` -> show `DT_NEEDED` entries (count those):
			- Example:
				```bash
				debpool07 ~/l05 $ readelf -d esrv | grep NEEDED
				 0x00000001 (NEEDED)                     Shared library: [libc.so.6]
				```
		- `ldd ./esrv` -> resolve them to the absolute pathes on the host and shows any missing libs
			- __Why:__ The presence of `.dynsym`, `.dynstr`, `.rel.plt`, `.got.plt` in your section list also indicates dynamic linking & PLT/GOT useage
			- Example:
				```bash
				debpool07 ~/l05 $ ldd esrv
						linux-gate.so.1 (0xf7ed8000)
						libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7c6a000)
						/lib/ld-linux.so.2 (0xf7eda000)
				```
5. Where the PLT / GOT are (for dynamic call targets)
	- From your secion output:
		- `.plt` at 0x08049020; `.got.plt` at 0x0804b334.
		- __Why:__ These addresses are whre function stubs / pointers will mapped. Good to note for hooking or return-to-GOT techniques

6. Symbol addresses: find functions like `main`, `cli_hndl`:
	- `nm -n esrv` or `readelf -s esrv` (symbol table).
	- __Why:__ give exact symbol addresses (if not stripped). If stripped, use `objdump -d esrv` and scan for strings and call sites

7. Relocations & which symbols are resolved at runtime
	- `readelf -r esrv` (relocations) and `readelf -d esrv` (dynamic tags)
	- __Why:__ shows which PLT/GOT slots are used and which relocations will be applied by the dynamic linker.

8. Disassemble to inspect code
	- `objdump -d esrv` or `objdump -D esrv` → you’ll see code bytes at the same addresses given in sections.
	- __Why:__ Confirm function boundaries, find useful gadgets, verify where vulnerable buffer lives relative to saved EIP.

9. Strings & quick checks
    - `strings esrv | less` → find plain text (helpful to find log messages or "/bin/sh" etc).
    - `file esrv` → quick summary.
    -` readelf -l esrv | grep STACK` or use checksec (if available) to list security features quickly. Your GNU_STACK RWE already tells you stack is executable.

## Real Runtime Virtual Address Space ($gdb `info proc mappings`)
```bash
gdb$ info proc mappings
process 387537
Mapped address spaces:

        Start Addr   End Addr       Size     Offset  Perms   objfile
         0x8048000  0x8049000     0x1000        0x0  r--p   /cs/home/ysheng21/l05/esrv
         0x8049000  0x804a000     0x1000     0x1000  r-xp   /cs/home/ysheng21/l05/esrv
         0x804a000  0x804b000     0x1000     0x2000  r--p   /cs/home/ysheng21/l05/esrv
         0x804b000  0x804c000     0x1000     0x2000  rw-p   /cs/home/ysheng21/l05/esrv
         0x804c000  0x806e000    0x22000        0x0  rw-p   [heap]
        0xb7d5b000 0xb7d7d000    0x22000        0x0  r--p   /usr/lib/i386-linux-gnu/libc.so.6
        0xb7d7d000 0xb7ef6000   0x179000    0x22000  r-xp   /usr/lib/i386-linux-gnu/libc.so.6
        0xb7ef6000 0xb7f76000    0x80000   0x19b000  r--p   /usr/lib/i386-linux-gnu/libc.so.6
        0xb7f76000 0xb7f78000     0x2000   0x21b000  r--p   /usr/lib/i386-linux-gnu/libc.so.6
        0xb7f78000 0xb7f79000     0x1000   0x21d000  rw-p   /usr/lib/i386-linux-gnu/libc.so.6
        0xb7f79000 0xb7f83000     0xa000        0x0  rw-p
        0xb7fc3000 0xb7fc5000     0x2000        0x0  rw-p
        0xb7fc5000 0xb7fc9000     0x4000        0x0  r--p   [vvar]
        0xb7fc9000 0xb7fcb000     0x2000        0x0  r-xp   [vdso]
        0xb7fcb000 0xb7fcc000     0x1000        0x0  r--p   /usr/lib/i386-linux-gnu/ld-linux.so.2
        0xb7fcc000 0xb7fef000    0x23000     0x1000  r-xp   /usr/lib/i386-linux-gnu/ld-linux.so.2
        0xb7fef000 0xb7ffd000     0xe000    0x24000  r--p   /usr/lib/i386-linux-gnu/ld-linux.so.2
        0xb7ffd000 0xb7fff000     0x2000    0x31000  r--p   /usr/lib/i386-linux-gnu/ld-linux.so.2
        0xb7fff000 0xb8000000     0x1000    0x33000  rw-p   /usr/lib/i386-linux-gnu/ld-linux.so.2
        0xbffdf000 0xc0000000    0x21000        0x0  rwxp   [stack]
```

1. The bianry it self (`esrv`)
	```bash
	0x8048000  0x8049000     0x1000        0x0  r--p   /cs/home/ysheng21/l05/esrv
	0x8049000  0x804a000     0x1000     0x1000  r-xp   /cs/home/ysheng21/l05/esrv
	0x804a000  0x804b000     0x1000     0x2000  r--p   /cs/home/ysheng21/l05/esrv
	0x804b000  0x804c000     0x1000     0x2000  rw-p   /cs/home/ysheng21/l05/esrv
	```
	- These four 4KB pages(each 0X1000 in size) correspond exactly 4 `LOAD` segments in the ELF
	- Permission match what we saw in Program Headers:
	- r--p (read-only) → ELF headers / metadata.
	- r-xp (read + exec) → code (.text, .plt).
	- r--p (read-only) → constants, .rodata.
	- rw-p (read/write) → .data, .bss, GOT.

2. The heap
	```bash
	0x804c000  0x806e000   rw-p  [heap]
	```
	- Heap starts right after your data segment, at` 0x804c000`.
	- The kernel gave it ~0x22000 bytes (136 KB) initially.
	- This grows upward when you call `brk()` / `malloc()`.

3. libc (shared library)
	```bash
	0xb7d5b000 0xb7f79000   ...   /usr/lib/i386-linux-gnu/libc.so.6
	```
	- This is glibc, the standard libaray
	- Notice: base address `0xb7d5b000` -> that’s much higher in memory than your program (ASLR places shared libs up near 0xb7xxxxxx).
	- It has its own mapping split into multiple regions:
		- r--p (read-only headers),
		- r-xp (executable code),
		- r--p (read-only data),
		- rw-p (writable data, .data/.bss inside libc).

4. Anonymous mappings: mmap (heap extensions, thread arenas, etc.)
	```bash
	0xb7f79000 0xb7f83000  rw-p
	0xb7fc3000 0xb7fc5000  rw-p
	```
	- These are anonymous memory regions (not backed by a file). Used for malloc arenas, TLS, or other dynamic allocations.

5. Kernel-provided regions
	```bash
	0xb7fc5000 0xb7fc9000  r--p  [vvar]
	0xb7fc9000 0xb7fcb000  r-xp  [vdso]
	```
6. The dynamic linker (`ld-linux.so.2`)
	```bash
	0xb7fcb000 0xb8000000  ...  /usr/lib/i386-linux-gnu/ld-linux.so.2
	```
	- This is the ELF interpreter (INTERP segment from readelf).
	- It is responsible for resolving dynamic symbols and relocating libc.
	- It lives right below the 0xb8000000 boundary (top of user space on 32-bit).

7. The Stack
	```bash
	0xbffdf000 0xc0000000  rwxp  [stack]
	```
	- Stack lives at the very top of the user address space (near 0xc0000000 for 32-bit).
	- It grows downward (towards lower addresses).
	- Here it is marked rwxp — read, write, execute (because you compiled with -z execstack). Normally, stack should be rw-p only.

## Stack (registers, instructions, and calculation)

__What is Stack jitter__
- `Stack jitter` means randomly changing the starting address of the starting address of the stack each time a program runs.
- `Why`:
    - Because most sttacks (like stack smashing) rely on predicting exactly where the stack will live in memory
    - If the OS keeps moving it around, it becomes much harder to guess where your shellcode or return address should go.

__What is Gadget__
- A `gadget` is a short sequence of instructions already present in a program or libraries (usually ending with `ret`) that attacker reuses by arranging return addresses on the stack.
- Gadgets are building blocks of __ROP (Return-Oriented Programming)__ chains: they let you perform arbitarry computation without injecting new executable code.

# Control-flow Hijacking | Code Injection | Shellcode Development

## NOP

## Register Anatanomy
- There are 8 general-purpose registers, each 32 bits (4 bytes) wide:
- `E` prefix = Extended (added when x86 went from 16-bit to 32-bit).

__Register Table Lookup__
| 32-bit name | 16-bit (low half) | 8-bit (lower half of 16) | 8-bit (upper half of 16) | Typical Purpose                             |
| ----------- | ----------------- | ------------------------ | ------------------------ | ------------------------------------------- |
| **EAX**     | AX                | AL                       | AH                       | “Accumulator” — arithmetic, return values   |
| **EBX**     | BX                | BL                       | BH                       | “Base” — memory addressing                  |
| **ECX**     | CX                | CL                       | CH                       | “Counter” — loops/shifts                    |
| **EDX**     | DX                | DL                       | DH                       | “Data” — I/O ops, multiplication/division   |
| **ESI**     | SI                | —                        | —                        | “Source index” — string/memory ops          |
| **EDI**     | DI                | —                        | —                        | “Destination index”                         |
| **EBP**     | BP                | —                        | —                        | “Base pointer” — points to stack frame base |
| **ESP**     | SP                | —                        | —                        | “Stack pointer” — top of stack              |


__Byte Layout__
- Example: `eax = 0x12345678`

| Bit range | Part           | Size    | Example value |
| --------- | -------------- | ------- | ------------- |
| 31-16     | (high 2 bytes) | 16 bits | `0x1234`      |
| 15-8      | AH             | 8 bits  | `0x56`        |
| 7-0       | AL             | 8 bits  | `0x78`        |


__Arithmetic and Sub-Registers__
```text
mov eax, 0
mov al, 0xFF       ; sets only low byte to 0xFF
inc eax            ; adds 1 → wraps low byte
```
- Now `eax = 0x00000100`(because 0xFF + 1 → carry into next byte).

__Stack and Pointer Regirester (esp, ebp)__
- ESP (Stack Pointer):
    - Always points to the top of the stack (lowest used address).
- EBP (Base Pointer): 
    - Marks the base of the current stack frame.
- When `push` something:
    ```text
    push eax   ; ESP = ESP - 4, then [ESP] = EAX
    ```
- When `pop`
    ```text
    pop ebx    ; EBX = [ESP], then ESP = ESP + 4
    ```

## System Call in Registers
__How x86-32 Syscalls Work__
- System call table[[Link](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit)]
- In 32-bit Linux, syscalls are made with the int 0x80 instruction: that’s a software interrupt that switches the CPU into kernel mode.

__Calling Convention__
| Register         | Meaning                        |
| ---------------- | ------------------------------ |
| **EAX**          | System call number (unique ID) |
| **EBX**          | 1st argument                   |
| **ECX**          | 2nd argument                   |
| **EDX**          | 3rd argument                   |
| **ESI**          | 4th argument                   |
| **EDI**          | 5th argument                   |
| **EBP**          | 6th argument                   |
| *(Return value)* | Stored in **EAX**              |

- Then execute: `int 0x80`

__Example: Write : "Hello World"__
```text
section .text
global _start

_start:
    mov eax, 4        ; syscall number 4 = write
    mov ebx, 1        ; file descriptor 1 = STDOUT
    mov ecx, msg      ; pointer to message
    mov edx, len      ; length of message
    int 0x80          ; trigger syscall

    mov eax, 1        ; syscall number 1 = exit
    xor ebx, ebx      ; return code 0
    int 0x80

section .data
msg db "Hello, world!", 0x0A
len equ $-msg
```
- Each part corresponding directory to C code
```c
write(1, "Hello, world!\n", 13);
exit(0);
```

## Q: What's the benefit of NULL-free shellcoding?
- __In short__:  NULL-free shellcode avoids the `0x00` byte (and often other “bad” bytes) so the payload won’t be truncated or corrupted by string-based copying/processing. That makes exploitation possible when the target copies input with string functions or treats \x00 as a terminator.

__Reasons__
- `Payload embedding constraints`: When you push bytes into a buffer through code that treats data as C strings or formats, 0x00 breaks the embedding.
- `Exploit primitives that rely on exact layout`: Overwriting return addresses, saved regs, or stack contents requires exact byte patterns. Unexpected nulls shift layout or stop copying.
- `String APIs truncate at '\0'`: Many vulnerable programs copy attacker data with strcpy, strncpy (when misused), gets-style, sprintf, etc. A 0x00 in your payload will be interpreted as end-of-string and everything after it will be lost.


__`strcpy` / `strncpy` / other `str*()` specifics — can they inject shellcode?__
- `strcpy(dest, src)` copies bytes from src to dest until it sees a '\0' in src, then it writes the terminating '\0' to dest.
    - So: if your shellcode (the bytes you want copied) contains 0x00 anywhere, `strcpy` will stop before that byte and the rest will never be copied.
    - If your shellcode contains no `0x00`, strcpy will copy the whole shellcode and then append a `0x00` after it (i.e., the destination will be shellcode||`0x00`).
- `strncpy(dest, src, n)` will copy up to n bytes; if src shorter than n, zeros pad the rest. strncpy can help if you know exact lengths, but beware of implicit zero-padding.



# Non-Executable Memory | Ret2libc | Code Resue 

## Q: What's the purpose of the %esp register in x86? What does it offer to attackers controlling it (in terms of code reuse)?

__Purpose__
- `%esp` is the stack pointer.
- It always points to the current top of the stack (the last item pushed).
- On x86 the stack grows downward (toward lower addresses), so pushing data subtracts from `%esp`, popping adds to `%esp`.
- Almost all function calls, local variables, and saved state (return addresses, saved registers) are arranged relative to `%esp` (and sometimes `%ebp` / frame pointer).

__What an attacker gains if they control it__
- __In short__: Controlling `%esp` gives an attacker a way to make the CPU treat attacker-controlled memory as the stack, which is the attacker’s playground for arranging addresses (gadgets), function arguments, and return sites.
1. `Return addresses`: ret pops a value from the address `%esp` points to and jumps there. If the attacker controls that memory, they control the popped address → they can transfer control flow accordingly.
2. `Stack arguments and local storage`: Functions that read arguments or locals from `[esp + offset]` or via `[ebp - offset]` (after a mov `%esp`, `%ebp` prologue) will be reading attacker-controlled data. That lets attackers influence the parameters to library functions called by the program.
3. `A stream for gadgets (ROP)`: By pivoting `%esp` into an attacker-controlled buffer, the attacker can place a sequence of addresses (addresses of gadgets) there; ret instructions will pop each gadget address in sequence (this is the basis of return-oriented programming — ROP). Controlling `%esp` turns a memory buffer into the program’s execution stack.
4. `Fake stack frames (setcontext) -style control`: By controlling stack contents and `%esp` you can craft fake saved registers, return addresses, and sometimes emulate the effect of setcontext or longjmp to resume execution in arbitrary contexts.
5. `Stack scanning / stack pointer arithmetic`: Some machine instructions treat `%esp` specially (push/pop, enter/leave, function prologues/epilogues). By changing `%esp` you can change where these instructions affect memory, causing the program to read/write attacker-chosen memory regions.