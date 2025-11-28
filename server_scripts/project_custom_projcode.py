# DocType: Project | Event: After Insert
# Set custom_project_code to the initial series (doc.name) and never change it.

# doc is provided by Frappe
if doc.name and not doc.get("custom_project_code"):
    frappe.db.set_value(doc.doctype, doc.name, "custom_project_code", doc.name)