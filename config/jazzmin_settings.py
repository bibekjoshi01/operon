# Jazzmin
# -----------------------------------------------------------------------------------------------

JAZZMIN_SETTINGS = {
    "site_title": "Operon Admin",
    "site_header": "OPERON",
    "site_brand": "OPERON",
    # "site_logo": "images/logo_main.png",
    "login_logo": "images/logo.png",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "theme": "flatly",
    "site_icon": None,
    "welcome_sign": "Welcome to the Operon",
    "copyright": "OPERON Pvt. Ltd.",
    "search_model": [],
    "user_avatar": None,
    # Links to put along the top menu
    "topmenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["order_management", "expense_management", "user"],
    "custom_links": {},
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://kayobadger.com.np/contact-us",
            "new_window": True,
            "icon": "fas fa-life-ring",
        },
    ],
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        # Custom User module
        "auth.User": "fas fa-user",
        # Order Management
        "order_management.PaymentMethod": "fas fa-credit-card",
        "order_management.Customer": "fas fa-user-tie",
        "order_management.Item": "fas fa-box",
        "order_management.OrderInvoice": "fas fa-cash-register",
        # Expense Management
        "expense_management.Expense": "fas fa-receipt",
        "expense_management.ExpenseCategory": "fas fa-folder-open",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Use modals instead of popups
    "related_modal_active": False,
    "custom_css": "css/jazzmin.css",
    "custom_js": "js/jazzmin.js",
    "use_google_fonts_cdn": True,
    "show_breadcrumbs": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
    "language_chooser": False,
}
