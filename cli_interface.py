"""
SphereRyder Security Services - Password Manager CLI
Command-Line Interface

This module provides an interactive command-line interface for the password manager.
"""

from password_manager import PasswordManager
import getpass
import sys


class PasswordManagerCLI:
    """Command-line interface for Password Manager"""
    
    def __init__(self):
        """Initialize the CLI with Password Manager instance"""
        self.pm = PasswordManager()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 70)
        print(" " * 15 + "SphereRyder Security Services")
        print(" " * 20 + "Password Manager v1.0")
        print("=" * 70)
        print()
    
    def print_menu(self):
        """Print main menu options"""
        print("\n" + "=" * 70)
        print("MAIN MENU")
        print("=" * 70)
        print("1. View Stored Passwords")
        print("2. Add New Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Change Master Password")
        print("6. View Activity Logs")
        print("7. Logout")
        print("=" * 70)
    
    def login(self) -> bool:
        """
        Handle user login
        
        Returns:
            True if login successful, False otherwise
        """
        self.clear_screen()
        self.print_header()
        
        print("PRE-CONFIGURED TEST ACCOUNTS:")
        print("-" * 70)
        print("Username: admin    | Password: Admin@2024")
        print("Username: testuser | Password: Test@2024")
        print("Username: demo     | Password: Demo@2024")
        print("-" * 70)
        print("\nNote: You can change your password after logging in.\n")
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter master password: ")
            
            if self.pm.authenticate(username, password):
                print(f"\n✓ Login successful! Welcome, {username}.")
                input("\nPress Enter to continue...")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n✗ Authentication failed. {remaining} attempts remaining.")
                else:
                    print("\n✗ Maximum login attempts exceeded.")
                    return False
        
        return False
    
    def view_passwords(self):
        """Display all stored passwords for current user"""
        self.clear_screen()
        self.print_header()
        
        domains = self.pm.get_all_domains()
        
        if not domains:
            print("No passwords stored yet.")
            input("\nPress Enter to continue...")
            return
        
        print(f"STORED PASSWORDS ({len(domains)} total)")
        print("=" * 70)
        
        for i, domain in enumerate(domains, 1):
            pwd_data = self.pm.get_password(domain)
            
            if pwd_data:
                print(f"\n{i}. Domain: {domain}")
                print(f"   Password: {pwd_data['password']}")
                if pwd_data['username']:
                    print(f"   Username: {pwd_data['username']}")
                if pwd_data['notes']:
                    print(f"   Notes: {pwd_data['notes']}")
                print(f"   Created: {pwd_data['created_at'][:10]}")
                print(f"   Updated: {pwd_data['updated_at'][:10]}")
                print("-" * 70)
        
        input("\nPress Enter to continue...")
    
    def add_password(self):
        """Add a new password entry"""
        self.clear_screen()
        self.print_header()
        
        print("ADD NEW PASSWORD")
        print("=" * 70)
        
        domain = input("\nEnter domain/service name (e.g., gmail.com): ").strip()
        
        if not domain:
            print("\n✗ Domain name cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        # Check if domain already exists
        if domain in self.pm.get_all_domains():
            print(f"\n✗ Password for '{domain}' already exists. Use 'Update' to modify it.")
            input("\nPress Enter to continue...")
            return
        
        username = input("Enter username (optional, press Enter to skip): ").strip() or None
        
        print("\nPassword Options:")
        print("1. Auto-generate secure password (recommended)")
        print("2. Enter your own password")
        choice = input("Choose option (1 or 2): ").strip()
        
        password = None
        if choice == "2":
            password = getpass.getpass("Enter password: ")
            if len(password) < 8:
                print("\n⚠ Warning: Password is shorter than 8 characters (not recommended)")
        else:
            password = self.pm.generate_password(16)
            print(f"\n✓ Generated password: {password}")
        
        notes = input("Enter notes (optional, press Enter to skip): ").strip() or None
        
        if self.pm.add_password(domain, password, username, notes):
            print(f"\n✓ Password for '{domain}' added successfully!")
        else:
            print("\n✗ Failed to add password.")
        
        input("\nPress Enter to continue...")
    
    def update_password(self):
        """Update an existing password"""
        self.clear_screen()
        self.print_header()
        
        domains = self.pm.get_all_domains()
        
        if not domains:
            print("No passwords stored yet.")
            input("\nPress Enter to continue...")
            return
        
        print("UPDATE PASSWORD")
        print("=" * 70)
        print("\nYour domains:")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        domain = input("\nEnter domain name to update: ").strip()
        
        if domain not in domains:
            print(f"\n✗ Domain '{domain}' not found.")
            input("\nPress Enter to continue...")
            return
        
        print("\nPassword Options:")
        print("1. Auto-generate new secure password (recommended)")
        print("2. Enter your own password")
        choice = input("Choose option (1 or 2): ").strip()
        
        new_password = None
        if choice == "2":
            new_password = getpass.getpass("Enter new password: ")
        else:
            new_password = self.pm.generate_password(16)
            print(f"\n✓ Generated password: {new_password}")
        
        if self.pm.update_password(domain, new_password):
            print(f"\n✓ Password for '{domain}' updated successfully!")
        else:
            print("\n✗ Failed to update password.")
        
        input("\nPress Enter to continue...")
    
    def delete_password(self):
        """Delete a password entry"""
        self.clear_screen()
        self.print_header()
        
        domains = self.pm.get_all_domains()
        
        if not domains:
            print("No passwords stored yet.")
            input("\nPress Enter to continue...")
            return
        
        print("DELETE PASSWORD")
        print("=" * 70)
        print("\nYour domains:")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        domain = input("\nEnter domain name to delete: ").strip()
        
        if domain not in domains:
            print(f"\n✗ Domain '{domain}' not found.")
            input("\nPress Enter to continue...")
            return
        
        confirm = input(f"\n⚠ Are you sure you want to delete '{domain}'? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            if self.pm.delete_password(domain):
                print(f"\n✓ Password for '{domain}' deleted successfully!")
            else:
                print("\n✗ Failed to delete password.")
        else:
            print("\n✓ Deletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def change_master_password(self):
        """Change the master password"""
        self.clear_screen()
        self.print_header()
        
        print("CHANGE MASTER PASSWORD")
        print("=" * 70)
        print("\n⚠ Warning: This will re-encrypt all your passwords with the new master password.")
        
        old_password = getpass.getpass("\nEnter current master password: ")
        new_password = getpass.getpass("Enter new master password: ")
        confirm_password = getpass.getpass("Confirm new master password: ")
        
        if new_password != confirm_password:
            print("\n✗ New passwords do not match.")
            input("\nPress Enter to continue...")
            return
        
        if len(new_password) < 8:
            print("\n✗ New password must be at least 8 characters long.")
            input("\nPress Enter to continue...")
            return
        
        if self.pm.change_master_password(old_password, new_password):
            print("\n✓ Master password changed successfully!")
            print("All passwords have been re-encrypted with the new master password.")
        else:
            print("\n✗ Failed to change password. Please check your current password.")
        
        input("\nPress Enter to continue...")
    
    def view_logs(self):
        """View activity logs"""
        self.clear_screen()
        self.print_header()
        
        print("ACTIVITY LOGS (Last 50 entries)")
        print("=" * 70)
        
        logs = self.pm.get_activity_logs(50)
        
        if not logs:
            print("No activity logs found.")
        else:
            for log in logs:
                print(log.strip())
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        # Login first
        if not self.login():
            print("\nExiting application.")
            return
        
        # Main menu loop
        while self.running:
            self.clear_screen()
            self.print_header()
            print(f"Logged in as: {self.pm.current_user}")
            self.print_menu()
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.view_passwords()
            elif choice == '2':
                self.add_password()
            elif choice == '3':
                self.update_password()
            elif choice == '4':
                self.delete_password()
            elif choice == '5':
                self.change_master_password()
            elif choice == '6':
                self.view_logs()
            elif choice == '7':
                self.pm.logout()
                print("\n✓ Logged out successfully.")
                self.running = False
            else:
                print("\n✗ Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
        
        print("\nThank you for using SphereRyder Password Manager!")


def main():
    """Entry point for CLI application"""
    try:
        cli = PasswordManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
