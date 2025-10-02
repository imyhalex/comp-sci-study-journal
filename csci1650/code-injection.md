# Code injection — plain-English intro

**What it is:** *Code injection* is a class of vulnerabilities where an attacker supplies data that your program treats as executable code (or as commands), causing that attacker-controlled input to run. Common forms include SQL injection, command injection, format-string/printf injection, dynamic code eval injection, and unsafe deserialization.

**Big picture:** attackers exploit any place your program *mixes data with code/commands* without proper separation. The result can be data theft, privilege escalation, remote code execution, or denial of service.

---

## 1) Simple example — command injection in C (vulnerable → fixed)

### Vulnerable (simple)

```c
// vuln_cmd.c  (vulnerable)
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char filename[256];
    printf("Enter file to list: ");
    if (fgets(filename, sizeof filename, stdin) == NULL) return 1;
    // strip newline
    size_t n = strlen(filename);
    if (n && filename[n-1] == '\n') filename[n-1] = '\0';

    // BAD: passing user input directly into system() builds a shell command
    char cmd[512];
    snprintf(cmd, sizeof cmd, "ls -l %s", filename);
    system(cmd);
    return 0;
}
```

**Walkthrough (line-by-line):**

* reads a filename from stdin into `filename`.
* constructs a command string `cmd` by concatenating `"ls -l "` and user input.
* calls `system(cmd)` which invokes a shell to run `cmd`.
* If the user supplies something like `mydir; rm -rf /tmp/somewhere` (don't try this), the shell executes both `ls -l mydir` and the `rm` command — that’s the injection.

### Fixed (safe) approaches

Option A — avoid shell, use `execve`/`fork` with an argv array:

```c
// fixed_cmd.c (safer)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // fork, execvp

int main(void) {
    char filename[256];
    printf("Enter file to list: ");
    if (!fgets(filename, sizeof filename, stdin)) return 1;
    size_t n = strlen(filename);
    if (n && filename[n-1] == '\n') filename[n-1] = '\0';

    // Validate/sanitize filename: allow only a-zA-Z0-9._-/ chars (example)
    for (char *p = filename; *p; ++p) {
        if (!((*p>='a' && *p<='z') || (*p>='A' && *p<='Z') ||
              (*p>='0' && *p<='9') || *p=='_' || *p=='.' || *p=='/' || *p=='-')) {
            fprintf(stderr, "Invalid character in filename\n");
            return 1;
        }
    }

    // Avoid shell: use execlp/execvp so arguments are not re-parsed by a shell
    pid_t pid = fork();
    if (pid == 0) {
        execlp("ls", "ls", "-l", filename, (char*)NULL);
        _exit(127); // exec failed
    } else if (pid > 0) {
        int status;
        waitpid(pid, &status, 0);
    } else {
        perror("fork");
    }
    return 0;
}
```

**Why this fixes it:** `exec` family passes argument vectors directly to the kernel; no shell interpretation means operators like `;` don't create extra commands. Also validating allowed chars reduces dangerous input.

---

## 2) Advanced example — SQL injection (PHP + parameterized query)

### Vulnerable PHP snippet (conceptual)

```php
// vuln_sql.php (vulnerable)
$username = $_GET['user'];
$query = "SELECT id FROM users WHERE username = '$username'"; // <-- direct interpolation
$result = mysqli_query($conn, $query);
```

If `username` contains `' OR '1'='1`, it changes the meaning of the query.

### Fixed (prepared statement)

```php
// fixed_sql.php (safer)
$username = $_GET['user'];
$stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();
```

**Line-by-line:** Prepared statements keep data and SQL separate; the DB treats `?` as a placeholder and binds literal data, so injected SQL fragments are treated as data, not SQL code.

---

## 3) Other injection types — short overview + safe patterns

* **Format-string injection (C):** calling `printf(user_input)` is dangerous because format specifiers in `user_input` are interpreted. Always use `printf("%s", user_input)` or better `fputs`/`fwrite`.
* **Dynamic code eval (JS/Python):** `eval(user_input)` is risky. Prefer parsing, restricted interpreters, or explicit APIs.
* **Unsafe deserialization:** loading attacker-controlled serialized objects can instantiate unexpected classes. Use strict schemas, versioning, or avoid object deserialization where possible.
* **Template injection:** user data injected into server templates that support expressions can run code — escape or sandbox template contexts.

---

## 4) Why this matters (real-world impact)

* Attackers can read, modify, or delete data (SQLi), run arbitrary shell commands (command injection), escalate privileges, pivot to other systems, or install malware.
* Many historical major breaches were enabled by injection flaws.
* Injection bugs are often easy to introduce (string concatenation) and can be catastrophic.

---

## 5) Common pitfalls & how to avoid them

* **Pitfall:** “I only use `system()` on local code — it's safe.”
  **Fix:** Local inputs can be attacker-controlled (e.g., from network, files, or other processes). Treat all inputs as untrusted.
* **Pitfall:** “Escaping is enough.”
  **Fix:** Manual escaping is error-prone. Prefer parameterized APIs or API functions that avoid interpretation (e.g., `execv` vs `system`).
* **Pitfall:** “I sanitize with a blacklist.”
  **Fix:** Blacklists miss edge cases. Use allowlists (whitelists) — define and allow only expected characters/values.
* **Pitfall:** Mixing data and code at many layers — UI, templates, DB, shell.
  **Fix:** Maintain a policy: separate data from code at every boundary.

---

## 6) Concrete defensive checklist (practical)

1. **Principle of least privilege:** run services with minimal permissions.
2. **Use parameterized queries / prepared statements** for DB access.
3. **Avoid invoking the shell**; use `execve`/`posix_spawn`/`CreateProcess` with argv lists.
4. **Escape outputs** (contextual escaping: HTML, JS, SQL, shell, JSON, etc.) when data flows into a different context.
5. **Validate with allowlists** (e.g., filenames only containing `[A-Za-z0-9._-/]`).
6. **Use safe APIs** (e.g., `snprintf` with size limits; `fgets` not `gets`).
7. **Static analysis and fuzzing** — automated tools catch classes of injection flaws.
8. **Code review & threat modeling** — review every spot where input crosses a trust boundary.

---

## 7) Analogy / diagram (intuition)

Imagine your program is a kitchen and `system()` is a chef who interprets spoken instructions. If you hand the chef a string that was “typed” by a stranger, and the chef executes every sentence literally, that stranger could say “chop onions; set fire to the stove.” Proper separation is like handing the chef a clean, parsed list of ingredients and actions (argv), or better, using a prebuilt appliance that only accepts safe commands — no freeform speech.

---

## 8) Summary — key takeaways

* **Code injection** happens when untrusted data is interpreted as code/commands.
* **Never mix data with code** — use APIs that separate them (prepared statements, exec with argv, safe template APIs).
* **Validate with whitelists**, prefer least privilege, and use contextual escaping when necessary.
* **Review and test**: code reviews, static analyzers, and fuzzers help find injection bugs before production.

---

## 9) Practice questions / mini-exercises

1. Given this C snippet, identify the injection risk and fix it:

   ```c
   char buf[128];
   gets(buf);
   printf(buf);
   ```
2. Write a small C program that lists files under a directory supplied by the user but safely — do **not** use `system()` or `popen()`. Include input validation and explain each defensive choice.

If you want, I can:

* Provide full solutions for the exercises above, or
* Run a vulnerability checklist on a code snippet you paste (I’ll point out injection risks and give fixes). Which would you like next?


# 