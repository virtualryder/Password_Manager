# 🔒 SphereRyder Security Services - Password Manager

> **Military-Grade Password Management System with AES-256-GCM Encryption**

A comprehensive, production-ready password manager built with Python, featuring end-to-end encryption, multi-user support, and both CLI and web-based interfaces.

✨ **Now fully compatible with Python 3.14!**

---

## 📋 Table of Contents

- [Features](#features)
- [Security Architecture](#security-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [GitHub Setup Instructions](#github-setup-instructions)
- [Local Deployment](#local-deployment)
- [Pre-configured Test Accounts](#pre-configured-test-accounts)
- [API Documentation](#api-documentation)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Functionality
- ✅ **Military-grade AES-256-GCM encryption** for password storage
- ✅ **PBKDF2 key derivation** with 480,000 iterations (OWASP 2023 recommendation)
- ✅ **Bcrypt password hashing** for user authentication
- ✅ **Multi-user support** with isolated password storage
- ✅ **Cryptographically secure** random password generation
- ✅ **Master password protection** with ability to change passwords
- ✅ **Activity logging** for security auditing
- ✅ **CRUD operations**: Create, Read, Update, Delete passwords

### Interfaces
- 🖥️ **Command-Line Interface (CLI)** - Interactive terminal-based UI
- 🌐 **Streamlit Web Interface** - Modern, user-friendly web application
- 📓 **Jupyter Notebook** - Comprehensive tutorial and testing environment

---

## 🔐 Security Architecture

### Encryption Flow

```
User Master Password
        ↓
    Bcrypt Hashing (12 rounds)
        ↓
    Authentication Successful
        ↓
    PBKDF2 Key Derivation
    (480,000 iterations + unique salt)
        ↓
    256-bit AES Encryption Key
        ↓
    AES-256-GCM Encryption
    (with unique nonce per password)
        ↓
    Encrypted Password Storage
```

### Security Features

1. **AES-256-GCM**: Authenticated encryption providing both confidentiality and integrity
2. **PBKDF2**: 480,000 iterations make brute-force attacks computationally prohibitive
3. **Unique Salts**: Each user has a unique salt, preventing rainbow table attacks
4. **Bcrypt**: Industry-standard password hashing with configurable cost factor
5. **Random Nonces**: Each password encryption uses a unique, random nonce
6. **Secure Random**: Uses Python's `secrets` module for cryptographically secure randomness

---

## 📦 Installation

### Prerequisites

- **Python 3.8 or higher** (tested and fully compatible with Python 3.14)
- **pip** (Python package manager)
- **Git** (for version control)

### Windows 11 Installation Steps

#### Step 1: Clone or Download the Project

```bash
# Navigate to your desired directory
cd C:\DRyder\Python-Week2

# If you have the files, just navigate to the directory
cd Password_Manager_Claudev1
```

#### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
# source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed bcrypt-5.0.0 cryptography-46.0.3 streamlit-1.52.1 pandas-2.3.3 ...
```

**Note:** Package versions may vary as the requirements.txt uses flexible version constraints (>=) to ensure compatibility with newer Python versions including Python 3.14.

---

## 🚀 Usage

### Method 1: Command-Line Interface (CLI)

```bash
# Run the CLI application
python cli_interface.py
```

**Features:**
- Interactive menu-driven interface
- Secure password input (hidden)
- View, add, update, delete passwords
- Change master password
- View activity logs

### Method 2: Streamlit Web Interface

```bash
# Start the web application
streamlit run streamlit_app.py
```

**Features:**
- Modern, responsive web UI
- Dashboard view of all passwords
- Easy-to-use forms
- Real-time updates
- Accessible at `http://localhost:8501`

### Method 3: Jupyter Notebook

```bash
# Start Jupyter Notebook
jupyter notebook password_manager_tutorial.ipynb
```

**Features:**
- Step-by-step tutorial
- Interactive code examples
- Security testing suite
- Performance benchmarks

---

## 📁 File Structure

```
Password_Manager_Claudev1/
│
├── password_manager.py          # Core password manager module
├── cli_interface.py             # Command-line interface
├── streamlit_app.py             # Web-based UI using Streamlit
├── password_manager_tutorial.ipynb  # Jupyter notebook tutorial
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore patterns
│
├── data/                        # Data directory (auto-created)
│   ├── users.json              # Encrypted user credentials
│   ├── passwords.json          # Encrypted passwords
│   └── activity.log            # Activity logs
│
└── docs/                        # Additional documentation
    └── SETUP_GUIDE.md          # Detailed setup guide
```

---

## 🔧 GitHub Setup Instructions

### Creating a Personal Access Token (Recommended Method)

GitHub now requires Personal Access Tokens instead of passwords for HTTPS operations.

#### Step 1: Generate a Personal Access Token

1. Go to GitHub.com and log in
2. Click your profile picture → **Settings**
3. Scroll down and click **Developer settings** (left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name: "Password Manager Push Access"
7. Select expiration (recommend: 90 days)
8. Select scopes:
   - ✅ `repo` (all repository permissions)
9. Click **Generate token**
10. **IMPORTANT**: Copy the token immediately (you won't see it again!)

#### Step 2: Initialize Git Repository Locally

```bash
# Navigate to your project directory
cd C:\DRyder\Python-Week2\Password_Manager_Claudev1

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SphereRyder Password Manager v1.0"
```

#### Step 3: Connect to GitHub Remote

```bash
# Add the remote repository
git remote add origin https://github.com/virtualryder/Password_Manager.git

# Verify remote was added
git remote -v
```

#### Step 4: Push to GitHub

```bash
# Push to GitHub (you'll be prompted for credentials)
git push -u origin main

# When prompted:
# Username: virtualryder
# Password: [PASTE YOUR PERSONAL ACCESS TOKEN HERE]
```

**Note**: If the default branch is `master` instead of `main`:
```bash
git branch -M main
git push -u origin main
```

### Alternative: SSH Key Authentication (More Secure)

#### Step 1: Generate SSH Key

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter to accept default location
# Enter a passphrase (or press Enter for no passphrase)
```

#### Step 2: Add SSH Key to GitHub

```bash
# Copy the SSH public key
# On Windows:
type %USERPROFILE%\.ssh\id_ed25519.pub

# On Linux/Mac:
# cat ~/.ssh/id_ed25519.pub
```

1. Copy the entire key output
2. Go to GitHub.com → Settings → SSH and GPG keys
3. Click **New SSH key**
4. Paste your key and give it a title
5. Click **Add SSH key**

#### Step 3: Push Using SSH

```bash
# Change remote URL to SSH
git remote set-url origin git@github.com:virtualryder/Password_Manager.git

# Push to GitHub
git push -u origin main
```

---

## 💻 Local Deployment

### Running the CLI Application

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run CLI
python cli_interface.py
```

### Running the Streamlit Web Application

```bash
# Activate virtual environment
venv\Scripts\activate

# Start Streamlit server
streamlit run streamlit_app.py

# Access at: http://localhost:8501
```

**Streamlit Configuration** (optional):

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 👥 Pre-configured Test Accounts

The system comes with three pre-configured test accounts:

| Username | Password | Description |
|----------|----------|-------------|
| `admin` | `Admin@2024` | Administrator account |
| `testuser` | `Test@2024` | Test user account |
| `demo` | `Demo@2024` | Demo account |

**Security Note**: Change these passwords immediately in production environments!

### Changing Pre-configured Passwords

**Via CLI:**
1. Login with a test account
2. Select "Change Master Password" from menu
3. Follow prompts

**Via Streamlit:**
1. Login with a test account
2. Navigate to "Change Master Password"
3. Fill in the form

---

## 📚 API Documentation

### PasswordManager Class

```python
from password_manager import PasswordManager

# Initialize
pm = PasswordManager(data_dir="data")

# Authenticate user
pm.authenticate(username="admin", password="Admin@2024")

# Generate secure password
password = pm.generate_password(length=16)

# Add password
pm.add_password(
    domain="github.com",
    password="MyPassword123!",  # Optional, auto-generated if None
    username="myuser",          # Optional
    notes="My GitHub account"   # Optional
)

# Retrieve password
pwd_data = pm.get_password("github.com")
print(pwd_data['password'])  # Decrypted password

# Update password
pm.update_password("github.com", new_password="NewPassword456!")

# Delete password
pm.delete_password("github.com")

# Get all domains
domains = pm.get_all_domains()

# Change master password
pm.change_master_password(
    old_password="Admin@2024",
    new_password="NewAdmin@2024"
)

# View logs
logs = pm.get_activity_logs(limit=50)

# Logout
pm.logout()
```

---

## 🛡️ Best Practices

### 1. Master Password Security
- ✅ Use at least 12 characters
- ✅ Include uppercase, lowercase, numbers, and special characters
- ✅ Never share your master password
- ✅ Use a unique password not used elsewhere
- ✅ Consider using a passphrase (e.g., "Correct-Horse-Battery-Staple")

### 2. Backup Strategy
- ✅ Regularly backup the `data/` directory
- ✅ Store backups in encrypted storage
- ✅ Test backup restoration periodically
- ✅ Keep backups in multiple secure locations

### 3. Access Control
- ✅ Set restrictive file permissions on `data/` directory
  ```bash
  # Windows (PowerShell):
  icacls data /inheritance:r /grant:r "%USERNAME%:(OI)(CI)F"
  
  # Linux/Mac:
  chmod 700 data
  ```
- ✅ Use full-disk encryption
- ✅ Lock computer when not in use
- ✅ Use strong authentication on your OS

### 4. Password Generation
- ✅ Always use auto-generated passwords when possible
- ✅ Minimum 16 characters for high-security accounts
- ✅ Include all character types
- ✅ Avoid dictionary words

### 5. Monitoring and Auditing
- ✅ Regularly review activity logs
- ✅ Look for suspicious login attempts
- ✅ Investigate unexpected password changes
- ✅ Monitor for unauthorized file access

---

## 🔍 Troubleshooting

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'cryptography'"
**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue 2: "Permission denied" when accessing data directory
**Solution (Windows):**
```bash
# Run as Administrator
icacls data /grant "%USERNAME%:(OI)(CI)F"
```

#### Issue 3: Streamlit won't start
**Solution:**
```bash
# Reinstall Streamlit
pip uninstall streamlit
pip install streamlit==1.29.0
```

#### Issue 4: Git push fails with "Authentication failed"
**Solution:**
- Verify you're using a Personal Access Token, not your password
- Check that your token has the `repo` scope
- Ensure your token hasn't expired

#### Issue 5: Can't decrypt passwords after system reinstall
**Solution:**
- This is by design - encryption keys are derived from master password
- You need both the master password AND the salt (stored in users.json)
- Always backup the entire `data/` directory

#### Issue 6: Package installation fails with Python 3.14
**Solution:**
- The project has been updated to support Python 3.14
- Ensure you're using the latest requirements.txt from the repository
- If you have an older version, update pandas to >=2.2.0:
  ```bash
  pip install "pandas>=2.2.0"
  ```
- For compilation errors with pandas 2.1.4 or older, upgrade to pandas 2.2.0 or higher

---

## 📄 License

This project is provided as-is for educational and internal use by SphereRyder Security Services.

---

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the Jupyter notebook tutorial
3. Check activity logs for error messages
4. Open an issue on GitHub

---

## 🔄 Version History

### Version 1.0.1 (Current)
- **Python 3.14 compatibility** - Updated package dependencies
- Updated requirements.txt to use flexible version constraints (>=)
- Upgraded pandas from 2.1.4 to >=2.2.0 for Python 3.14 support
- All features tested and verified on Python 3.14.0

### Version 1.0.0
- Initial release
- AES-256-GCM encryption
- PBKDF2 key derivation (480,000 iterations)
- Bcrypt authentication
- Multi-user support
- CLI and Streamlit interfaces
- Jupyter notebook tutorial
- Pre-configured test accounts

---

## 🎯 Future Enhancements

- [ ] Two-factor authentication (2FA/TOTP)
- [ ] Password strength analyzer
- [ ] Breach detection integration
- [ ] Cloud backup support
- [ ] Mobile application
- [ ] Browser extension
- [ ] Biometric authentication
- [ ] Hardware security key support

---

## ⚠️ Security Notice

This password manager is designed for educational purposes and internal use. For production deployment:

1. Conduct a thorough security audit
2. Implement additional security layers (firewalls, IDS/IPS)
3. Use hardware security modules (HSM) for key storage
4. Implement regular security updates
5. Follow your organization's security policies
6. Consider professional penetration testing

---

**Built with ❤️ by SphereRyder Security Services**

*Protecting Your Digital Identity*
#   P a s s w o r d _ M a n a g e r 
 
 
