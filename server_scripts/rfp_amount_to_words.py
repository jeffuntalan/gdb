# Convert numbers to words (handles big pesos + 86/100 format, no imports, no underscores)
def convert_number(n):
    ones = ["ZERO","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN",
            "ELEVEN","TWELVE","THIRTEEN","FOURTEEN","FIFTEEN","SIXTEEN","SEVENTEEN",
            "EIGHTEEN","NINETEEN"]
    tens = ["","","TWENTY","THIRTY","FORTY","FIFTY","SIXTY","SEVENTY","EIGHTY","NINETY"]
    scales = [(1000000000, "BILLION"), (1000000, "MILLION"), (1000, "THOUSAND"), (1, "")]

    def two_digits(x):
        if x < 20:
            return ones[x]
        return tens[x // 10] + ("" if x % 10 == 0 else " " + ones[x % 10])

    def three_digits(x):
        if x < 100:
            return two_digits(x)
        head = ones[x // 100] + " HUNDRED"
        tail = x % 100
        return head if tail == 0 else head + " " + two_digits(tail)

    if n == 0:
        return "ZERO"

    parts = []
    for scale_val, scale_name in scales:
        if n >= scale_val:
            chunk = n // scale_val
            n = n % scale_val
            if scale_val == 1:
                # last chunk (<= 999)
                parts.append(three_digits(chunk))
            else:
                parts.append(three_digits(chunk) + (" " + scale_name if scale_name else ""))
    return " ".join(parts)

# Main logic (Before Save)
if not doc.amount:
    doc.amount_in_words = ""
else:
    total_cents = int(round(float(doc.amount) * 100))
    pesos = total_cents // 100
    cents = total_cents % 100

    peso_words = convert_number(pesos)

    if cents > 0:
        # replaced str.format with safe f-string
        final_words = f"{peso_words} & {cents:02d}/100 PESOS ONLY"
    else:
        final_words = f"{peso_words} PESOS ONLY"

    doc.amount_in_words = final_words
