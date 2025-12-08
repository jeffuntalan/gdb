# Fetch project name for the title
project_name = frappe.db.get_value("Project", doc.project_code, "project_name")

# Create journal entry
je = frappe.new_doc("Journal Entry")
je.voucher_type = "Journal Entry"
je.posting_date = frappe.utils.nowdate()
je.title = f"Progress Billing - {project_name}"
je.remark = doc.description or f"Progress Billing for {project_name}"

# === DEBITS ===
if doc.dp_recoupment_net:
    je.append("accounts", {
        "account": "2300 - Unearned Revenues - GDB",
        "debit_in_account_currency": float(doc.dp_recoupment_net),
    })

if doc.retention_net:
    je.append("accounts", {
        "account": "1310 - Retention on Contracts - GDB",
        "debit_in_account_currency": float(doc.retention_net),
    })

if doc.retention_vat:
    je.append("accounts", {
        "account": "1306 - AR Output VAT (on retention) - GDB",
        "debit_in_account_currency": float(doc.retention_vat),
    })

if doc.collectible:
    je.append("accounts", {
        "account": "1300 - AR Services Renderred - GDB",
        "debit_in_account_currency": float(doc.collectible),
    })

if doc.vat_collectible:
    je.append("accounts", {
        "account": "1305 - AR Output VAT - GDB",
        "debit_in_account_currency": float(doc.vat_collectible),
    })

# === CREDIT ===
if doc.accomplishment_net:
    je.append("accounts", {
        "account": "3000 - Service Revenue - GDB",
        "credit_in_account_currency": float(doc.accomplishment_net),
    })

# Output VAT (Combined: retention + collectible)
output_vat_total = 0.0

retention_vat = float(doc.retention_vat or 0)
vat_collectible = float(doc.vat_collectible or 0)

output_vat_total = retention_vat + vat_collectible

if output_vat_total > 0:
    je.append("accounts", {
        "account": "2130 - Output VAT - GDB",
        "credit_in_account_currency": output_vat_total
    })

# === Finalize ===
je.insert()
je.submit()
