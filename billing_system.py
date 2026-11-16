"""
PS 23 - Simple Billing System
Rungta International Skills University - School of CSE
Concepts used: Lists, Dictionaries, Functions, File Handling
"""

# ---------------------------------------------------------------
# Product catalogue (dictionary): product name -> price per unit
# ---------------------------------------------------------------
PRODUCTS = {
    "Rice": 50,
    "Sugar": 40,
    "Oil": 120,
}

GST_RATE = 0.05          # 5% GST on the subtotal
BILL_FILE = "bill.txt"   # file where the final bill is saved

# Bill items are kept in a list; each item is a dictionary
bill_items = []


def find_product(name):
    """Return the catalogue name matching `name` (case-insensitive), else None."""
    name = name.strip().lower()
    for product in PRODUCTS:
        if product.lower() == name:
            return product
    return None


def add_item(product_name, quantity):
    """Validate and add an item to the bill. Returns True if added."""
    product = find_product(product_name)
    if product is None:
        print("Invalid product. Available: " + ", ".join(PRODUCTS))
        return False

    if quantity < 1:
        print("Quantity must be at least 1.")
        return False

    amount = PRODUCTS[product] * quantity

    # If the product is already in the bill, increase its quantity
    for item in bill_items:
        if item["name"] == product:
            item["qty"] += quantity
            item["amount"] += amount
            break
    else:
        bill_items.append({"name": product, "qty": quantity, "amount": amount})

    print(f"{product} x{quantity} added | Amount: {amount}")
    return True


def calculate_totals():
    """Return (subtotal, gst, grand_total)."""
    subtotal = sum(item["amount"] for item in bill_items)
    gst = subtotal * GST_RATE
    grand_total = subtotal + gst
    return subtotal, gst, grand_total


def build_bill_text(customer):
    """Create the neatly formatted bill as a single string."""
    subtotal, gst, grand_total = calculate_totals()
    line = "=" * 44
    thin = "-" * 44

    rows = [
        line,
        "SIMPLE BILLING SYSTEM".center(44),
        line,
        f"Customer: {customer}",
        thin,
        f"{'Item':<12}{'Qty':>6}{'Rate':>10}{'Amount':>14}",
        thin,
    ]
    for item in bill_items:
        rate = PRODUCTS[item["name"]]
        rows.append(
            f"{item['name']:<12}{item['qty']:>6}{rate:>10}{item['amount']:>14.2f}"
        )
    rows += [
        thin,
        f"{'Subtotal:':<30}{subtotal:>14.2f}",
        f"{'GST (5%):':<30}{gst:>14.2f}",
        thin,
        f"{'Grand Total:':<30}{grand_total:>14.2f}",
        line,
        "Thank you! Visit again.".center(44),
        line,
    ]
    return "\n".join(rows)


def view_bill():
    """Show the items added so far (running bill)."""
    if not bill_items:
        print("No items added yet.")
        return
    print("\nCurrent items:")
    print(" | ".join(f"{i['name']} x{i['qty']} = {i['amount']}" for i in bill_items))
    subtotal, gst, grand_total = calculate_totals()
    print(f"Subtotal: {subtotal:.0f} | GST (5%): {gst:.2f}")
    print(f"Grand Total: {grand_total:.2f}")


def save_bill(text):
    """Save the bill to bill.txt (file handling)."""
    try:
        with open(BILL_FILE, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Bill saved to {BILL_FILE}")
    except OSError as err:
        print(f"Could not save bill: {err}")


def generate_bill(customer):
    """Print the final bill and save it to a file."""
    if not bill_items:
        print("Cannot generate bill: no items added.")
        return
    text = build_bill_text(customer)
    print("\n" + text)
    subtotal, gst, grand_total = calculate_totals()
    print(f"Subtotal: {subtotal:.0f} | GST (5%): {gst:.2f}")
    print(f"Grand Total: {grand_total:.2f}")
    save_bill(text)


def read_quantity():
    """Read a whole-number quantity; returns None if not a number."""
    raw = input("Quantity: ").strip()
    try:
        return int(raw)
    except ValueError:
        print("Quantity must be a whole number.")
        return None


def show_menu():
    print("\n----- MENU -----")
    print("1. Add item")
    print("2. View bill")
    print("3. Generate bill")
    print("4. Exit")


def main():
    print("=== Simple Billing System ===")
    print("Products: " + ", ".join(f"{n} Rs.{p}" for n, p in PRODUCTS.items()))
    customer = input("Customer name: ").strip() or "Customer"

    while True:
        show_menu()
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            name = input("Add item: ")
            qty = read_quantity()
            if qty is not None:
                add_item(name, qty)
        elif choice == "2":
            view_bill()
        elif choice == "3":
            generate_bill(customer)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
