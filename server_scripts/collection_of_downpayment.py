dp_net_vat = doc.dp_amount_net_of_vat
vat = doc.vat_amount
ewt = doc.ewt
actual = doc.actual_amount

# For safety: gross DP should be net + vat
gross_dp = dp_net_vat + vat

# Check: actual should equal gross_dp - ewt
expected_actual = gross_dp - ewt
if round(actual, 2) != round(expected_actual, 2):
    frappe.throw(f"Actual amount collected should be {expected_actual} (Gross DP - EWT)")

project_name = frappe.db.get_value("Project", doc.project_number, "project_name")

journal_entry = frappe.new_doc("Journal Entry")
journal_entry.posting_date = frappe.utils.nowdate()
journal_entry.voucher_type = "Journal Entry"
journal_entry.remark = f"DP Collection for Project: {project_name}"
journal_entry.title = f"DP - {project_name}"

# Debit: Tax Withheld
journal_entry.append("accounts", {
    "account": "1610 - Tax Withheld from Source - GDB",  # Replace with actual
    "debit_in_account_currency": ewt,
#    "reference_type": "Project",
#    "reference_name": doc.project_number
})

# Debit: Cash Received
journal_entry.append("accounts", {
    "account": "1100 - Cash-In-Bank BDO Main - GDB",  # Replace with actual
    "debit_in_account_currency": actual,
#    "reference_type": "Project",
#    "reference_name": doc.project_number
})

# Credit: Unearned Revenues (net)
journal_entry.append("accounts", {
    "account": "2300 - Unearned Revenues - GDB",  # Replace with actual
    "credit_in_account_currency": dp_net_vat,
#    "reference_type": "Project",
#    "reference_name": doc.project_number
})

# Credit: VAT Payable
journal_entry.append("accounts", {
    "account": "2135 - VAT Payable - GDB",  # Replace with actual
    "credit_in_account_currency": vat,
#    "reference_type": "Project",
#    "reference_name": doc.project_number
})

journal_entry.insert()
journal_entry.submit()

## July 15, 2025 Removed project references due to ref type errors.