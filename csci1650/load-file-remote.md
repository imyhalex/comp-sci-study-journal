## 1. Where you are right now

* On your **local machine** (your shell prompt looks like this):

  ```
  imyhalex@yAshiroharA:~/csci1650$
  ```

  You have files like:

  ```
  cs1650-login.txt  l05  l05.tar.gz  l05.tar.gz:Zone.Identifier  l07.tar.gz  l07.tar.gz:Zone.Identifier
  ```

* Then you ran:

  ```bash
  ssh ysheng21@ssh.cs.brown.edu -t host=@depool
  ```

  After the forwarding dance, you landed on:

  ```
  debpool09 ~ $
  ```

  That is **your remote Brown CS debpool environment**.

Right now you are in two different machines:

* **Local**: your personal computer (`AshiroharA`).
* **Remote**: Brown’s `debpool09` environment.

---

## 2. How to get the tar file into the remote environment

SSH alone does not copy files. You need to use **scp** (secure copy) or **rsync**.

For example, from your **local shell** (`imyhalex@yAshiroharA:~/csci1650$`), run:

```bash
scp l05.tar.gz ysheng21@ssh.cs.brown.edu:~
```

Explanation:

* `scp` = secure copy.
* `l05.tar.gz` = your file.
* `ysheng21@ssh.cs.brown.edu:~` = copy into your home directory on the Brown CS cluster.

Now when you SSH into `ssh.cs.brown.edu` and forward to `debpool09`, you should see `l05.tar.gz` sitting in your home directory (`debpool09 ~ $ ls`).

---

## 3. Extracting the tarball on the remote side

Once the file is on `debpool09`, unpack it:

```bash
tar -xvzf l05.tar.gz
```

* `x` = extract
* `v` = verbose (show files)
* `z` = gzip
* `f` = filename

This will create a folder (`l05`) in your current directory on `debpool09`.

---

## 4. Common pitfalls

* **If `scp` gives “permission denied”**: make sure you’re running `scp` from **local**, not inside the remote shell.
* **If you already logged in to `debpool09`**, open a new terminal and run `scp` from your computer.
* **The `Zone.Identifier` files** come from Windows or WSL. Ignore them — they’re metadata about where the file was downloaded. Just copy `l05.tar.gz` and `l07.tar.gz`.

---

So the workflow is:

1. On your local machine:

   ```bash
   cd ~/csci1650
   scp l05.tar.gz l07.tar.gz ysheng21@ssh.cs.brown.edu:~
   ```

2. SSH in:

   ```bash
   ssh ysheng21@ssh.cs.brown.edu -t host=@depool
   ```

3. On `debpool09`:

   ```bash
   ls
   tar -xvzf l05.tar.gz
   tar -xvzf l07.tar.gz
   ```