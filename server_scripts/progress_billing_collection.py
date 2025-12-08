# Get project name for title
project_name = frappe.db.get_value("Project", doc.project_code, "project_name")

# Create Journal Entry
je = frappe.new_doc("Journal Entry")
je.voucher_type = "Journal Entry"
je.posting_date = frappe.utils.nowdate()
je.title = f"Progress Billing Collection - {project_name}"
je.remark = doc.description or f"Collection for {project_name}"

# === DEBIT ENTRIES ===

# Tax Withheld from Source
if doc.ewt:
    je.append("accounts", {
        "account": "1610 - Tax Withheld from Source - GDB",
        "debit_in_account_currency": float(doc.ewt),
    })

# Cash-in-Bank (Actual Net Collected)
if doc.net_collected:
    je.append("accounts", {
        "account": "1100 - Cash-In-Bank BDO Main - GDB",
        "debit_in_account_currency": float(doc.net_collected),
    })

# Output VAT (Gross VAT credited to Output VAT)
if doc.vat_amount:
    je.append("accounts", {
        "account": "2130 - Output VAT - GDB",
        "debit_in_account_currency": float(doc.vat_amount),
    })

# === CREDIT ENTRIES ===

# AR Output VAT (reverse the original receivable VAT)
if doc.vat_amount:
    je.append("accounts", {
        "account": "1305 - AR Output VAT - GDB",
        "credit_in_account_currency": float(doc.vat_amount),
    })

# AR Services Rendered (reverse the receivable)
if doc.net_of_vat:
    je.append("accounts", {
        "account": "1300 - AR Services Renderred - GDB",
        "credit_in_account_currency": float(doc.net_of_vat),
    })

# VAT Payable (for government liability)
if doc.vat_amount:
    je.append("accounts", {
        "account": "2135 - VAT Payable - GDB",
        "credit_in_account_currency": float(doc.vat_amount),
    })

# Finalize and submit JE
je.insert()
je.submit()
