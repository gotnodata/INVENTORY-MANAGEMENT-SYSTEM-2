import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
import config
from database import models
from auth import auth
from ui.login import LoginWindow
from ui.windows import InventoryManagementGUI

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# region agent log
_DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug-31c49c.log")

def _agent_log(hypothesisId: str, location: str, message: str, data: dict | None = None, runId: str = "pre-fix"):
    try:
        import json, time
        payload = {
            "sessionId": "31c49c",
            "runId": runId,
            "hypothesisId": hypothesisId,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _install_excepthook():
    def _hook(exc_type, exc, tb):
        try:
            import traceback
            _agent_log(
                "H-exception",
                "main.py:sys.excepthook",
                "Unhandled exception",
                {"type": getattr(exc_type, "__name__", str(exc_type)), "message": str(exc), "traceback": "".join(traceback.format_tb(tb))},
            )
        finally:
            sys.__excepthook__(exc_type, exc, tb)

    sys.excepthook = _hook
# endregion


def init_database():
    """Initialize all database tables"""
    models.init_db()
    models.create_categories_table()
    models.create_suppliers_table()
    models.create_transactions_table()
    models.create_users_table()
    models.create_measurement_units_table()
    models.init_default_measurement_units()
    models.update_database_schema()  # Update existing database


def create_first_admin():
    """Create first admin user if no users exist. Returns True if first admin was created."""
    users = auth.get_all_users()
    if users:
        return False  # Users already exist
    
    # Create first admin user
    setup_root = tk.Tk()
    setup_root.iconbitmap("ui/images/favicon.ico")
    setup_root.geometry(config.SETUP_WINDOW_GEOMETRY)
    setup_root.withdraw()  # Hide main window

    username = simpledialog.askstring("First Time Setup", "Enter admin username:")
    if not username:
        setup_root.destroy()
        return False
    
    password = simpledialog.askstring("First Time Setup", "Enter admin password:", show='*')
    if not password or len(password) < config.MIN_PASSWORD_LENGTH:
        messagebox.showerror("Error", f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters!")
        setup_root.destroy()
        return False
    
    email = simpledialog.askstring("First Time Setup", "Enter admin email (optional):")
    
    if auth.create_user(username, password, email or None, config.ROLE_ADMIN):
        messagebox.showinfo("Success", f"Admin user '{username}' created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create admin user!")
    
    setup_root.destroy()
    return True  # First admin was created


def main():
    """Main application entry point"""
    _install_excepthook()
    _agent_log("H-flow", "main.py:main", "Starting application")
    # Initialize database
    init_database()
    _agent_log("H-flow", "main.py:main", "Database initialized")
    
    # Create first admin user if needed
    first_admin_created = create_first_admin()
    _agent_log("H-flow", "main.py:main", "First-admin check completed", {"created": bool(first_admin_created)})
    
    # Show login window (either immediately or after admin creation)
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
    _agent_log("H-flow", "main.py:main", "Login window closed", {"authenticated": bool(login_window.authenticated_user)})
    
    # If login successful, show main application
    if login_window.authenticated_user:
        main_root = tk.Tk()
        app = InventoryManagementGUI(main_root, login_window.authenticated_user)
        main_root.mainloop()


if __name__ == "__main__":
    _install_excepthook()
    _agent_log("H-flow", "main.py:__main__", "Entered __main__", {"argv": sys.argv})
    try:
        main()
    except Exception as e:
        _agent_log("H-exception", "main.py:__main__", "Exception bubbled to __main__", {"type": type(e).__name__, "message": str(e)})
        raise
