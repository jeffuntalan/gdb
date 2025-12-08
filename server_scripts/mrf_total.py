total = 0

# Safely loop through child table rows
for row in doc.items:
    if row.amount:
        total = total + row.amount  # avoid += (not allowed in Safe Exec)

# Assign to your read-only total field
doc.custom_total_amount = total
