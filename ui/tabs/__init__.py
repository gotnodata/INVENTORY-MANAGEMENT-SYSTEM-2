"""UI tabs package - modular tab implementations"""
from ui.tabs.inventory_tab import InventoryTab
from ui.tabs.categories_tab import CategoriesTab
from ui.tabs.suppliers_tab import SuppliersTab
from ui.tabs.transactions_tab import TransactionsTab
from ui.tabs.users_tab import UsersTab
from ui.tabs.reports_tab import ReportsTab

__all__ = [
    'InventoryTab',
    'CategoriesTab',
    'SuppliersTab',
    'TransactionsTab',
    'UsersTab',
    'ReportsTab'
]
