# Complete Guide to SSH Keys for GitLab

This guide walks you through the entire process of setting up SSH keys for GitLab, from checking existing keys to generating new ones, adding them to GitLab, and configuring your repository to use them.

## Table of Contents
- [Check for Existing SSH Keys](#check-for-existing-ssh-keys)
- [Generate a New SSH Key](#generate-a-new-ssh-key)
- [Add Your SSH Key to the SSH Agent](#add-your-ssh-key-to-the-ssh-agent)
- [Add Your SSH Key to GitLab](#add-your-ssh-key-to-gitlab)
- [Test Your SSH Connection](#test-your-ssh-connection)
- [Configure Git Repository to Use SSH](#configure-git-repository-to-use-ssh)
- [Troubleshooting](#troubleshooting)

## Check for Existing SSH Keys

Before generating a new SSH key, check if you already have one:

```bash
# List all existing SSH keys
ls -la ~/.ssh/

# Look for files named:
# - id_rsa and id_rsa.pub
# - id_ed25519 and id_ed25519.pub
# - id_ed25519_gitlab and id_ed25519_gitlab.pub
```

If you see `.pub` files like those listed above, you already have SSH keys. You can either use an existing key or generate a new one.

## Generate a New SSH Key

If you don't have an SSH key or want to create a new one specifically for GitLab:

```bash
# Generate a new ED25519 key (recommended)
ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519_gitlab

# OR generate an RSA key (alternative, less secure but more compatible)
# ssh-keygen -t rsa -b 4096 -C "your.email@example.com" -f ~/.ssh/id_rsa_gitlab
```

During the process:
1. You'll be asked to enter a passphrase (recommended for security).
2. Two files will be generated:
   - Private key: `~/.ssh/id_ed25519_gitlab` (keep this secure and never share)
   - Public key: `~/.ssh/id_ed25519_gitlab.pub` (this is what you'll add to GitLab)

## Add Your SSH Key to the SSH Agent

The SSH agent manages your keys and remembers your passphrase:

```bash
# Start the SSH agent in the background
eval "$(ssh-agent -s)"

# Add your private key to the SSH agent
ssh-add ~/.ssh/id_ed25519_gitlab
```

For persistence across terminal sessions, you can add this to your shell's startup file:

```bash
# For bash, add to ~/.bashrc or ~/.bash_profile
echo 'eval "$(ssh-agent -s)"' >> ~/.bashrc
echo 'ssh-add ~/.ssh/id_ed25519_gitlab' >> ~/.bashrc

# For zsh, add to ~/.zshrc
echo 'eval "$(ssh-agent -s)"' >> ~/.zshrc
echo 'ssh-add ~/.ssh/id_ed25519_gitlab' >> ~/.zshrc
```

## Add Your SSH Key to GitLab

1. Copy your public key to the clipboard:

```bash
# Linux
cat ~/.ssh/id_ed25519_gitlab.pub | xclip -selection clipboard

# macOS
cat ~/.ssh/id_ed25519_gitlab.pub | pbcopy

# Windows (Git Bash or WSL)
cat ~/.ssh/id_ed25519_gitlab.pub | clip

# Alternatively, just display it and copy manually
cat ~/.ssh/id_ed25519_gitlab.pub
```

2. Add the key to your GitLab account:

   a. Log in to GitLab
   
   b. Click on your profile icon in the top-right corner
   
   c. Select "Preferences"
   
   d. In the left sidebar, click "SSH Keys"
   
   e. Paste your public key in the "Key" field
   
   f. Give it a title (e.g., "Work Laptop" or "Personal Computer")
   
   g. Click "Add key"

## Test Your SSH Connection

Verify that your SSH key is working with GitLab:

```bash
# Test SSH connection to GitLab
ssh -T git@gitlab.com
```

You should see a message like:
```
Welcome to GitLab, @username!
```

If this is your first time connecting, you'll be asked to confirm the authenticity of the host. Type "yes" to continue.

## Configure Git Repository to Use SSH

If you have an existing repository using HTTPS, change it to use SSH:

```bash
# Check current remote URL
git remote -v

# Should show something like:
# origin https://gitlab.com/chatbook/chatbook-backend.git (fetch)
# origin https://gitlab.com/chatbook/chatbook-backend.git (push)

# Change remote URL from HTTPS to SSH
git remote set-url origin git@gitlab.com:chatbook/chatbook-backend.git

# Verify the change
git remote -v

# Should now show:
# origin git@gitlab.com:chatbook/chatbook-backend.git (fetch)
# origin git@gitlab.com:chatbook/chatbook-backend.git (push)
```

If you're cloning a new repository, use the SSH URL:

```bash
# Clone using SSH
git clone git@gitlab.com:chatbook/chatbook-backend.git
```

## Create SSH Config File (Optional but Recommended)

You can create an SSH config file to manage multiple SSH keys and hosts:

```bash
# Create or edit the SSH config file
nano ~/.ssh/config
```

Add the following content:

```
# GitLab.com
Host gitlab.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_ed25519_gitlab

# You can add other hosts like GitHub or company GitLab instances
# Host github.com
#   PreferredAuthentications publickey
#   IdentityFile ~/.ssh/id_ed25519_github
```

This configures SSH to automatically use the correct key for each host.

## Troubleshooting

### Permission Denied Issues

If you see "Permission denied (publickey)" errors:

1. Ensure your SSH key is added to the SSH agent:
```bash
ssh-add -l
```

2. If it's not listed, add it:
```bash
ssh-add ~/.ssh/id_ed25519_gitlab
```

3. Check that your public key is correctly added to GitLab

### Multiple Keys Management

If you're using multiple SSH keys for different services:

1. Use different key filenames (e.g., `id_ed25519_gitlab`, `id_ed25519_github`)
2. Configure the SSH config file as shown above
3. Test specific configurations:
```bash
ssh -T git@gitlab.com -i ~/.ssh/id_ed25519_gitlab
```

### Debug Connection Issues

For debugging SSH connection issues:

```bash
# Verbose mode shows detailed connection information
ssh -vT git@gitlab.com
```

### Passphrase Issues

If you don't want to enter your passphrase every time:

1. Consider using the SSH agent as described above
2. For persistent management, look into tools like `keychain` or `ssh-agent` managers

---

With this guide, you should be able to fully set up and use SSH authentication with GitLab, making your Git operations more secure and convenient. 