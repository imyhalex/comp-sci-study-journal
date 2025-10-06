In Linux, the **`nm`** command is used to **inspect symbol tables** in object files, libraries, and executables.

### In simple terms:

`nm` shows you **which functions and variables** are defined or referenced inside a compiled binary (like `.o`, `.a`, or executable files).

---

### Basic Usage

```bash
nm filename
```

This lists the symbols in the given file.

---

### Example

If you have a compiled object file:

```bash
gcc -c hello.c
nm hello.o
```

You might see output like:

```
0000000000000000 T main
                 U printf
```

**Explanation:**

* `T main` → `main` is defined in the **text (code)** section of this file.
* `U printf` → `printf` is **undefined here**, meaning it’s referenced but defined elsewhere (like in the C standard library).

---

### Common Symbol Types

| Symbol | Meaning                                                        |
| ------ | -------------------------------------------------------------- |
| `T`    | Function or symbol in the **text/code** section (defined here) |
| `U`    | **Undefined** symbol (referenced but not defined here)         |
| `B`    | Symbol in the **BSS** section (uninitialized global variable)  |
| `D`    | Symbol in the **data** section (initialized global variable)   |
| `R`    | Read-only data section                                         |
| `W`    | Weak symbol (can be overridden)                                |
| `N`    | Debugging symbol (if not stripped)                             |

---

###  Useful Options

* `-C` → Demangle C++ symbols (make them human-readable)
* `-g` → Display only external (global) symbols
* `-n` or `--numeric-sort` → Sort by address
* `-A` → Show filename before each symbol
* `--defined-only` → Show only symbols defined in the file

Example:

```bash
nm -C --defined-only libexample.a
```

---

### Typical Use Cases

* Debugging linking errors (`undefined reference to ...`)
* Inspecting which symbols are exported by a library
* Reverse-engineering or analyzing binaries
* Checking if a function or variable exists in a compiled file

---

Would you like me to show an example of how to use `nm` to debug a **“undefined reference” linker error**?
