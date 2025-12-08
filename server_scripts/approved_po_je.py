if doc.docstatus == 1:

    # Create the Journal Entry
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "posting_date": frappe.utils.today(),
        "user_remark": doc.description or "Created from PO Approval",
        "company": doc.company,  # match company of current doc

        "accounts": [
            {
                "account": doc.account,
                "debit_in_account_currency": doc.total,
                "cost_center": "PROJ - Project Operations - GDB",
                "project": doc.project_code,
                "remark": doc.description or "",
            },
            {
                "account": "2100 - A.P. Supplier - GDB",
                "credit_in_account_currency": doc.total,
                "cost_center": "PROJ - Project Operations - GDB",
                "project": doc.project_code,
                "remark": doc.description or "",
                "party_type": "Supplier",
                "party": doc.supplier  # required for Payable account
            }
        ]
    })

    je.insert(ignore_permissions=True)
    je.submit()

    frappe.msgprint("Journal Entry " + je.name + " created.")
