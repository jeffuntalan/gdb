# Get the project name for title
project_name = frappe.db.get_value("Project", doc.project_code, "project_name")

# Create the Journal Entry
je = frappe.new_doc("Journal Entry")
je.voucher_type = "Journal Entry"
je.posting_date = frappe.utils.nowdate()
je.title = f"Retention Collection - {project_name}"
je.remark = doc.description or "Collection of 10% retention"

# === DEBIT ENTRIES ===

# Tax Withheld from Source
if doc.ewt:
    je.append("accounts", {
        "account": "1610 - Tax Withheld from Source - GDB",
        "debit_in_account_currency": float(doc.ewt),
    })

# Cash-In-Bank
if doc.net_collected:
    je.append("accounts", {
        "account": "1100 - Cash-In-Bank BDO Main - GDB",
        "debit_in_account_currency": float(doc.net_collected),
    })

# Output VAT (matching total VAT amount collected)
if doc.vat_amount:
    je.append("accounts", {
        "account": "2130 - Output VAT - GDB",
        "debit_in_account_currency": float(doc.vat_amount),
    })

# === CREDIT ENTRIES ===

# AR Output VAT (on Retention)
if doc.vat_amount:
    je.append("accounts", {
        "account": "1306 - AR Output VAT (on retention) - GDB",
        "credit_in_account_currency": float(doc.vat_amount),
    })

# AR Services Rendered (retention component)
if doc.net_of_vat:
    je.append("accounts", {
        "account": "1300 - AR Services Renderred - GDB",
        "credit_in_account_currency": float(doc.net_of_vat),
    })

# VAT Payable
if doc.vat_amount:
    je.append("accounts", {
        "account": "2135 - VAT Payable - GDB",
        "credit_in_account_currency": float(doc.vat_amount),
    })

# Balance Check
total_debit = sum(a.debit_in_account_currency or 0 for a in je.accounts)
total_credit = sum(a.credit_in_account_currency or 0 for a in je.accounts)
if round(total_debit, 2) != round(total_credit, 2):
    frappe.throw(f"Journal Entry not balanced. Debit: {total_debit}, Credit: {total_credit}")

# Submit Journal Entry
je.insert()
je.submit()
