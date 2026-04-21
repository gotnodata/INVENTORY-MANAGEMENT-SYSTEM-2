"""Reports generation tab module"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os
import config
from database import models
from database.models import *
from database.export_helpers import export_to_csv, export_to_txt, generate_filename


class ReportsTab:
    """Reports generation tab class (admin only)"""
    
    def __init__(self, notebook, status_bar_updater):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 Reports")
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create reports tab UI with enhanced layout"""
        # Report type selection
        type_frame = ttk.LabelFrame(self.frame, text="📋 Report Type", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.report_type_var = tk.StringVar(value="inventory")
        ttk.Radiobutton(type_frame, text="📦 Inventory Report", variable=self.report_type_var, value="inventory").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(type_frame, text="💳 Transaction Report", variable=self.report_type_var, value="transactions").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(type_frame, text="💰 Sales Report", variable=self.report_type_var, value="sales").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(type_frame, text="👥 User Activity Report", variable=self.report_type_var, value="users").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Radiobutton(type_frame, text="🏭 Supplier Report", variable=self.report_type_var, value="suppliers").pack(anchor=tk.W, padx=10, pady=2)
        
        # Date range
        date_frame = ttk.LabelFrame(self.frame, text="📅 Date Range", padding=10)
        date_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date range with preset options
        preset_frame = ttk.Frame(date_frame)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(preset_frame, text="Quick Select:").pack(side=tk.LEFT)
        
        self.preset_var = tk.StringVar()
        preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, width=15)
        preset_combo['values'] = ['Today', 'This Week', 'This Month', 'This Quarter', 'This Year', 'Custom']
        preset_combo.set('This Month')
        preset_combo.pack(side=tk.LEFT, padx=5)
        preset_combo.bind('<<ComboboxSelected>>', self._on_preset_change)
        
        ttk.Button(preset_frame, text="🔄 Apply", command=self._apply_preset).pack(side=tk.LEFT, padx=5)
        
        # Custom date fields
        custom_frame = ttk.Frame(date_frame)
        custom_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(custom_frame, text="Start Date:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(custom_frame, textvariable=self.start_date_var, width=15)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(custom_frame, text="End Date:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(custom_frame, textvariable=self.end_date_var, width=15)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="📊 Generate Report", command=self.generate_report, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 Export to CSV", command=self.export_csv, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 Export to TXT", command=self.export_txt, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_report, width=10).pack(side=tk.LEFT, padx=5)
        
        # Report display
        display_frame = ttk.LabelFrame(self.frame, text="📋 Report Output", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Report text with status
        report_container = ttk.Frame(display_frame)
        report_container.pack(fill=tk.BOTH, expand=True)
        
        self.report_text = tk.Text(report_container, height=20, width=80, wrap=tk.WORD)
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(report_container, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self.status_label = ttk.Label(display_frame, text="Ready to generate reports", 
                                   font=config.DEFAULT_FONT_BODY, 
                                   foreground='gray')
        self.status_label.pack(pady=5)
    
    def _on_preset_change(self, event):
        """Handle preset date range change"""
        preset = self.preset_var.get()
        today = datetime.now()
        
        if preset == 'Today':
            self.start_date_var.set(today.strftime('%Y-%m-%d'))
            self.end_date_var.set(today.strftime('%Y-%m-%d'))
        elif preset == 'This Week':
            start_of_week = today - timedelta(days=today.weekday())
            self.start_date_var.set(start_of_week.strftime('%Y-%m-%d'))
            self.end_date_var.set(today.strftime('%Y-%m-%d'))
        elif preset == 'This Month':
            self.start_date_var.set(today.replace(day=1).strftime('%Y-%m-%d'))
            self.end_date_var.set(today.strftime('%Y-%m-%d'))
        elif preset == 'This Quarter':
            current_quarter = (today.month - 1) // 3 + 1
            start_of_quarter = today.replace(month=current_quarter * 3 - 2, day=1)
            self.start_date_var.set(start_of_quarter.strftime('%Y-%m-%d'))
            self.end_date_var.set(today.strftime('%Y-%m-%d'))
        elif preset == 'This Year':
            self.start_date_var.set(today.replace(month=1, day=1).strftime('%Y-%m-%d'))
            self.end_date_var.set(today.strftime('%Y-%m-%d'))
        # 'Custom' leaves fields unchanged
    
    def _apply_preset(self):
        """Apply the preset date range"""
        self._on_preset_change(None)
        self.update_status_bar(f"📅 Applied date range: {self.start_date_var.get()} to {self.end_date_var.get()}")
    
    def generate_report(self):
        """Generate selected report"""
        try:
            report_type = self.report_type_var.get()
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            
            self.status_label.config(text="🔄 Generating report...", foreground=config.COLOR_INFO)
            self.update_status_bar("🔄 Generating report...")
            
            if report_type == "inventory":
                data = models.generate_inventory_report(start_date, end_date)
                self.display_inventory_report(data)
            elif report_type == "transactions":
                data = models.generate_transaction_report(start_date, end_date)
                self.display_transaction_report(data)
            elif report_type == "sales":
                data = models.generate_sales_report(start_date, end_date)
                self.display_sales_report(data)
            elif report_type == "users":
                data = models.generate_user_activity_report(start_date, end_date)
                self.display_user_activity_report(data)
            elif report_type == "suppliers":
                data = models.generate_supplier_report(start_date, end_date)
                self.display_supplier_report(data)
            else:
                messagebox.showerror("Error", "Invalid report type!")
                return
                
            self.status_label.config(text="✅ Report generated successfully!", foreground=config.COLOR_SUCCESS)
            self.update_status_bar(f"✅ {report_type.title()} report generated successfully!")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", foreground=config.COLOR_DANGER)
            self.update_status_bar(f"❌ Failed to generate report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def display_inventory_report(self, data):
        """Display inventory report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"📦 INVENTORY REPORT\n")
        self.report_text.insert(tk.END, f"Generated: {data.get('generated_at', 'N/A')}\n")
        if data.get('filter_period'):
            self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📊 Summary Statistics:\n")
        self.report_text.insert(tk.END, f"Total Items: {data.get('total_items', 0)}\n")
        self.report_text.insert(tk.END, f"Total Value: ${data.get('total_value', 0):.2f}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📂 Items by Category:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        for category in data.get('categories', []):
            self.report_text.insert(tk.END, f"  {category[0]}: {category[1]} items, ${category[2]:.2f}\n")
        
        self.report_text.insert(tk.END, f"\n")
        self.report_text.insert(tk.END, f"⚠️  Low Stock Items:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        for item in data.get('low_stock', []):
            self.report_text.insert(tk.END, f"  {item[1]}: {item[3]} units\n")
    
    def display_transaction_report(self, data):
        """Display transaction report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"💳 TRANSACTION REPORT\n")
        self.report_text.insert(tk.END, f"Generated: {data.get('generated_at', 'N/A')}\n")
        if data.get('filter_period'):
            self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📊 Summary Statistics:\n")
        self.report_text.insert(tk.END, f"Total Transactions: {data.get('total_transactions', 0)}\n")
        self.report_text.insert(tk.END, f"Total IN: {data.get('total_in', 0)}\n")
        self.report_text.insert(tk.END, f"Total OUT: {data.get('total_out', 0)}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📋 Recent Transactions (Last 20):\n")
        self.report_text.insert(tk.END, "-" * 80 + "\n")
        for transaction in data.get('transactions', [])[:20]:
            self.report_text.insert(tk.END, 
                f"  {transaction[0]:<5} | {transaction[1]:<20} | {transaction[2]:<8} | "
                f"{transaction[3]:<8} | {transaction[4]:<12} | {transaction[5]:<20}\n")
    
    def display_sales_report(self, data):
        """Display sales report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"💰 SALES REPORT\n")
        self.report_text.insert(tk.END, f"Generated: {data.get('generated_at', 'N/A')}\n")
        if data.get('filter_period'):
            self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📊 Sales Summary:\n")
        self.report_text.insert(tk.END, f"Total Sales: ${data.get('total_sales', 0):.2f}\n")
        self.report_text.insert(tk.END, f"Total Items Sold: {data.get('total_items_sold', 0)}\n")
        self.report_text.insert(tk.END, f"Average Sale: ${data.get('average_sale', 0):.2f}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"🏆 Top Selling Items:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        for item in data.get('top_items', []):
            self.report_text.insert(tk.END, f"  {item[0]:<15} | {item[1]:<20} | "
                                     f"{item[2]} units | ${item[3]:.2f}\n")
    
    def display_user_activity_report(self, data):
        """Display user activity report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"👥 USER ACTIVITY REPORT\n")
        self.report_text.insert(tk.END, f"Generated: {data.get('generated_at', 'N/A')}\n")
        if data.get('filter_period'):
            self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📊 User Summary:\n")
        self.report_text.insert(tk.END, f"Total Users: {data.get('total_users', 0)}\n")
        self.report_text.insert(tk.END, f"Active Users: {data.get('active_users', 0)}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"👥 User List:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        for user in data.get('users', []):
            self.report_text.insert(tk.END, f"  {user[0]:<5} | {user[1]:<20} ({user[3]}) | "
                                 f"Created: {user[4]}\n")
    
    def display_supplier_report(self, data):
        """Display supplier report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, f"🏭 SUPPLIER REPORT\n")
        self.report_text.insert(tk.END, f"Generated: {data.get('generated_at', 'N/A')}\n")
        if data.get('filter_period'):
            self.report_text.insert(tk.END, f"Period: {data['filter_period']}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"📊 Supplier Summary:\n")
        self.report_text.insert(tk.END, f"Total Suppliers: {data.get('total_suppliers', 0)}\n")
        self.report_text.insert(tk.END, f"\n")
        
        self.report_text.insert(tk.END, f"🏭 Supplier List:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        for supplier in data.get('suppliers', []):
            self.report_text.insert(tk.END, f"  {supplier[0]:<5} | {supplier[1]:<25} | "
                                 f"{supplier[2] or 'N/A':<20} | {supplier[3] or 'N/A':<15}\n")
    
    def export_csv(self):
        """Export report to CSV"""
        try:
            report_type = self.report_type_var.get()
            data = {
                'report_type': report_type,
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'filter_period': f"{self.start_date_var.get()} to {self.end_date_var.get()}"
            }
            
            # Get actual report data based on type
            if report_type == "inventory":
                data.update(models.generate_inventory_report(self.start_date_var.get(), self.end_date_var.get()))
            elif report_type == "transactions":
                data.update(models.generate_transaction_report(self.start_date_var.get(), self.end_date_var.get()))
            elif report_type == "sales":
                data.update(models.generate_sales_report(self.start_date_var.get(), self.end_date_var.get()))
            elif report_type == "users":
                data.update(models.generate_user_activity_report(self.start_date_var.get(), self.end_date_var.get()))
            elif report_type == "suppliers":
                data.update(models.generate_supplier_report(self.start_date_var.get(), self.end_date_var.get()))
            
            filename = generate_filename(f"{report_type}_report", "csv")
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=filename
            )
            
            if filepath:
                success, message = export_to_csv(data, filepath)
                if success:
                    self.update_status_bar(f"📄 Report exported to {filepath}")
                    messagebox.showinfo("Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def export_txt(self):
        """Export report to TXT"""
        try:
            report_content = self.report_text.get(1.0, tk.END)
            report_type = self.report_type_var.get()
            filename = generate_filename(f"{report_type}_report", "txt")
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=filename
            )
            
            if filepath:
                success, message = export_to_txt(report_content, filepath)
                if success:
                    self.update_status_bar(f"📄 Report exported to {filepath}")
                    messagebox.showinfo("Export Successful", message)
                else:
                    messagebox.showerror("Export Failed", message)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def clear_report(self):
        """Clear report display"""
        self.report_text.delete(1.0, tk.END)
        self.status_label.config(text="📋 Report cleared", foreground='gray')
        self.update_status_bar("📋 Report display cleared")
