# General

## Q1
```text
080491f3 <entry>:
 80491f3:    55                       push   %ebp
 80491f4:    89 e5                    mov    %esp,%ebp
 80491f6:    83 ec 08                 sub    $0x8,%esp
 80491f9:    8b 55 08                 mov    0x8(%ebp),%edx
 80491fc:    8b 45 0c                 mov    0xc(%ebp),%eax
 80491ff:    01 c2                    add    %eax,%edx
 8049201:    a1 20 c0 04 08           mov    0x804c020,%eax
 8049206:    83 ec 08                 sub    $0x8,%esp
 8049209:    52                       push   %edx
 804920a:    ff 75 0c                 push   0xc(%ebp)
 804920d:    ff 75 08                 push   0x8(%ebp)
 8049210:    68 2c a0 04 08           push   $0x804a02c
 8049215:    68 08 a0 04 08           push   $0x804a008
 804921a:    50                       push   %eax
 804921b:    e8 30 fe ff ff           call   8049050 <fprintf@plt>
 8049220:    83 c4 20                 add    $0x20,%esp
 8049223:    90                       nop
 8049224:    c9                       leave
 8049225:    c3                       ret
```
- Q: __objdump local variables & parameters__
    - Find unique offset of %ebp
    - Positive offsets from %ebp = parameters
    - Negative offsets from %ebp = local variables
- Q: __Does entry() call external functions?__
    - Yes — calls 1 external function: fprintf.
    - A @plt suffix means:
        - It is an external library function (not defined in the binary)
        - The PLT stub will jump to the function in libc (after lazy binding via GOT).
- Q: __Does entry() use stack smashing protection (stack canaries)?__
    - Compilers insert a secret value (a “canary”) into the stack to detect corruption.
        - if (canary has changed) → call __stack_chk_fail()
        - If an overflow clobbered the return address, it almost certainly overwrote the canary too.
        - The program immediately aborts instead of returning into attacker code.
    - What does the stack look like if stack have stack smashing protection is on?
        - If you do NOT see these instructions → no stack canary.
            ```text
            Begin of stack:
            mov %gs:0x14, %eax      ; load canary from thread-local storage
            mov %eax, -0x4(%ebp)    ; store canary under saved EBP
            At the end of the stack:
            mov -0x4(%ebp), %edx    ; load stored canary
            xor %gs:0x14, %edx      ; compare canary values
            jne __stack_chk_fail@plt ; mismatch → stack smash detected
            ```
- Q: __Does entry() employ FORTIFY_SOURCE?__
    - FORTIFY_SOURCE is a compile-time + run-time hardening feature used by GCC and glibc.
    - It automatically replaces some unsafe C functions with safer, bounds-checked versions, when possible.
    - It helps detect: 
        - buffer overflows; format string misuse; unsafe string/buffer operations; memory copying that exceeds known buffer size
    - Without FORTIFY:
        - fprintf@plt
    - With FORTIFY enabled:
        - __fprintf_chk@plt

## Q2
- Assuming an x86 (32-bit) system, which register (%eax, %ebx, %ecx, %edx, %esi, %edi, %ebp, %esp, %eip, %eflags) needs to be controlled in order to perform a return-oriented programming (ROP) attack?
    - %esp: the stack pointer. In Return-Oriented Programming, every ret pops the next gadget address from the stack. Therefore the stack becomes the instruction stream, and %esp becomes the effective instruction pointer for the chain. Controlling %esp = controlling which gadget executes next.
- More registers:
    - %eip — instruction pointer
        - The actual CPU program counter. Overwriting it = classic stack overflow. ROP does not require direct control, since ret updates %eip automatically.
    - %ebp — base/frame pointer
        - Anchor for stack frames. Sometimes useful for stack pivots or bypassing canaries, but not critical for ROP.

## Q3
```text
Someone suggested the following, alternative implementation of the
stack protector: in the function prologue, the random value (i.e.,
canary/cookie template), before being pushed onto the stack, is XOR-ed with
the saved return address; similarly, in the function epilogue, the pushed
canary/cookie gets XOR-ed, again with the saved return address, before
being compared with the template. Does this (alternative) implementation
provide any additional benefit? (Justify your answer for full credit.)
```
- Yes it does. This (new) implementation can detect direct overwrites to the return address.
- Specifically, during the execution of the epilogue, the pushed canary/cookie will be XOR’ed with the saved return address, and if the latter is modified, then the resulting cookie will not match its template.

## Q4: 5 Major Binary Hardening Mechanisms (x86 Linux)
1. PIE (Position-Independent Executable)
    - Allows ASLR to fully randomize the binary load address.
    - Detect by: `Type: DYN (Position-Independent Executable)`
2. NX / DEP (Non-Executable Stack)
    - Makes the stack non-executable.
    - Detect by section header flags for .note.GNU-stack or `program header`:
        - Presence of GNU_STACK without E (Executable) flag → NX enabled.
3. Stack Canaries / SSP (Stack Smashing Protector)
    - Detect by presence of:
        - symbol: `__stack_chk_fail`
        - text relocation: .note.gnu.property with IBT/SHSTK (newer systems)
4. RELRO (Relocation Read-Only)
    - It is a hardening technique that makes a part of the process memory read-only after relocations are applied at program startup.
    - The dynamic linker writes important addresses into the GOT (Global Offset Table). After this is done, we lock the GOT so attackers cannot overwrite function pointers.
    - RELRO: GNU_RELRO is present. (Given that .got.plt does not exist it is highly-likely that BINDNOW is employed too, but we cannot be certain about this until we inspect the .dynamic section.)
5. FORTIFY_SOURCE
    - Compile-time bounds-checking.
    - Detect by presence of:
        ```text
        __chk*
        __builtin___memcpy_chk
        ```
- Full ASLR: The binary is position-independent (see ‘Type’, ‘Entry point address’, or the ‘Addr’ field of every section – everything is relative to 0x0), so if ASLR is supported, the binary itself can be mapped to a random location.

## Q5: Stack pivoting
- Stack pivoting is a core technique in advanced ROP exploits
- Moving the stack pointer (`esp`) away from the real stack to a fake stack that the attacker controls.
- Because ROP requires a long chain of gadget addresses, but the real stack often:
    - is too small,
    - contains canaries,
    - or isn’t fully under attacker control.
- So instead of trying to build the ROP chain on the real stack, you do this:
    - put the ROP chain somewhere else (heap, .bss, global buffer)
    - then use a gadget to pivot (esp) to that location
    - now ret will execute each gadget in your fake stack

## Q6: Format String
- What Is a Format String Vulnerability?
    - A format string vulnerability happens when: User input becomes the format string, instead of a fixed string.
- In C, functions like printf, fprintf, sprintf, etc. take a format string that tells them how to interpret arguments.
    - Example: ```printf("Number: %d\n", x);``` -> Here "Number: %d\n" is the format string, and %d tells printf to expect an int.
- A format string vulnerability happens when: User input becomes the format string, instead of a fixed string.
    - If user_input = "Hello", it's fine.
    - But if user_input = `"%x %x %x %x"`:
    - printf will treat those as format directives
    - and start reading values from the stack
    - even though the program did not pass these arguments
    - This leads to information disclosure.
- Worst Case `%n` → memory write
    - This is where format strings become exploitable.
    - %n tells printf:
        - Write the number of bytes printed so far into the memory address pointed to by the next argument.
        - Example: `printf("AAAA%n", &x);` -> After printing 4 bytes, x becomes 4.
        - If the attacker controls the format string: They can cause printf to read a “pointer” (really: raw stack data) and write to that location.
        - This becomes powerful enough to:
            - overwrite saved return addresses
            - overwrite function pointers
            - bypass stack canaries
            - write to `.got.plt` entries (ret2plt attacks)
            - escalate into ROP / arbitrary code execution
