# Shellcode Development

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