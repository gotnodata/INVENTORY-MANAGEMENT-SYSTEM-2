"""Report export helper functions for CSV and TXT formats"""
import csv
import os
from datetime import datetime
import config


def generate_filename(report_type, format_type):
    """Generate filename with timestamp and report type"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_report_type = report_type.replace(" ", "_").replace("&", "and")
    return f"{clean_report_type}_{timestamp}.{format_type}"


def export_to_csv(report_data, filepath):
    """Export report data to CSV format"""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header with report metadata
            writer.writerow(['Report Generated:', report_data.get('generated_at', 'N/A')])
            if 'filter_period' in report_data:
                writer.writerow(['Period:', report_data['filter_period']])
            writer.writerow([])  # Empty row
            
            # Write different sections based on report type
            if 'items' in report_data:  # Inventory Report
                writer.writerow(['INVENTORY ITEMS'])
                writer.writerow(['ID', 'Name', 'Category', 'Quantity', 'Cost Price'])
                for item in report_data.get('items', []):
                    writer.writerow([
                        item[0],  # ID
                        item[1],  # Name
                        item[7] or 'No Category',  # Category name
                        f"{item[3]} {item[8] if item[8] else ''}",  # Quantity with unit
                        item[9] or 0.0  # Cost price
                    ])
                
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Items:', report_data.get('total_items', 0)])
                writer.writerow(['Total Value:', f"${report_data.get('total_value', 0):.2f}"])
                
            elif 'transactions' in report_data:  # Transaction Report
                writer.writerow(['TRANSACTIONS'])
                writer.writerow(['ID', 'Date', 'Type', 'Item', 'Quantity', 'Notes'])
                for transaction in report_data.get('transactions', []):
                    writer.writerow([
                        transaction[0],  # ID
                        transaction[1],  # Date
                        transaction[2],  # Type
                        transaction[5],  # Item name
                        transaction[3],  # Quantity
                        transaction[4]  # Notes
                    ])
                
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Transactions:', report_data.get('total_transactions', 0)])
                writer.writerow(['Total IN:', report_data.get('total_in', 0)])
                writer.writerow(['Total OUT:', report_data.get('total_out', 0)])
                
            elif 'sales' in report_data:  # Sales Report
                writer.writerow(['SALES SUMMARY'])
                writer.writerow(['Item', 'Quantity Sold', 'Total Revenue'])
                for sale in report_data.get('sales', []):
                    writer.writerow([
                        sale[0],  # Item name
                        sale[1],  # Quantity sold
                        f"${sale[2]:.2f}"  # Total revenue
                    ])
                
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Sales:', f"${report_data.get('total_sales', 0):.2f}"])
                writer.writerow(['Total Items Sold:', report_data.get('total_items_sold', 0)])
                writer.writerow(['Average Sale:', f"${report_data.get('average_sale', 0):.2f}"])
                
            elif 'users' in report_data:  # User Activity Report
                writer.writerow(['USER ACTIVITY'])
                writer.writerow(['ID', 'Username', 'Email', 'Role', 'Created At'])
                for user in report_data.get('users', []):
                    writer.writerow([
                        user[0],  # ID
                        user[1],  # Username
                        user[2] or 'N/A',  # Email
                        user[3],  # Role
                        user[4]   # Created At
                    ])
                
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Users:', report_data.get('total_users', 0)])
                writer.writerow(['Active Users:', report_data.get('active_users', 0)])
                
            elif 'suppliers' in report_data:  # Supplier Report
                writer.writerow(['SUPPLIERS'])
                writer.writerow(['ID', 'Name', 'Contact', 'Email', 'Phone'])
                for supplier in report_data.get('suppliers', []):
                    writer.writerow([
                        supplier[0],  # ID
                        supplier[1],  # Name
                        supplier[2] or 'N/A',  # Contact
                        supplier[3] or 'N/A',  # Email
                        supplier[4] or 'N/A'   # Phone
                    ])
                
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Total Suppliers:', report_data.get('total_suppliers', 0)])
        
        return True, f"Report exported successfully to {filepath}"
    except Exception as e:
        return False, f"Error exporting: {str(e)}"


def export_to_txt(report_content, filepath):
    """Export report content to TXT format"""
    try:
        with open(filepath, 'w', encoding='utf-8') as txtfile:
            txtfile.write(report_content)
        return True, f"Report exported successfully to {filepath}"
    except Exception as e:
        return False, f"Error exporting: {str(e)}"
