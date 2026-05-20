"""
FreshCart POS System
====================
IS 303 — Day 6: Functions Unlocked

Each department fills in their functions below.
The main() function at the bottom wires everything together.

DEPARTMENTS:
  Team 1: CHECKOUT  — scan_item(), calculate_subtotal()
  Team 2: INVENTORY — check_stock(), update_stock()
  Team 3: LOYALTY   — check_membership(), apply_discount()
  Team 4: RECEIPTS  — calculate_tax(), generate_receipt()
"""

# ============================================================
# SHARED DATA — Everyone uses these (do NOT edit)
# ============================================================

INVENTORY = {
    "apple":   {"price": 1.25, "stock": 50},
    "bread":   {"price": 3.49, "stock": 30},
    "milk":    {"price": 4.99, "stock": 20},
    "cheese":  {"price": 6.75, "stock": 15},
    "chips":   {"price": 3.99, "stock": 40},
    "soda":    {"price": 1.99, "stock": 60},
    "eggs":    {"price": 5.49, "stock": 25},
    "chicken": {"price": 8.99, "stock": 10},
}

MEMBERS = {
    "M001": {"name": "Sarah Johnson",  "discount": 0.10},
    "M002": {"name": "Mike Chen",      "discount": 0.15},
    "M003": {"name": "Emma Davis",     "discount": 0.05},
}

cart = []

# ============================================================
# 1: CHECKOUT — Scan items and calculate subtotal
# ============================================================
def scan_item(item, INVENTORY):
    
    if item in INVENTORY.keys():
        item_found = False
        for i in range(len(cart)):
            if item == cart[i]['scanned_item']:
                item_found = True
        if item_found:
            cart[i]['qty'] += 1
        else:
            scanned_item = item
            qty = 1
            price = INVENTORY[item]['price']
            scanned_item_dict = {"scanned_item":scanned_item, "qty":qty, "price":price}
            cart.append(scanned_item_dict)
    return cart



def calculate_subtotal(cart):
    subtotal = 0
    for i in range(len(cart)):
        category_price = cart[i]['price']*cart[i]['qty']
        subtotal += category_price
    return subtotal


# ============================================================
# 2: INVENTORY — Check and update stock levels
# ============================================================
def check_stock(item, INVENTORY):
    if item in INVENTORY:
        return INVENTORY[item]["stock"]
    

def update_stock(item, INVENTORY):
    if item in INVENTORY:
        INVENTORY[item]["stock"] -= 1
        



# ============================================================
# 3: LOYALTY — Membership lookup and discounts
# ============================================================
customer_id = input("Enter Membership ID (or enter to skip)" )

def check_membership(customer_id, MEMBERS):
    if customer_id in MEMBERS.keys():
        name = MEMBERS [customer_id]["name"]
        discount = MEMBERS [customer_id]["discount"]
        return f"Welcome back, {name}! Your discount is {discount*100}%."
    else:
        return "No membership found. No discount applied."

print(check_membership(customer_id, MEMBERS))

# ============================================================
# 4: RECEIPTS & TAX — Tax calculation and receipt
# ============================================================

def calculate_tax(amount):
    tax_rate = 0.07  # 7% sales tax
    return amount * tax_rate

def generate_receipt(cart, subtotal, discount, tax, total, customer_name):

    receipt = "\n--- FreshCart Receipt ---\n"
    receipt += f"Customer: {customer_name}\n\n"

    for item in cart:
        receipt += f"{item['name']} - ${item['price']:.2f}\n"

    receipt += f"\nSubtotal: ${subtotal:.2f}"
    receipt += f"\nDiscount: -${discount:.2f}"
    receipt += f"\nTax: ${tax:.2f}"
    receipt += f"\nTotal: ${total:.2f}"

    return receipt

# ============================================================
# MAIN — The CEO wires everything together
# (Do NOT edit until integration phase)
# ============================================================

def main():
    """
    Run the FreshCart POS system.
    This is where all department functions come together.
    """
    print("=" * 40)
    print("   Welcome to FreshCart Grocery!")
    print("=" * 40)

    cart = []

    # --- Step 1: Check membership (Team 3) ---
    customer_id = input("\nMembership ID (or Enter to skip): ").strip()
    if customer_id:
        member = check_membership(customer_id, MEMBERS)
    else:
        member = None

    if member:
        customer_name = member["name"]
        discount_rate = member["discount"]
        print(f"Welcome back, {customer_name}! "
              f"({discount_rate * 100:.0f}% member discount)")
    else:
        customer_name = "Guest"
        discount_rate = 0.0
        print("Shopping as Guest today.")

    # --- Step 2: Scan items (Team 1 + Team 2) ---
    while True:
        item = input("\nScan item (or 'done'): ").strip().lower()
        if item == "done":
            break

        # Check stock first (Team 2)
        stock = check_stock(item, INVENTORY)
        if stock <= 0:
            print(f"  Sorry, '{item}' is out of stock or not found!")
            continue

        # Scan the item (Team 1)
        scanned = scan_item(item, INVENTORY)
        if scanned is None:
            print(f"  Item '{item}' not found in system.")
            continue

        cart = scanned
        update_stock(item, INVENTORY)
        print(f"  Added: {item} — ${INVENTORY[item]['price']:.2f}")

    if not cart:
        print("\nNo items scanned. Goodbye!")
        return

    # --- Step 3: Calculate totals (Team 1 + Team 3 + Team 4) ---
    subtotal = calculate_subtotal(cart)
    discount = apply_discount(subtotal, discount_rate)
    after_discount = subtotal - discount
    tax = calculate_tax(after_discount)
    total = after_discount + tax

    # --- Step 4: Generate receipt (Team 4) ---
    receipt = generate_receipt(cart, subtotal, discount, tax,
                              total, customer_name)
    print(receipt)

    print("\nThank you for shopping at FreshCart!")


# --- Entry point ---
if __name__ == "__main__":
    main()