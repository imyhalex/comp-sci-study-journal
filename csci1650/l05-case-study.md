# Case

```c
/*
 * Echo Protocol (TCP-based Echo Service)
 *  - RFC 862: https://tools.ietf.org/html/rfc862
 *
 * Vasileios P. Kemerlis <vpk@cs.brown.edu>
 *  - CSCI 1650: Software Security and Exploitation
 *  - https://cs.brown.edu/courses/csci1650/
 */

/*
 * Bugs:
 *  - Stack-based buffer overflow in 'cli_hndl()'
 */

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BACKLOG_DFL     1       /* default backlog value                */
#define ECHO_PORT_DFL   7777    /* default Echo Protocol port (TCP)     */
#define BUF_SZ          512     /* buffer size                          */
#define BUF_LEN         (BUF_SZ<<1)     /* (BUF_SZ * 2)                 */


/* cleanup routine */
static void
cleanup(int srv_fd)
{
        /* socket cleanup */
        if (srv_fd != -1)
                close(srv_fd);
}

/* client handler */
static void
cli_hndl(int cfd)
{
        /* message buffer                       */
        char    buf[BUF_SZ];

        /* length pointer                       */
        ssize_t len;

        /* cleanup                              */
        /* memset(buf, 0, BUF_SZ);              */

        /*
         * main processing loop; messages
         *
         * BUG: 'BUF_LEN' = 'BUF_SZ<<1' (should be 'BUF_SZ' or less)
         */
        while ((len = read(cfd, buf, BUF_LEN)) > 0) {
                /*
                 * don't bother checking
                 * the return value :)
                 */
                write(cfd, buf, len);
        }

        /* error reporting                      */
        if (len == -1)
                perror("[-] read(2) failed");

        /* done                                 */
}

int
main(int argc, char **argv)
{
        /* socket descriptors; server, client   */
        int sfd = -1, cfd = -1;

        /* IPv4 addresses; server, client       */
        struct sockaddr_in
                sin = {
                        .sin_family     = AF_INET,
                        .sin_port       = htons(ECHO_PORT_DFL),
                        .sin_addr       = { INADDR_ANY },
                },
                cin = {
                        .sin_family     = 0,
                        .sin_port       = 0,
                        .sin_addr       = { .s_addr = 0 },
                };

        /* client address size; value-result    */
        socklen_t clen  = sizeof(struct sockaddr_in);

        /* bool (enable)                        */
        int enable      = 0xe4ff;

        /* verbose                              */
        fprintf(stdout, "[+] Creating listening socket... ");

        /* get the listening socket             */
        if ((sfd = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
                /* failed                       */
                fprintf(stdout, "[FAILURE]\n"); fflush(stdout);
                perror("[-] socket(2) failed");
                goto err;
        }

        /* enable address reuse                 */
        if (setsockopt(sfd,
                        SOL_SOCKET,
                        SO_REUSEADDR,
                        &enable,
                        sizeof(int)) == -1)
                perror("[*] setsockopt(2) failed");

        /* verbose                              */
        fprintf(stdout, "[SUCCESS]\n"); fflush(stdout);
        fprintf(stdout, "[+] Binding listening socket.... ");

        /* bind the listening socket            */
        if (bind(sfd,
                (const struct sockaddr *)&sin,
                sizeof(struct sockaddr_in)) == -1) {
                /* failed                       */
                fprintf(stdout, "[FAILURE]\n"); fflush(stdout);
                perror("[-] bind(2) failed");
                goto err;
        }

        /* verbose                              */
        fprintf(stdout, "[SUCCESS]\n"); fflush(stdout);
        fprintf(stdout, "[+] Listening at %s:%hu... ",
                        inet_ntoa(sin.sin_addr),
                        ntohs(sin.sin_port));

        /* mark the socket as passive           */
        if (listen(sfd, BACKLOG_DFL) == -1) {
                /* failed                       */
                fprintf(stdout, "[FAILURE]\n"); fflush(stdout);
                perror("[-] listen(2) failed");
                goto err;
        }

        /* verbose                              */
        fprintf(stdout, "[SUCCESS]\n"); fflush(stdout);

        /* main processing loop; connections    */
        while ((cfd = accept(sfd, (struct sockaddr *)&cin, &clen)) != -1) {
                /* verbose                      */
                fprintf(stdout, "[*] New connection from %s:%hu\n",
                                inet_ntoa(cin.sin_addr),
                                ntohs(cin.sin_port));

                /* handle the client            */
                cli_hndl(cfd);

                /*
                 * cleanup and prepare
                 * for the next client
                 */
                close(cfd);
                memset(&cin, 0, sizeof(struct sockaddr_in));
                clen    = sizeof(struct sockaddr_in);
                cfd     = -1;
        }

        /* never reached                        */

        /* cleanup                              */
        cleanup(sfd);

        /* done; success                        */
        return EXIT_SUCCESS;

        /* error handling                       */
err:
        /* cleanup                              */
        cleanup(sfd);

        /* done; error                          */
        return EXIT_FAILURE;
}
```

# Run
```bash
debpool07 ~/l05 $ make esrv_run
setarch i686 -3 -R       env -i          ./esrv
[+] Creating listening socket... [SUCCESS]
[+] Binding listening socket.... [SUCCESS]
[+] Listening at 0.0.0.0:7777... [SUCCESS]

# in another termnial
debpool07 ~ $ nc debpool07 7777

debpool07 ~/l05 $ make esrv_run
setarch i686 -3 -R       env -i          ./esrv
[+] Creating listening socket... [SUCCESS]
[+] Binding listening socket.... [SUCCESS]
[+] Listening at 0.0.0.0:7777... [SUCCESS]
[*] New connection from 10.116.52.18:60302
```
## Antamomy `readelf -e esrv`:
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

### Study of this ELF
1. Quick Metadata (what kind of binary it is)
	- `readelf -h esrv` -> shows `ELF32` and `Type: EXEC`.
		- __Meaning__: 32-bit executable with fixed virtual address (non-PIE). You can trust the addresses in the headers as the addresses the loader will use for this binary itself
	- `Entry point address`: the location of your first instruction

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

### Q&As
![img](./img/Screenshot%202025-10-02%20205128.png)

### Example Commands
```bash
file esrv                        # quick type summary
readelf -h esrv                  # ELF header (class / type / entry)
readelf -l esrv                  # Program headers (segments) -> where mapped
readelf -S esrv                  # Section headers -> addresses of .text/.data/.got
readelf -d esrv | sed -n 's/.*NEEDED.*$/&/p'   # list DT_NEEDED
readelf -r esrv                  # relocation entries (.rel.plt etc)
readelf -s esrv | less           # symbol table
nm -n esrv                       # symbols sorted by address
objdump -d esrv | less           # disassembly with addresses
ldd esrv                         # runtime shared-library resolution (paths)
strings esrv | grep -i 'ld-linux' -n   # search for interpreter string
```

## GDB
```bash
# run application within gdb
gdb$ r
Starting program: /cs/home/ysheng21/l05/esrv
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[+] Creating listening socket... [SUCCESS]
[+] Binding listening socket.... [SUCCESS]
[+] Listening at 0.0.0.0:7777... [SUCCESS]
```

### Real Runtime Virtual Address Space
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

### 
```bash
gdb$ disassemble main

gdb$ si # step 


```
0### Putting it all together
```bash
0xc0000000   [top of user space]
   [stack]          rwxp
-------------------------------
0xb7fcb000   ld-linux.so.2 (dynamic linker)
0xb7fc5000   [vvar]/[vdso]
0xb7d5b000   libc.so.6
-------------------------------
0x806e000    end of heap
0x804c000    heap start
0x8048000    your program (esrv)
-------------------------------
0x00000000   [NULL page, unmapped]
```

## `objdump -d`
```bash
debpool07 ~/l05 $ objdump -d esrv

esrv:     file format elf32-i386


Disassembly of section .init:

08049000 <_init>:
 8049000:       53                      push   %ebx
 8049001:       83 ec 08                sub    $0x8,%esp
 8049004:       e8 77 01 00 00          call   8049180 <__x86.get_pc_thunk.bx>
 8049009:       81 c3 2b 23 00 0       add    $0x232b,%ebx
 804900f:       8b 83 fc ff ff ff       mov    -0x4(%ebx),%eax
 8049015:       85 c0                   test   %eax,%eax
 8049017:       74 02                   je     804901b <_init+0x1b>
 8049019:       ff d0                   call   *%eax
 804901b:       83 c4 08                add    $0x8,%esp
 804901e:       5b                      pop    %ebx
 804901f:       c3                      ret

Disassembly of section .plt:

08049020 <setsockopt@plt-0x10>:
 8049020:       ff 35 38 b3 04 08       push   0x804b338
 8049026:       ff 25 3c b3 04 08       jmp    *0x804b33c
 804902c:       00 00                   add    %al,(%eax)
        ...

08049030 <setsockopt@plt>:
 8049030:       ff 25 40 b3 04 08       jmp    *0x804b340
 8049036:       68 00 00 00 00          push   $0x0
 804903b:       e9 e0 ff ff ff          jmp    8049020 <_init+0x20>

08049040 <__libc_start_main@plt>:
 8049040:       ff 25 44 b3 04 08       jmp    *0x804b344
 8049046:       68 08 00 00 00          push   $0x8
 804904b:       e9 d0 ff ff ff          jmp    8049020 <_init+0x20>

08049050 <read@plt>:
 8049050:       ff 25 48 b3 04 08       jmp    *0x804b348
 8049056:       68 10 00 00 00          push   $0x10
 804905b:       e9 c0 ff ff ff          jmp    8049020 <_init+0x20>

08049060 <fflush@plt>:
 8049060:       ff 25 4c b3 04 08       jmp    *0x804b34c
 8049066:       68 18 00 00 00          push   $0x18
 804906b:       e9 b0 ff ff ff          jmp    8049020 <_init+0x20>

08049070 <inet_ntoa@plt>:
 8049070:       ff 25 50 b3 04 08       jmp    *0x804b350
 8049076:       68 20 00 00 00          push   $0x20
 804907b:       e9 a0 ff ff ff          jmp    8049020 <_init+0x20>

08049080 <htons@plt>:
 8049080:       ff 25 54 b3 04 08       jmp    *0x804b354
 8049086:       68 28 00 00 00          push   $0x28
 804908b:       e9 90 ff ff ff          jmp    8049020 <_init+0x20>

08049090 <perror@plt>:
 8049090:       ff 25 58 b3 04 08       jmp    *0x804b358
 8049096:       68 30 00 00 00          push   $0x30
 804909b:       e9 80 ff ff ff          jmp    8049020 <_init+0x20>

080490a0 <accept@plt>:
 80490a0:       ff 25 5c b3 04 08       jmp    *0x804b35c
 80490a6:       68 38 00 00 00          push   $0x38
 80490ab:       e9 70 ff ff ff          jmp    8049020 <_init+0x20>

080490b0 <fwrite@plt>:
 80490b0:       ff 25 60 b3 04 08       jmp    *0x804b360
 80490b6:       68 40 00 00 00          push   $0x40
 80490bb:       e9 60 ff ff ff          jmp    8049020 <_init+0x20>

080490c0 <fprintf@plt>:
 80490c0:       ff 25 64 b3 04 08       jmp    *0x804b364
 80490c6:       68 48 00 00 00          push   $0x48
 80490cb:       e9 50 ff ff ff          jmp    8049020 <_init+0x20>

080490d0 <write@plt>:
 80490d0:       ff 25 68 b3 04 08       jmp    *0x804b368
 80490d6:       68 50 00 00 00          push   $0x50
 80490db:       e9 40 ff ff ff          jmp    8049020 <_init+0x20>

080490e0 <bind@plt>:
 80490e0:       ff 25 6c b3 04 08       jmp    *0x804b36c
 80490e6:       68 58 00 00 00          push   $0x58
 80490eb:       e9 30 ff ff ff          jmp    8049020 <_init+0x20>

080490f0 <memset@plt>:
 80490f0:       ff 25 70 b3 04 08       jmp    *0x804b370
 80490f6:       68 60 00 00 00          push   $0x60
 80490fb:       e9 20 ff ff ff          jmp    8049020 <_init+0x20>

08049100 <listen@plt>:
 8049100:       ff 25 74 b3 04 08       jmp    *0x804b374
 8049106:       68 68 00 00 00          push   $0x68
 804910b:       e9 10 ff ff ff          jmp    8049020 <_init+0x20>

08049110 <ntohs@plt>:
 8049110:       ff 25 78 b3 04 08       jmp    *0x804b378
 8049116:       68 70 00 00 00          push   $0x70
 804911b:       e9 00 ff ff ff          jmp    8049020 <_init+0x20>

08049120 <socket@plt>:
 8049120:       ff 25 7c b3 04 08       jmp    *0x804b37c
 8049126:       68 78 00 00 00          push   $0x78
 804912b:       e9 f0 fe ff ff          jmp    8049020 <_init+0x20>

08049130 <close@plt>:
 8049130:       ff 25 80 b3 04 08       jmp    *0x804b380
 8049136:       68 80 00 00 00          push   $0x80
 804913b:       e9 e0 fe ff ff          jmp    8049020 <_init+0x20>

Disassembly of section .text:

08049140 <_start>:
 8049140:       31 ed                   xor    %ebp,%ebp
 8049142:       5e                      pop    %esi
 8049143:       89 e1                   mov    %esp,%ecx
 8049145:       83 e4 f0                and    $0xfffffff0,%esp
 8049148:       50                      push   %eax
 8049149:       54                      push   %esp
 804914a:       52                      push   %edx
 804914b:       e8 19 00 00 00          call   8049169 <_start+0x29>
 8049150:       81 c3 e4 21 00 00       add    $0x21e4,%ebx
 8049156:       6a 00                   push   $0x0
 8049158:       6a 00                   push   $0x0
 804915a:       51                      push   %ecx
 804915b:       56                      push   %esi
 804915c:       c7 c0 c3 92 04 08       mov    $0x80492c3,%eax
 8049162:       50                      push   %eax
 8049163:       e8 d8 fe ff ff          call   8049040 <__libc_start_main@plt>
 8049168:       f4                      hlt
 8049169:       8b 1c 24                mov    (%esp),%ebx
 804916c:       c3                      ret
 804916d:       66 90                   xchg   %ax,%ax
 804916f:       90                      nop

08049170 <_dl_relocate_static_pie>:
 8049170:       c3                      ret
 8049171:       66 90                   xchg   %ax,%ax
 8049173:       66 90                   xchg   %ax,%ax
 8049175:       66 90                   xchg   %ax,%ax
 8049177:       66 90                   xchg   %ax,%ax
 8049179:       66 90                   xchg   %ax,%ax
 804917b:       66 90                   xchg   %ax,%ax
 804917d:       66 90                   xchg   %ax,%ax
 804917f:       90                      nop

08049180 <__x86.get_pc_thunk.bx>:
 8049180:       8b 1c 24                mov    (%esp),%ebx
 8049183:       c3                      ret
 8049184:       66 90                   xchg   %ax,%ax
 8049186:       66 90                   xchg   %ax,%ax
 8049188:       66 90                   xchg   %ax,%ax
 804918a:       66 90                   xchg   %ax,%ax
 804918c:       66 90                   xchg   %ax,%ax
 804918e:       66 90                   xchg   %ax,%ax

08049190 <deregister_tm_clones>:
 8049190:       b8 8c b3 04 08          mov    $0x804b38c,%eax
 8049195:       3d 8c b3 04 08          cmp    $0x804b38c,%eax
 804919a:       74 24                   je     80491c0 <deregister_tm_clones+0x30>
 804919c:       b8 00 00 00 00          mov    $0x0,%eax
 80491a1:       85 c0                   test   %eax,%eax
 80491a3:       74 1b                   je     80491c0 <deregister_tm_clones+0x30>
 80491a5:       55                      push   %ebp
 80491a6:       89 e5                   mov    %esp,%ebp
 80491a8:       83 ec 14                sub    $0x14,%esp
 80491ab:       68 8c b3 04 08          push   $0x804b38c
 80491b0:       ff d0                   call   *%eax
 80491b2:       83 c4 10                add    $0x10,%esp
 80491b5:       c9                      leave
 80491b6:       c3                      ret
 80491b7:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi
 80491be:       66 90                   xchg   %ax,%ax
 80491c0:       c3                      ret
 80491c1:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi
 80491c8:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi
 80491cf:       90                      nop

080491d0 <register_tm_clones>:
 80491d0:       b8 8c b3 04 08          mov    $0x804b38c,%eax
 80491d5:       2d 8c b3 04 08          sub    $0x804b38c,%eax
 80491da:       89 c2                   mov    %eax,%edx
 80491dc:       c1 e8 1f                shr    $0x1f,%eax
 80491df:       c1 fa 02                sar    $0x2,%edx
 80491e2:       01 d0                   add    %edx,%eax
 80491e4:       d1 f8                   sar    %eax
 80491e6:       74 20                   je     8049208 <register_tm_clones+0x38>
 80491e8:       ba 00 00 00 00          mov    $0x0,%edx
 80491ed:       85 d2                   test   %edx,%edx
 80491ef:       74 17                   je     8049208 <register_tm_clones+0x38>
 80491f1:       55                      push   %ebp
 80491f2:       89 e5                   mov    %esp,%ebp
 80491f4:       83 ec 10                sub    $0x10,%esp
 80491f7:       50                      push   %eax
 80491f8:       68 8c b3 04 08          push   $0x804b38c
 80491fd:       ff d2                   call   *%edx
 80491ff:       83 c4 10                add    $0x10,%esp
 8049202:       c9                      leave
 8049203:       c3                      ret
 8049204:       8d 74 26 00             lea    0x0(%esi,%eiz,1),%esi
 8049208:       c3                      ret
 8049209:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi

08049210 <__do_global_dtors_aux>:
 8049210:       f3 0f 1e fb             endbr32
 8049214:       80 3d 90 b3 04 08 00    cmpb   $0x0,0x804b390
 804921b:       75 1b                   jne    8049238 <__do_global_dtors_aux+0x28>
 804921d:       55                      push   %ebp
 804921e:       89 e5                   mov    %esp,%ebp
 8049220:       83 ec 08                sub    $0x8,%esp
 8049223:       e8 68 ff ff ff          call   8049190 <deregister_tm_clones>
 8049228:       c6 05 90 b3 04 08 01    movb   $0x1,0x804b390
 804922f:       c9                      leave
 8049230:       c3                      ret
 8049231:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi
 8049238:       c3                      ret
 8049239:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi

08049240 <frame_dummy>:
 8049240:       f3 0f 1e fb             endbr32
 8049244:       eb 8a                   jmp    80491d0 <register_tm_clones>

08049246 <cleanup>:
 8049246:       55                      push   %ebp
 8049247:       89 e5                   mov    %esp,%ebp
 8049249:       83 ec 08                sub    $0x8,%esp
 804924c:       83 7d 08 ff             cmpl   $0xffffffff,0x8(%ebp)
 8049250:       74 0e                   je     8049260 <cleanup+0x1a>
 8049252:       83 ec 0c                sub    $0xc,%esp
 8049255:       ff 75 08                push   0x8(%ebp)
 8049258:       e8 d3 fe ff ff          call   8049130 <close@plt>
 804925d:       83 c4 10                add    $0x10,%esp
 8049260:       90                      nop
 8049261:       c9                      leave
 8049262:       c3                      ret

08049263 <cli_hndl>:
 8049263:       55                      push   %ebp
 8049264:       89 e5                   mov    %esp,%ebp
 8049266:       81 ec 18 02 00 00       sub    $0x218,%esp
 804926c:       eb 19                   jmp    8049287 <cli_hndl+0x24>
 804926e:       8b 45 f4                mov    -0xc(%ebp),%eax
 8049271:       83 ec 04                sub    $0x4,%esp
 8049274:       50                      push   %eax
 8049275:       8d 85 f4 fd ff ff       lea    -0x20c(%ebp),%eax
 804927b:       50                      push   %eax
 804927c:       ff 75 08                push   0x8(%ebp)
 804927f:       e8 4c fe ff ff          call   80490d0 <write@plt>
 8049284:       83 c4 10                add    $0x10,%esp
 8049287:       83 ec 04                sub    $0x4,%esp
 804928a:       68 00 04 00 00          push   $0x400
 804928f:       8d 85 f4 fd ff ff       lea    -0x20c(%ebp),%eax
 8049295:       50                      push   %eax
 8049296:       ff 75 08                push   0x8(%ebp)
 8049299:       e8 b2 fd ff ff          call   8049050 <read@plt>
 804929e:       83 c4 10                add    $0x10,%esp
 80492a1:       89 45 f4                mov    %eax,-0xc(%ebp)
 80492a4:       83 7d f4 00             cmpl   $0x0,-0xc(%ebp)
 80492a8:       7f c4                   jg     804926e <cli_hndl+0xb>
 80492aa:       83 7d f4 ff             cmpl   $0xffffffff,-0xc(%ebp)
 80492ae:       75 10                   jne    80492c0 <cli_hndl+0x5d>
 80492b0:       83 ec 0c                sub    $0xc,%esp
 80492b3:       68 08 a0 04 08          push   $0x804a008
 80492b8:       e8 d3 fd ff ff          call   8049090 <perror@plt>
 80492bd:       83 c4 10                add    $0x10,%esp
 80492c0:       90                      nop
 80492c1:       c9                      leave
 80492c2:       c3                      ret

080492c3 <main>:
 80492c3:       8d 4c 24 04             lea    0x4(%esp),%ecx
 80492c7:       83 e4 f0                and    $0xfffffff0,%esp
 80492ca:       ff 71 fc                push   -0x4(%ecx)
 80492cd:       55                      push   %ebp
 80492ce:       89 e5                   mov    %esp,%ebp
 80492d0:       53                      push   %ebx
 80492d1:       51                      push   %ecx
 80492d2:       83 ec 30                sub    $0x30,%esp
 80492d5:       c7 45 f4 ff ff ff ff    movl   $0xffffffff,-0xc(%ebp)
 80492dc:       c7 45 f0 ff ff ff ff    movl   $0xffffffff,-0x10(%ebp)
 80492e3:       c7 45 e0 00 00 00 00    movl   $0x0,-0x20(%ebp)
 80492ea:       c7 45 e4 00 00 00 00    movl   $0x0,-0x1c(%ebp)
 80492f1:       c7 45 e8 00 00 00 00    movl   $0x0,-0x18(%ebp)
 80492f8:       c7 45 ec 00 00 00 00    movl   $0x0,-0x14(%ebp)
 80492ff:       66 c7 45 e0 02 00       movw   $0x2,-0x20(%ebp)
 8049305:       83 ec 0c                sub    $0xc,%esp
 8049308:       68 61 1e 00 00          push   $0x1e61
 804930d:       e8 6e fd ff ff          call   8049080 <htons@plt>
 8049312:       83 c4 10                add    $0x10,%esp
 8049315:       66 89 45 e2             mov    %ax,-0x1e(%ebp)
 8049319:       c7 45 d0 00 00 00 00    movl   $0x0,-0x30(%ebp)
 8049320:       c7 45 d4 00 00 00 00    movl   $0x0,-0x2c(%ebp)
 8049327:       c7 45 d8 00 00 00 00    movl   $0x0,-0x28(%ebp)
 804932e:       c7 45 dc 00 00 00 00    movl   $0x0,-0x24(%ebp)
 8049335:       c7 45 cc 10 00 00 00    movl   $0x10,-0x34(%ebp)
 804933c:       c7 45 c8 ff e4 00 00    movl   $0xe4ff,-0x38(%ebp)
 8049343:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049348:       50                      push   %eax
 8049349:       6a 21                   push   $0x21
 804934b:       6a 01                   push   $0x1
 804934d:       68 1c a0 04 08          push   $0x804a01c
 8049352:       e8 59 fd ff ff          call   80490b0 <fwrite@plt>
 8049357:       83 c4 10                add    $0x10,%esp
 804935a:       83 ec 04                sub    $0x4,%esp
 804935d:       6a 00                   push   $0x0
 804935f:       6a 01                   push   $0x1
 8049361:       6a 02                   push   $0x2
 8049363:       e8 b8 fd ff ff          call   8049120 <socket@plt>
 8049368:       83 c4 10                add    $0x10,%esp
 804936b:       89 45 f4                mov    %eax,-0xc(%ebp)
 804936e:       83 7d f4 ff             cmpl   $0xffffffff,-0xc(%ebp)
 8049372:       75 3d                   jne    80493b1 <main+0xee>
 8049374:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049379:       50                      push   %eax
 804937a:       6a 0a                   push   $0xa
 804937c:       6a 01                   push   $0x1
 804937e:       68 3e a0 04 08          push   $0x804a03e
 8049383:       e8 28 fd ff ff          call   80490b0 <fwrite@plt>
 8049388:       83 c4 10                add    $0x10,%esp
 804938b:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049390:       83 ec 0c                sub    $0xc,%esp
 8049393:       50                      push   %eax
 8049394:       e8 c7 fc ff ff          call   8049060 <fflush@plt>
 8049399:       83 c4 10                add    $0x10,%esp
 804939c:       83 ec 0c                sub    $0xc,%esp
 804939f:       68 49 a0 04 08          push   $0x804a049
 80493a4:       e8 e7 fc ff ff          call   8049090 <perror@plt>
 80493a9:       83 c4 10                add    $0x10,%esp
 80493ac:       e9 4f 02 00 00          jmp    8049600 <main+0x33d>
 80493b1:       83 ec 0c                sub    $0xc,%esp
 80493b4:       6a 04                   push   $0x4
 80493b6:       8d 45 c8                lea    -0x38(%ebp),%eax
 80493b9:       50                      push   %eax
 80493ba:       6a 02                   push   $0x2
 80493bc:       6a 01                   push   $0x1
 80493be:       ff 75 f4                push   -0xc(%ebp)
 80493c1:       e8 6a fc ff ff          call   8049030 <setsockopt@plt>
 80493c6:       83 c4 20                add    $0x20,%esp
 80493c9:       83 f8 ff                cmp    $0xffffffff,%eax
 80493cc:       75 10                   jne    80493de <main+0x11b>
 80493ce:       83 ec 0c                sub    $0xc,%esp
 80493d1:       68 5e a0 04 08          push   $0x804a05e
 80493d6:       e8 b5 fc ff ff          call   8049090 <perror@plt>
 80493db:       83 c4 10                add    $0x10,%esp
 80493de:       a1 8c b3 04 08          mov    0x804b38c,%eax
 80493e3:       50                      push   %eax
 80493e4:       6a 0a                   push   $0xa
 80493e6:       6a 01                   push   $0x1
 80493e8:       68 77 a0 04 08          push   $0x804a077
 80493ed:       e8 be fc ff ff          call   80490b0 <fwrite@plt>
 80493f2:       83 c4 10                add    $0x10,%esp
 80493f5:       a1 8c b3 04 08          mov    0x804b38c,%eax
 80493fa:       83 ec 0c                sub    $0xc,%esp
 80493fd:       50                      push   %eax
 80493fe:       e8 5d fc ff ff          call   8049060 <fflush@plt>
 8049403:       83 c4 10                add    $0x10,%esp
 8049406:       a1 8c b3 04 08          mov    0x804b38c,%eax
 804940b:       50                      push   %eax
 804940c:       6a 21                   push   $0x21
 804940e:       6a 01                   push   $0x1
 8049410:       68 84 a0 04 08          push   $0x804a084
 8049415:       e8 96 fc ff ff          call   80490b0 <fwrite@plt>
 804941a:       83 c4 10                add    $0x10,%esp
 804941d:       83 ec 04                sub    $0x4,%esp
 8049420:       6a 10                   push   $0x10
 8049422:       8d 45 e0                lea    -0x20(%ebp),%eax
 8049425:       50                      push   %eax
 8049426:       ff 75 f4                push   -0xc(%ebp)
 8049429:       e8 b2 fc ff ff          call   80490e0 <bind@plt>
 804942e:       83 c4 10                add    $0x10,%esp
 8049431:       83 f8 ff                cmp    $0xffffffff,%eax
 8049434:       75 3d                   jne    8049473 <main+0x1b0>
 8049436:       a1 8c b3 04 08          mov    0x804b38c,%eax
 804943b:       50                      push   %eax
 804943c:       6a 0a                   push   $0xa
 804943e:       6a 01                   push   $0x1
 8049440:       68 3e a0 04 08          push   $0x804a03e
 8049445:       e8 66 fc ff ff          call   80490b0 <fwrite@plt>
 804944a:       83 c4 10                add    $0x10,%esp
 804944d:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049452:       83 ec 0c                sub    $0xc,%esp
 8049455:       50                      push   %eax
 8049456:       e8 05 fc ff ff          call   8049060 <fflush@plt>
 804945b:       83 c4 10                add    $0x10,%esp
 804945e:       83 ec 0c                sub    $0xc,%esp
 8049461:       68 a6 a0 04 08          push   $0x804a0a6
 8049466:       e8 25 fc ff ff          call   8049090 <perror@plt>
 804946b:       83 c4 10                add    $0x10,%esp
 804946e:       e9 8d 01 00 00          jmp    8049600 <main+0x33d>
 8049473:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049478:       50                      push   %eax
 8049479:       6a 0a                   push   $0xa
 804947b:       6a 01                   push   $0x1
 804947d:       68 77 a0 04 08          push   $0x804a077
 8049482:       e8 29 fc ff ff          call   80490b0 <fwrite@plt>
 8049487:       83 c4 10                add    $0x10,%esp
 804948a:       a1 8c b3 04 08          mov    0x804b38c,%eax
 804948f:       83 ec 0c                sub    $0xc,%esp
 8049492:       50                      push   %eax
 8049493:       e8 c8 fb ff ff          call   8049060 <fflush@plt>
 8049498:       83 c4 10                add    $0x10,%esp
 804949b:       0f b7 45 e2             movzwl -0x1e(%ebp),%eax
 804949f:       0f b7 c0                movzwl %ax,%eax
 80494a2:       83 ec 0c                sub    $0xc,%esp
 80494a5:       50                      push   %eax
 80494a6:       e8 65 fc ff ff          call   8049110 <ntohs@plt>
 80494ab:       83 c4 10                add    $0x10,%esp
 80494ae:       0f b7 d8                movzwl %ax,%ebx
 80494b1:       83 ec 0c                sub    $0xc,%esp
 80494b4:       ff 75 e4                push   -0x1c(%ebp)
 80494b7:       e8 b4 fb ff ff          call   8049070 <inet_ntoa@plt>
 80494bc:       83 c4 10                add    $0x10,%esp
 80494bf:       8b 15 8c b3 04 08       mov    0x804b38c,%edx
 80494c5:       53                      push   %ebx
 80494c6:       50                      push   %eax
 80494c7:       68 b9 a0 04 08          push   $0x804a0b9
 80494cc:       52                      push   %edx
 80494cd:       e8 ee fb ff ff          call   80490c0 <fprintf@plt>
 80494d2:       83 c4 10                add    $0x10,%esp
 80494d5:       83 ec 08                sub    $0x8,%esp
 80494d8:       6a 01                   push   $0x1
 80494da:       ff 75 f4                push   -0xc(%ebp)
 80494dd:       e8 1e fc ff ff          call   8049100 <listen@plt>
 80494e2:       83 c4 10                add    $0x10,%esp
 80494e5:       83 f8 ff                cmp    $0xffffffff,%eax
 80494e8:       75 3d                   jne    8049527 <main+0x264>
 80494ea:       a1 8c b3 04 08          mov    0x804b38c,%eax
 80494ef:       50                      push   %eax
 80494f0:       6a 0a                   push   $0xa
 80494f2:       6a 01                   push   $0x1
 80494f4:       68 3e a0 04 08          push   $0x804a03e
 80494f9:       e8 b2 fb ff ff          call   80490b0 <fwrite@plt>
 80494fe:       83 c4 10                add    $0x10,%esp
 8049501:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049506:       83 ec 0c                sub    $0xc,%esp
 8049509:       50                      push   %eax
 804950a:       e8 51 fb ff ff          call   8049060 <fflush@plt>
 804950f:       83 c4 10                add    $0x10,%esp
 8049512:       83 ec 0c                sub    $0xc,%esp
 8049515:       68 d5 a0 04 08          push   $0x804a0d5
 804951a:       e8 71 fb ff ff          call   8049090 <perror@plt>
 804951f:       83 c4 10                add    $0x10,%esp
 8049522:       e9 d9 00 00 00          jmp    8049600 <main+0x33d>
 8049527:       a1 8c b3 04 08          mov    0x804b38c,%eax
 804952c:       50                      push   %eax
 804952d:       6a 0a                   push   $0xa
 804952f:       6a 01                   push   $0x1
 8049531:       68 77 a0 04 08          push   $0x804a077
 8049536:       e8 75 fb ff ff          call   80490b0 <fwrite@plt>
 804953b:       83 c4 10                add    $0x10,%esp
 804953e:       a1 8c b3 04 08          mov    0x804b38c,%eax
 8049543:       83 ec 0c                sub    $0xc,%esp
 8049546:       50                      push   %eax
 8049547:       e8 14 fb ff ff          call   8049060 <fflush@plt>
 804954c:       83 c4 10                add    $0x10,%esp
 804954f:       eb 77                   jmp    80495c8 <main+0x305>
 8049551:       0f b7 45 d2             movzwl -0x2e(%ebp),%eax
 8049555:       0f b7 c0                movzwl %ax,%eax
 8049558:       83 ec 0c                sub    $0xc,%esp
 804955b:       50                      push   %eax
 804955c:       e8 af fb ff ff          call   8049110 <ntohs@plt>
 8049561:       83 c4 10                add    $0x10,%esp
 8049564:       0f b7 d8                movzwl %ax,%ebx
 8049567:       83 ec 0c                sub    $0xc,%esp
 804956a:       ff 75 d4                push   -0x2c(%ebp)
 804956d:       e8 fe fa ff ff          call   8049070 <inet_ntoa@plt>
 8049572:       83 c4 10                add    $0x10,%esp
 8049575:       8b 15 8c b3 04 08       mov    0x804b38c,%edx
 804957b:       53                      push   %ebx
 804957c:       50                      push   %eax
 804957d:       68 ec a0 04 08          push   $0x804a0ec
 8049582:       52                      push   %edx
 8049583:       e8 38 fb ff ff          call   80490c0 <fprintf@plt>
 8049588:       83 c4 10                add    $0x10,%esp
 804958b:       83 ec 0c                sub    $0xc,%esp
 804958e:       ff 75 f0                push   -0x10(%ebp)
 8049591:       e8 cd fc ff ff          call   8049263 <cli_hndl>
 8049596:       83 c4 10                add    $0x10,%esp
 8049599:       83 ec 0c                sub    $0xc,%esp
 804959c:       ff 75 f0                push   -0x10(%ebp)
 804959f:       e8 8c fb ff ff          call   8049130 <close@plt>
 80495a4:       83 c4 10                add    $0x10,%esp
 80495a7:       83 ec 04                sub    $0x4,%esp
 80495aa:       6a 10                   push   $0x10
 80495ac:       6a 00                   push   $0x0
 80495ae:       8d 45 d0                lea    -0x30(%ebp),%eax
 80495b1:       50                      push   %eax
 80495b2:       e8 39 fb ff ff          call   80490f0 <memset@plt>
 80495b7:       83 c4 10                add    $0x10,%esp
 80495ba:       c7 45 cc 10 00 00 00    movl   $0x10,-0x34(%ebp)
 80495c1:       c7 45 f0 ff ff ff ff    movl   $0xffffffff,-0x10(%ebp)
 80495c8:       83 ec 04                sub    $0x4,%esp
 80495cb:       8d 45 cc                lea    -0x34(%ebp),%eax
 80495ce:       50                      push   %eax
 80495cf:       8d 45 d0                lea    -0x30(%ebp),%eax
 80495d2:       50                      push   %eax
 80495d3:       ff 75 f4                push   -0xc(%ebp)
 80495d6:       e8 c5 fa ff ff          call   80490a0 <accept@plt>
 80495db:       83 c4 10                add    $0x10,%esp
 80495de:       89 45 f0                mov    %eax,-0x10(%ebp)
 80495e1:       83 7d f0 ff             cmpl   $0xffffffff,-0x10(%ebp)
 80495e5:       0f 85 66 ff ff ff       jne    8049551 <main+0x28e>
 80495eb:       83 ec 0c                sub    $0xc,%esp
 80495ee:       ff 75 f4                push   -0xc(%ebp)
 80495f1:       e8 50 fc ff ff          call   8049246 <cleanup>
 80495f6:       83 c4 10                add    $0x10,%esp
 80495f9:       b8 00 00 00 00          mov    $0x0,%eax
 80495fe:       eb 13                   jmp    8049613 <main+0x350>
 8049600:       83 ec 0c                sub    $0xc,%esp
 8049603:       ff 75 f4                push   -0xc(%ebp)
 8049606:       e8 3b fc ff ff          call   8049246 <cleanup>
 804960b:       83 c4 10                add    $0x10,%esp
 804960e:       b8 01 00 00 00          mov    $0x1,%eax
 8049613:       8d 65 f8                lea    -0x8(%ebp),%esp
 8049616:       59                      pop    %ecx
 8049617:       5b                      pop    %ebx
 8049618:       5d                      pop    %ebp
 8049619:       8d 61 fc                lea    -0x4(%ecx),%esp
 804961c:       c3                      ret

Disassembly of section .fini:

08049620 <_fini>:
 8049620:       53                      push   %ebx
 8049621:       83 ec 08                sub    $0x8,%esp
 8049624:       e8 57 fb ff ff          call   8049180 <__x86.get_pc_thunk.bx>
 8049629:       81 c3 0b 1d 00 00       add    $0x1d0b,%ebx
 804962f:       83 c4 08                add    $0x8,%esp
 8049632:       5b                      pop    %ebx
 8049633:       c3                      ret
```

# A — Interpreting `esrv.c` (plain English + line-by-line of the important parts)

**Plain-English summary:**
`esrv.c` implements a simple TCP echo server (RFC 862): create a listening socket, accept connections, and for each connection read data from the client and write the same bytes back. The bug: `cli_hndl()` allocates a 512-byte stack buffer `buf[BUF_SZ]` but calls `read(..., BUF_LEN)` where `BUF_LEN` is `BUF_SZ<<1` (1,024). That lets an attacker send more bytes than the buffer holds and overflow the stack.

## High-level control flow (main)

1. Build an IPv4/TCP socket: `socket(PF_INET, SOCK_STREAM, 0)`.
2. `setsockopt(..., SO_REUSEADDR, ...)` to reuse address quickly.
3. `bind()` to `0.0.0.0:7777`.
4. `listen()` with small backlog.
5. Loop: `accept()` incoming connection into `cfd` and client addr `cin`.
6. Call `cli_hndl(cfd)` to echo; after it returns, `close(cfd)` and loop.

## `cli_hndl(int cfd)` — important lines

```c
char buf[BUF_SZ];            // BUF_SZ == 512
ssize_t len;

/* while ((len = read(cfd, buf, BUF_LEN)) > 0) { ... } */
```

* `BUF_LEN` is defined as `BUF_SZ<<1` (i.e., 1024). `read()` will copy up to 1024 bytes into a stack buffer that is only 512 bytes long → **stack buffer overflow**.
* If the client sends >512 bytes, the write may overwrite adjacent stack data: saved frame pointer (EBP), saved return address (EIP) on 32-bit, or other local vars — classic return-address overwrite avenue.

### How an exploit would leverage this

* Because the program is compiled with `-m32 -no-pie -fno-pic -z execstack -z norelro` (Makefile), it:

  * Produces a 32-bit non-PIE binary (fixed addresses).
  * Enables an executable stack (`-z execstack`).
  * Disables RELRO protections (`-z norelro`) so GOT/PLT can be more easily abused.
  * Combined with running under `setarch i686 -3 -R` (which disables ASLR), this environment is intentionally made exploit-friendly for teaching.
* An attacker can overflow `buf` to smash saved EIP and redirect execution (return-to-stack shellcode or return-to-libc depending on environment).

# B — How to read the `readelf -e esrv` output you pasted

I’ll map important `readelf` lines to meaning and to what we care about for exploitation/analysis.

## ELF Header (top of output)

```
Class: ELF32        -> 32-bit binary
Data: little endian
Type: EXEC          -> Non-PIE executable
Machine: Intel 80386
Entry point address: 0x8049140
Start of program headers: 52
Start of section headers: 82380
Number of program headers: 10
Number of section headers: 36
```

* **Entry point** is where execution begins (after loader handles dynamic linking). For exploit work, `Entry point` is useful but you more often want addresses of `.text`, `main`, or functions.
* `ELF32` + `Type: EXEC` + compiler flags means fixed code addresses (no PIE).

## Section Headers table

Shows `.text`, `.data`, `.rodata`, `.bss`, etc. Each section has:

* `Name`, `Addr` (virtual address), `Off` (file offset), `Size`, flags.
  Example from your output:

```
[13] .text   Addr 08049140  Off 001140  Size 0004dd  Flg: AX
[23] .data   Addr 0804b384  Off 002384  Size 000008  Flg: WA
[24] .bss    Addr 0804b38c  Off 00238c  Size 000008  Flg: WA (NOBITS)
```

* `.text` contains code; `.data` writable initialized globals; `.bss` uninitialized data (no file space).
* Offsets are where those sections reside inside the file.

> Note: section headers are mostly a linking-level convenience. When the program runs, the OS cares about *segments* (program headers), not individual sections.

## Program Headers (Segments)

Program headers are the loader’s view. Example lines:

```
Type    Offset   VirtAddr   FileSiz  MemSiz  Flg
LOAD    0x000000 0x08048000 0x004f4  0x004f4  R
LOAD    0x001000 0x08049000 0x00634  0x00634  R E
...
GNU_STACK  ...  RWE
```

* `LOAD` segments are mapped to memory by the kernel (with protection bits from `Flg`).
* The `R E` segment at `0x08049000` contains `.text` and is executable.
* `GNU_STACK` indicates stack permission bits; `RWE` means the binary requests an executable stack (bad from a security standpoint) — that comes from `-z execstack`.

## Interpreter

```
[Requesting program interpreter: /lib/ld-linux.so.2]
```

* Dynamic linker is used (dynamic linking present). Look at `.dyn`, `.got.plt`, `.rel.plt` if you want to do GOT/PLT based attacks.

## Section-to-Segment mapping

At the bottom `Section to Segment mapping` shows which sections land in which LOAD segment. E.g. `.text` in LOAD segment 03, `.data` and `.bss` in LOAD segment 05.

## What the Makefile flags show up as

* `-m32` → ELF32 (you already saw ELF32).
* `-no-pie` / `-fno-pic` → addresses in ELF are absolute and not position independent.
* `-z execstack` → `GNU_STACK` segment will be executable (readelf shows `RWE`).
* `-z norelro` → disables RELRO protections; readelf won’t explicitly say “no RELRO”, but you can check for `GNU_RELRO` and whether `.got` is read-only after relocation. (Tools like `checksec` summarize this; but you can infer from LDFLAGS and presence/absence of `GNU_RELRO`.)

# C — Fixes and code examples

We’ll provide two fixes: a **simple** quick fix and an **improved** robust variant.

## Example 1 — simple, minimal fix (correct the call)

Replace `BUF_LEN` with `BUF_SZ` (or better `sizeof buf`) when calling `read`:

```c
/* minimal safe change inside cli_hndl */
while ((len = read(cfd, buf, sizeof(buf))) > 0) {
    if (len > 0) {
        ssize_t wrote = 0, off = 0;
        while (off < len) {
            wrote = write(cfd, buf + off, len - off);
            if (wrote == -1) { perror("write"); break; }
            off += wrote;
        }
    }
}
```

Line-by-line:

* `sizeof(buf)` guarantees the read can never overflow `buf`.
* The inner `write` loop handles short writes.

**Why it matters:** stops stack overflow by bounding reads to actual buffer size.

**Pitfall:** still uses `read()` which returns byte count; if you want to support textual protocols, you might prefer line-buffered handling. Also this does not authenticate inputs or handle extremely long streams gracefully (it just processes in chunks).

## Example 2 — robust, safer server (using `recv` with explicit bounds and loop)

```c
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>

#define BUF_SZ 512

static void cli_hndl(int cfd) {
    char buf[BUF_SZ];
    ssize_t len;

    for (;;) {
        len = recv(cfd, buf, sizeof(buf), 0);
        if (len == 0) { /* peer closed */ break; }
        if (len == -1) {
            if (errno == EINTR) continue;
            perror("recv");
            break;
        }
        ssize_t off = 0;
        while (off < len) {
            ssize_t w = send(cfd, buf + off, len - off, 0);
            if (w == -1) {
                if (errno == EINTR) continue;
                perror("send");
                goto done;
            }
            off += w;
        }
    }
done:
    return;
}
```

Why this is better:

* `recv/send` for socket semantics (can set flags later).
* Handles `EINTR`.
* No overflow (buffer size used everywhere).
* Easier to add timeouts, non-blocking, limits per-connection, etc.

# D — Useful inspection commands and what they tell you

Run these in your environment. I’ll give the commands and what to expect:

* `readelf -h esrv` → ELF header (class, type, entry).
* `readelf -l esrv` → Program headers / segments.
* `readelf -S esrv` → Section headers table (shows `.text`, `.data`, etc).
* `readelf -r esrv` → Relocations (useful for GOT/PLT).
* `readelf -s esrv` → Dynamic/global symbols.
* `objdump -d esrv | less` → Disassembly of `.text`. Use `objdump -D` to disassemble all.
* `nm -n esrv` → symbols sorted by address. Useful to find `main` address (if not stripped).
* `strings esrv | less` → literal strings; can reveal messages and interpreter string.
* `ldd esrv` → which shared libraries will be loaded at runtime (dynamic).
* `file esrv` → quick summary (ELF 32-bit LSB executable, etc).
* `size esrv` → text/data/bss sizes.

**Security checks** (quick heuristics):

* `readelf -l esrv` and look for `GNU_STACK` permissions: `RWE` means executable stack allowed.
* `readelf -S esrv` check for `.got.plt` and `GNU_RELRO` section presence/absence.
* `objdump -d` and `nm` to find useful gadgets or function addresses.

# E — Analogy to build intuition

Think of the program stack frame as a stack of labeled boxes:

* `buf[512]` is a box of size 512 bytes near the top.
* Saved frame pointer and return address are boxes below it.
* `read(cfd, buf, 1024)` is like pouring 1024 ml of liquid into a 512 ml box — the overflow spills into the boxes below (saved EIP), letting an attacker change the label (return address) so the function returns where the attacker wants.

# F — Common pitfalls & things to watch

* **Assuming `read()` returns full requested bytes.** It may return less; always handle partial reads/writes.
* **Using constants instead of `sizeof`.** Automatically wrong after refactors; use `sizeof(buf)`.
* **Disabling security features in Makefile for production** (`-z execstack`, `-z norelro`, `-no-pie`) — those flags are educational/deliberate for exploitation exercises and must not be used in production.
* **Confusing section addresses vs. runtime mappings.** The kernel maps segments. Sections are used by the linker and debugger.

# G — Short summary (key takeaways)

* `esrv.c` is a simple echo server with a **stack-based buffer overflow**: `buf[512]` + `read(..., 1024)` causes overflow.
* The Makefile purposely builds an exploit-friendly binary (32-bit, no PIE, executable stack).
* Read `readelf -e` by first reading ELF header, then program headers (what the loader maps), then section headers (linker-level). Look for `GNU_STACK`, interpreter (`/lib/ld-linux.so.2`), `.text`, `.data`, `.bss`, and relocation sections.
* Fix by bounding reads to `sizeof(buf)` and handling partial reads/writes; for robust code, use `recv`/`send` with proper error handling and consider connection-level limits.

# H — Two practice questions / mini exercises

1. **Find the exact stack layout**: compile `esrv` with debugging (`-g`) and run under `gdb` (with the same run environment used by Makefile). Put a breakpoint at the start of `cli_hndl`, then examine the saved EIP and offsets: `info frame`, `x/200xb $esp` after reading a 700-byte string from a client. Report which bytes overwrite the saved EIP. (This practices mapping overflow length → return address overwrite.)
2. **Patch and test**: change `cli_hndl()` to use the robust `recv` loop above. Recompile and verify `readelf -l` still shows `GNU_STACK` RWE (because of LDFLAGS), but confirm your program no longer crashes when you send 2KB of data (it should echo only in 512-byte chunks).

