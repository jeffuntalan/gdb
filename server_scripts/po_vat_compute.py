if doc.grand_total:
    # Get percentage from float field (e.g. 12 means 12%)
    vat_percent = doc.get("custom_vat_") or 0

    # Convert to decimal rate
    vat_rate = vat_percent / 100

    # Compute Net of VAT
    net = doc.grand_total / (1 + vat_rate)

    # Compute VAT Amount
    vat = doc.grand_total - net

    # Assign computed values
    doc.custom_net_of_vat = net
    doc.custom_vat = vat
