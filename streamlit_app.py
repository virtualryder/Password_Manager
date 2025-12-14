"""
SphereRyder Security Services - Password Manager
Streamlit Web Interface

This module provides a simplified web-based UI for the password manager using Streamlit.
"""

import streamlit as st
from password_manager import PasswordManager
import pandas as pd
from datetime import datetime


# Configure page
st.set_page_config(
    page_title="SphereRyder Password Manager",
    page_icon="🔒",
    layout="wide"
)


def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'pm' not in st.session_state:
        st.session_state.pm = PasswordManager()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None


def login_page():
    """Display login page"""
    st.title("🔒 SphereRyder Password Manager")
    st.markdown("### Secure Password Management System")
    
    st.info("""
    **Pre-configured Test Accounts:**
    
    | Username | Password |
    |----------|----------|
    | admin | Admin@2024 |
    | testuser | Test@2024 |
    | demo | Demo@2024 |
    
    💡 You can change your password after logging in.
    """)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Master Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if st.session_state.pm.authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✓ Login successful! Welcome, {username}.")
                st.rerun()
            else:
                st.error("✗ Authentication failed. Please check your credentials.")


def main_page():
    """Display main application page"""
    # Header
    st.title("🔒 SphereRyder Password Manager")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as: **{st.session_state.username}**")
        st.markdown("---")
        
        menu_option = st.radio(
            "Navigation",
            ["View Passwords", "Add Password", "Update Password", "Delete Password", 
             "Change Master Password", "Activity Logs"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.pm.logout()
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Main content area
    if menu_option == "View Passwords":
        view_passwords_page()
    elif menu_option == "Add Password":
        add_password_page()
    elif menu_option == "Update Password":
        update_password_page()
    elif menu_option == "Delete Password":
        delete_password_page()
    elif menu_option == "Change Master Password":
        change_master_password_page()
    elif menu_option == "Activity Logs":
        activity_logs_page()


def view_passwords_page():
    """Display all stored passwords"""
    st.header("📋 Stored Passwords")
    
    domains = st.session_state.pm.get_all_domains()
    
    if not domains:
        st.info("No passwords stored yet. Add your first password using the 'Add Password' option.")
        return
    
    st.success(f"Total passwords stored: {len(domains)}")
    
    # Create a table of passwords
    password_data = []
    for domain in domains:
        pwd_data = st.session_state.pm.get_password(domain)
        if pwd_data:
            password_data.append({
                'Domain': domain,
                'Username': pwd_data.get('username', 'N/A'),
                'Password': pwd_data['password'],
                'Created': pwd_data.get('created_at', '')[:10],
                'Updated': pwd_data.get('updated_at', '')[:10]
            })
    
    # Display as DataFrame
    if password_data:
        df = pd.DataFrame(password_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Show detailed view
        st.markdown("---")
        st.subheader("Detailed View")
        selected_domain = st.selectbox("Select a domain to view details:", domains)
        
        if selected_domain:
            pwd_data = st.session_state.pm.get_password(selected_domain)
            if pwd_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Domain:** {selected_domain}")
                    st.markdown(f"**Username:** {pwd_data.get('username', 'N/A')}")
                    st.markdown(f"**Password:** `{pwd_data['password']}`")
                
                with col2:
                    st.markdown(f"**Created:** {pwd_data.get('created_at', 'N/A')}")
                    st.markdown(f"**Updated:** {pwd_data.get('updated_at', 'N/A')}")
                    if pwd_data.get('notes'):
                        st.markdown(f"**Notes:** {pwd_data['notes']}")


def add_password_page():
    """Add a new password"""
    st.header("➕ Add New Password")
    
    with st.form("add_password_form"):
        domain = st.text_input("Domain/Service Name *", placeholder="e.g., gmail.com, github")
        username = st.text_input("Username (optional)", placeholder="e.g., john.doe@email.com")
        
        password_option = st.radio(
            "Password Option",
            ["Auto-generate secure password (recommended)", "Enter your own password"]
        )
        
        custom_password = None
        if password_option == "Enter your own password":
            custom_password = st.text_input("Password", type="password")
        
        notes = st.text_area("Notes (optional)", placeholder="Add any additional notes...")
        
        submit = st.form_submit_button("Add Password")
        
        if submit:
            if not domain:
                st.error("Domain name is required!")
            elif domain in st.session_state.pm.get_all_domains():
                st.error(f"Password for '{domain}' already exists. Use 'Update Password' to modify it.")
            else:
                # Determine password to use
                password_to_use = custom_password if password_option == "Enter your own password" else None
                
                if st.session_state.pm.add_password(
                    domain, 
                    password_to_use,
                    username if username else None,
                    notes if notes else None
                ):
                    st.success(f"✓ Password for '{domain}' added successfully!")
                    
                    # Show generated password if auto-generated
                    if password_option == "Auto-generate secure password (recommended)":
                        pwd_data = st.session_state.pm.get_password(domain)
                        if pwd_data:
                            st.info(f"**Generated Password:** `{pwd_data['password']}`")
                            st.warning("⚠️ Please save this password - it won't be shown again!")
                else:
                    st.error("Failed to add password.")


def update_password_page():
    """Update an existing password"""
    st.header("🔄 Update Password")
    
    domains = st.session_state.pm.get_all_domains()
    
    if not domains:
        st.info("No passwords stored yet.")
        return
    
    with st.form("update_password_form"):
        selected_domain = st.selectbox("Select Domain to Update", domains)
        
        password_option = st.radio(
            "Password Option",
            ["Auto-generate new secure password (recommended)", "Enter your own password"]
        )
        
        custom_password = None
        if password_option == "Enter your own password":
            custom_password = st.text_input("New Password", type="password")
        
        submit = st.form_submit_button("Update Password")
        
        if submit:
            # Determine password to use
            password_to_use = custom_password if password_option == "Enter your own password" else None
            
            if st.session_state.pm.update_password(selected_domain, password_to_use):
                st.success(f"✓ Password for '{selected_domain}' updated successfully!")
                
                # Show generated password if auto-generated
                if password_option == "Auto-generate new secure password (recommended)":
                    pwd_data = st.session_state.pm.get_password(selected_domain)
                    if pwd_data:
                        st.info(f"**New Generated Password:** `{pwd_data['password']}`")
                        st.warning("⚠️ Please save this password - it won't be shown again!")
            else:
                st.error("Failed to update password.")


def delete_password_page():
    """Delete a password entry"""
    st.header("🗑️ Delete Password")
    
    domains = st.session_state.pm.get_all_domains()
    
    if not domains:
        st.info("No passwords stored yet.")
        return
    
    st.warning("⚠️ Warning: Deleting a password is permanent and cannot be undone!")
    
    with st.form("delete_password_form"):
        selected_domain = st.selectbox("Select Domain to Delete", domains)
        
        confirm = st.checkbox("I confirm I want to delete this password")
        
        submit = st.form_submit_button("Delete Password", type="primary")
        
        if submit:
            if not confirm:
                st.error("Please confirm deletion by checking the checkbox.")
            else:
                if st.session_state.pm.delete_password(selected_domain):
                    st.success(f"✓ Password for '{selected_domain}' deleted successfully!")
                else:
                    st.error("Failed to delete password.")


def change_master_password_page():
    """Change master password"""
    st.header("🔐 Change Master Password")
    
    st.warning("""
    ⚠️ **Important:** This will re-encrypt all your passwords with the new master password.
    
    Make sure to remember your new password - it cannot be recovered if lost!
    """)
    
    with st.form("change_master_password_form"):
        old_password = st.text_input("Current Master Password", type="password")
        new_password = st.text_input("New Master Password", type="password")
        confirm_password = st.text_input("Confirm New Master Password", type="password")
        
        submit = st.form_submit_button("Change Password")
        
        if submit:
            if not old_password or not new_password or not confirm_password:
                st.error("All fields are required!")
            elif new_password != confirm_password:
                st.error("New passwords do not match!")
            elif len(new_password) < 8:
                st.error("New password must be at least 8 characters long!")
            else:
                if st.session_state.pm.change_master_password(old_password, new_password):
                    st.success("✓ Master password changed successfully!")
                    st.info("All your passwords have been re-encrypted with the new master password.")
                else:
                    st.error("Failed to change password. Please check your current password.")


def activity_logs_page():
    """Display activity logs"""
    st.header("📊 Activity Logs")
    
    logs = st.session_state.pm.get_activity_logs(100)
    
    if not logs:
        st.info("No activity logs found.")
        return
    
    st.success(f"Showing last {len(logs)} log entries")
    
    # Display logs in a text area
    log_text = "\n".join(logs)
    st.text_area("Activity Log", log_text, height=400)


def main():
    """Main application entry point"""
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_page()


if __name__ == "__main__":
    main()
