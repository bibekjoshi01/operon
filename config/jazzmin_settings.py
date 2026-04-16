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
    "site_icon": None,
    "welcome_sign": "Welcome to the Operon",
    "copyright": "OPERON Pvt. Ltd.",
    "search_model": [],
    "user_avatar": None,
    # Links to put along the top menu
    "topmenu_links": [],
    "usermenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "party_management",
        "sales",
        "purchase",
        "inventory",
        "user",
        "core",
    ],
    "custom_links": {},
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        # Custom User module
        "auth.User": "fas fa-user",
        # Core Setup
        "core.AdditionalChargeType": "fas fa-receipt",
        "core.PaymentMethod": "fas fa-credit-card",
        # Party Management
        "party_management.Customer": "fas fa-user-tie",
        "party_management.Supplier": "fas fa-truck-loading",
        # Items
        "inventory.Item": "fas fa-box",
        "inventory.ItemUnit": "fas fa-balance-scale",
        "inventory.ItemBrand": "fas fa-copyright",
        "inventory.ItemCategory": "fas fa-sitemap",
        "inventory.Warehouse": "fas fa-warehouse",
        # Purchase & Sales
        "purchase.PurchaseInvoice": "fas fa-file-invoice-dollar",
        "purchase.PurchaseReturn": "fas fa-undo-alt",
        "sales.SalesInvoice": "fas fa-cash-register",
        "sales.SalesReturn": "fas fa-undo",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Use modals instead of popups
    "related_modal_active": False,
    "custom_css": "css/jazzmin.css",
    "custom_js": "js/jazzmin.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}
