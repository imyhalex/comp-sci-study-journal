# Control Flow Hijacking

- When a program runs, the cpu follows a control flow: instruction after instruction, ocassionally jumping when it hits things like loops, conditionals, or function calls

- Control Flow Hijacking happens when an attacker forces the program to execute instructions in an order different from what the prgrammer intended

- This usually means tricking the program into jumping to malicious code, instead of countinuing normally

## How Control Flow Noramallu Works
- CPU executes instruction sequentially (next instruction in memory)
- Branch instructions (if, goto, loops) modify the normal order.
- Function calls push the return address on the stack, so after the function finishes, the CPU knows where to resume.

## What Hijacking Looks Like
- An attacker alters this flow by overwriting:
    - Return addresses on the stack
    - Function pointers
    - Virtual function tables (C++ vtables)
    - Exception handlers

## Example: Buffer Overflow -> Return Address Hijack (Classic)
```c
#include <stdio.h>
#include <string.h>

void vulnerable() {
    char buf[16];
    printf("Enter input: ");
    gets(buf); // ❌ dangerous, no bounds checking
}

int main() {
    vulnerable();
    printf("Safe return\n");
    return 0;
}
```
- What Happens:
    - Normally: user input fills buf, function returns → "Safe return".
    - If attacker enters too many characters, they overwrite memory beyond buf, including the return address.
    - Now instead of returning to main, CPU “returns” to attacker’s code.

## Advanced Example: Function Pointer Hijack
```c
#include <stdio.h>

void secret() {
    printf("Hacked! Control flow hijacked.\n");
}

void safe() {
    printf("This is safe.\n");
}

int main() {
    void (*func)(void) = safe;
    char buffer[8];

    // Attacker overwrites function pointer
    strcpy(buffer, "AAAAAAAAAAAAAAAAAAAA"); 
    func(); // Could now point to secret()
}
```
- Here, if memory corruption changes func’s address → program executes secret() instead of safe().


## Real-World Attacks:
- Stack smashing (buffer overflow): overwrite return address.
- Heap spraying + use-after-free: redirect function calls.
- Return-Oriented Programming (ROP): chain together existing code snippets to avoid injecting new code.
- Control Flow Integrity (CFI) bypasses: trick the system into “valid but unintended” jumps.

