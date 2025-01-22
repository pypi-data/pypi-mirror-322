ROLES = [
    {
        "name": "admin",
        "description": "Manage all aspects, including employee roles, menus, promotions, and settings.",
        "is_removable": False,
    },
    {
        "name": "manager",
        "description": "Access to reports, inventory, and staff management (without system-level settings)",
        "is_removable": False,
    },
    {
        "name": "cashier",
        "description": "Process sales, apply discounts (if allowed), and issue receipts.  Limited access to reports (e.g., daily sales summary).",
    },
    {
        "name": "waiter / server",
        "description": "Enter orders, split bills, and send order tickets to kitchen printers or displays. Limited visibility of sales or reports.",
    },
]
