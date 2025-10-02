### 1️⃣ Splitting Inside a Single Terminal (with `tmux` or `screen`)

#### Using `tmux`:

1. Install it:

   ```bash
   sudo apt install tmux        # Debian/Ubuntu
   sudo dnf install tmux        # Fedora
   ```
2. Start it:

   ```bash
   tmux
   ```
3. Split horizontally:
   Press `Ctrl + b` then `%`
4. Split vertically:
   Press `Ctrl + b` then `"`
5. Switch between panes:
   `Ctrl + b` then arrow keys
6. Exit tmux:
   Type `exit` in each pane or `Ctrl + b` then `:` and type `kill-session`

#### Using `screen`:

* `Ctrl + a` then `|` → vertical split
* `Ctrl + a` then `S` → horizontal split
* (But `tmux` is much more modern.)

---

### 2️⃣ Splitting the Terminal Window in a GUI

If you’re using a graphical terminal emulator (like GNOME Terminal, Konsole, Tilix):

* **GNOME Terminal:** `Ctrl + Shift + O` (split horizontally), `Ctrl + Shift + E` (split vertically)
* **Tilix (a tiling terminal):** Right-click → “Split Terminal” or use `Ctrl + Shift + O` / `Ctrl + Shift + E`
* **Konsole:** `Ctrl + Shift + ` (split horizontally) and `Ctrl + Shift + )` (split vertically)

---

### 3️⃣ Opening Multiple Tabs/Windows

If splitting isn’t available, you can just open multiple terminal windows or tabs in your emulator.


### 🟢 If you’re using **`tmux`**:

* **Switch panes**:
  `Ctrl + b` then arrow keys (← ↑ ↓ →)
  Example: `Ctrl + b`, then → moves to the right pane.
* **Cycle through panes**:
  `Ctrl + b` then `o`
* **Swap panes** (move their positions):
  `Ctrl + b` then `{` (swap with previous)
  `Ctrl + b` then `}` (swap with next)

---

### 🟢 If you’re using **GNOME Terminal / Tilix / Konsole splits**:

* Usually `Alt + Arrow keys` (← ↑ ↓ →) to jump between split panes.
* Or just click with your mouse into the pane.

---

### 🟢 If you’re using **GNU Screen**:

* `Ctrl + a` then **Tab** → switch between split panes.
