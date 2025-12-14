# GitHub Push Guide - SphereRyder Password Manager

## 🔐 CRITICAL SECURITY NOTICE

**NEVER use your GitHub password directly for HTTPS operations!**

GitHub deprecated password authentication. You MUST use one of these methods:
1. Personal Access Token (Recommended for beginners)
2. SSH Key (Recommended for advanced users)

---

## Method 1: Personal Access Token (PAT) - RECOMMENDED

### Step 1: Create a Personal Access Token

1. **Go to GitHub.com** and log in with your account
2. Click your **profile picture** (top right) → **Settings**
3. Scroll to the bottom of the left sidebar → **Developer settings**
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**

6. **Configure your token:**
   - **Note**: "Password Manager Push Access"
   - **Expiration**: Select "90 days" (or your preference)
   - **Scopes**: Check these boxes:
     - ✅ `repo` (Full control of private repositories)
       - This includes all sub-items

7. Scroll down and click **Generate token**

8. **CRITICAL**: Copy the token immediately!
   ```
   Example: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   - You won't see it again!
   - Save it in a secure location temporarily

### Step 2: Initialize Git Repository

Open Command Prompt or PowerShell in your project directory:

```bash
# Navigate to your project
cd C:\DRyder\Python-Week2\Password_Manager_Claudev1

# Initialize git (if not already done)
git init

# Check current status
git status
```

### Step 3: Stage All Files

```bash
# Add all files to git
git add .

# Verify what will be committed
git status

# You should see all your files in green
```

### Step 4: Create Initial Commit

```bash
# Create your first commit
git commit -m "Initial commit: SphereRyder Password Manager v1.0

- AES-256-GCM encryption implementation
- PBKDF2 key derivation (480,000 iterations)
- Multi-user support with bcrypt authentication
- CLI and Streamlit web interfaces
- Comprehensive Jupyter notebook tutorial
- Pre-configured test accounts"

# Verify commit was created
git log --oneline
```

### Step 5: Add GitHub Remote

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/virtualryder/Password_Manager.git

# Verify remote was added correctly
git remote -v

# Expected output:
# origin  https://github.com/virtualryder/Password_Manager.git (fetch)
# origin  https://github.com/virtualryder/Password_Manager.git (push)
```

### Step 6: Rename Branch to 'main' (if needed)

```bash
# Check current branch name
git branch

# If it shows 'master', rename to 'main'
git branch -M main

# Verify
git branch
```

### Step 7: Push to GitHub

```bash
# Push your code to GitHub
git push -u origin main
```

**When prompted for credentials:**
```
Username: virtualryder
Password: [PASTE YOUR PERSONAL ACCESS TOKEN HERE - NOT YOUR GITHUB PASSWORD]
```

**Example:**
```
Username for 'https://github.com': virtualryder
Password for 'https://virtualryder@github.com': ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 8: Verify on GitHub

1. Go to https://github.com/virtualryder/Password_Manager
2. You should see all your files!
3. Check that the README.md displays correctly

---

## Method 2: SSH Key Authentication (Advanced)

### Why SSH?
- More secure than HTTPS
- No need to enter credentials repeatedly
- Industry best practice

### Step 1: Generate SSH Key

```bash
# Open Command Prompt or PowerShell
# Generate new SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter to accept default location
# Enter a passphrase (recommended) or press Enter for no passphrase
```

**Output:**
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\YourName/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\YourName/.ssh/id_ed25519
Your public key has been saved in C:\Users\YourName/.ssh/id_ed25519.pub
```

### Step 2: Copy Your Public Key

**On Windows (Command Prompt):**
```bash
type %USERPROFILE%\.ssh\id_ed25519.pub
```

**On Windows (PowerShell):**
```bash
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

**Copy the entire output** (starts with `ssh-ed25519`)

### Step 3: Add SSH Key to GitHub

1. Go to GitHub.com → **Settings**
2. Click **SSH and GPG keys** (left sidebar)
3. Click **New SSH key**
4. **Title**: "Password Manager Development - Windows 11"
5. **Key type**: Authentication Key
6. **Key**: Paste your public key
7. Click **Add SSH key**

### Step 4: Test SSH Connection

```bash
# Test connection to GitHub
ssh -T git@github.com

# Expected output:
# Hi virtualryder! You've successfully authenticated, but GitHub does not provide shell access.
```

### Step 5: Change Remote URL to SSH

```bash
# If you already added HTTPS remote, change it to SSH
git remote set-url origin git@github.com:virtualryder/Password_Manager.git

# Verify
git remote -v

# Expected output:
# origin  git@github.com:virtualryder/Password_Manager.git (fetch)
# origin  git@github.com:virtualryder/Password_Manager.git (push)
```

### Step 6: Push to GitHub

```bash
# Push without needing to enter credentials
git push -u origin main
```

---

## Common Git Commands

### Making Updates

```bash
# After making changes to files

# 1. Check what changed
git status

# 2. Stage changes
git add .

# 3. Commit with a message
git commit -m "Updated password generation algorithm"

# 4. Push to GitHub
git push
```

### Viewing History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log -5
```

### Checking Status

```bash
# See current status
git status

# See differences in files
git diff

# See staged differences
git diff --staged
```

### Creating Branches

```bash
# Create and switch to new branch
git checkout -b feature/new-encryption

# List all branches
git branch

# Switch between branches
git checkout main
git checkout feature/new-encryption

# Merge branch into main
git checkout main
git merge feature/new-encryption

# Push new branch to GitHub
git push -u origin feature/new-encryption
```

---

## Troubleshooting

### Error: "Authentication failed"

**Problem**: Using GitHub password instead of token

**Solution**: 
1. Use Personal Access Token instead of password
2. Or switch to SSH authentication

### Error: "remote: Repository not found"

**Problem**: Repository doesn't exist or wrong URL

**Solution**:
```bash
# Verify remote URL
git remote -v

# Correct URL format:
# HTTPS: https://github.com/virtualryder/Password_Manager.git
# SSH:   git@github.com:virtualryder/Password_Manager.git
```

### Error: "Updates were rejected"

**Problem**: Remote has changes you don't have locally

**Solution**:
```bash
# Pull changes first
git pull origin main

# Resolve any conflicts, then push
git push
```

### Error: "fatal: not a git repository"

**Problem**: Not in a git repository

**Solution**:
```bash
# Initialize git
git init
```

### Personal Access Token Expired

**Problem**: Token expired after 90 days

**Solution**:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click on your token
3. Click "Regenerate token"
4. Copy new token and use it for authentication

---

## Security Best Practices

### ✅ DO:
- Use Personal Access Tokens with minimal required scopes
- Set expiration dates on tokens
- Use SSH keys with passphrases
- Keep your `.gitignore` file updated
- Review changes before committing (`git status`, `git diff`)
- Use meaningful commit messages

### ❌ DON'T:
- Never commit your `data/` directory (it's in .gitignore)
- Never commit passwords or API keys
- Never share your Personal Access Token
- Never commit SSH private keys
- Never use your GitHub password for git operations

---

## Verification Checklist

After pushing to GitHub, verify:

- [ ] All code files are present
- [ ] README.md displays correctly
- [ ] No sensitive data was committed (check for `data/` folder)
- [ ] `.gitignore` is working (data folder should not be visible)
- [ ] Requirements.txt is present
- [ ] Documentation files are readable
- [ ] Jupyter notebook is accessible

---

## Need Help?

If you encounter issues:

1. Check the error message carefully
2. Review this guide's troubleshooting section
3. Search for the error on Google or Stack Overflow
4. Check GitHub's documentation: https://docs.github.com

---

## Quick Reference Card

### First Time Setup
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/virtualryder/Password_Manager.git
git push -u origin main
```

### Regular Updates
```bash
git add .
git commit -m "Your message here"
git push
```

### Using SSH
```bash
ssh-keygen -t ed25519 -C "email@example.com"
# Add key to GitHub
git remote set-url origin git@github.com:virtualryder/Password_Manager.git
git push
```

---

**Remember**: Always review what you're committing before pushing to GitHub!
