def create_balance_sheet():
    balance_sheet = {}
    people_owed = input("Enter people who are owed (separated by commas): ")
    for entry in people_owed.split(","):
        name, amount = entry.strip().split("+")
        balance_sheet[name.strip()] = float(amount.strip())

    people_owe = input("Enter people who owe money (separated by commas): ")
    for entry in people_owe.split(","):
        name, amount = entry.strip().split("+")
        balance_sheet[name.strip()] = -float(amount.strip())

    return balance_sheet


def balance_calculation(balance_sheet):
    transactions = []
    book_balance = 0

    for name, amount in balance_sheet.items():
        if amount < 0:
            while amount < 0:
                offset = False
                for other_name, other_amount in balance_sheet.items():
                    if other_name != name and other_amount > 0:
                        if other_amount >= abs(amount):
                            transactions.append((name, other_name, abs(amount)))
                            balance_sheet[other_name] -= abs(amount)
                            amount = 0
                            offset = True
                            break
                        else:
                            transactions.append((name, other_name, other_amount))
                            balance_sheet[other_name] -= other_amount
                            amount += other_amount
                            offset = True
                if not offset:
                    break

            if not offset:
                transactions.append((name, "@Liam1265", abs(amount)))
                book_balance += abs(amount)

    if sum(balance_sheet.values()) < 0:
        for name, amount in balance_sheet.items():
            if amount > 0:
                transactions.append(("@Liam1265", name, amount))
                book_balance -= amount

    # Handle remaining owed amount
    if sum(balance_sheet.values()) > 0:
        remaining_owed = sum(balance_sheet.values())
        transactions.append(("Book", "Liam1265", remaining_owed))
        book_balance -= remaining_owed

    # Group transactions by person who owes money
    grouped_transactions = {}
    for transaction in transactions:
        debtor = transaction[0]
        creditor = transaction[1]
        amount = transaction[2]
        if debtor not in grouped_transactions:
            grouped_transactions[debtor] = []
        grouped_transactions[debtor].append((creditor, amount))

    # Updated output format
    for debtor, debts in grouped_transactions.items():
        print("\nHey, Got you down last week. Please Venmo the following person/s and send a screenshot for FP. Let me know if you have any questions. Thanks.")
        for creditor, amount in debts:
            print(f"{debtor} owes {creditor} ${amount:.2f}")

    print(f"\nTotal amount owed to @Liam1265: ${book_balance:.2f}")


balance_sheet = create_balance_sheet()
balance_calculation(balance_sheet)