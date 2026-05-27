"""
Stock Portfolio Tracker
CodeAlpha Python Internship - Task 2
Author: Vaishnavi
"""

import csv
import json
import os
from datetime import datetime

# Hardcoded stock prices dictionary
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 320,
    "AMZN": 185,
    "META": 480,
    "NFLX": 620,
    "NVDA": 900,
    "RELIANCE": 2900,
    "TCS": 3800,
}

PORTFOLIO_FILE    = "my_portfolio.json"
TRANSACTION_FILE  = "transactions.json"


# ─────────────────────────────────────────────
#  PERSISTENT LOAD / SAVE
# ─────────────────────────────────────────────

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return {}


def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=4)


def load_transactions():
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as f:
            return json.load(f)
    return []


def save_transaction(action, symbol, qty, price):
    """Append one transaction record to history file."""
    history = load_transactions()
    history.append({
        "date":   datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "action": action,          # ADDED / REMOVED / UPDATED / SET
        "symbol": symbol,
        "qty":    qty,
        "price":  price,
        "value":  price * qty,
    })
    with open(TRANSACTION_FILE, "w") as f:
        json.dump(history, f, indent=4)


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def show_available_stocks(portfolio=None):
    print("\n" + "=" * 75)
    print(f"{'📈 AVAILABLE STOCKS':^75}")
    print("=" * 75)
    print(f"  {'Symbol':<10} {'Price (USD/INR)':>16} {'Your Holdings':>16} {'Total Value':>18}")
    print("-" * 75)
    for symbol, price in STOCK_PRICES.items():
        if portfolio and symbol in portfolio:
            qty = portfolio[symbol]
            holding  = f"✔ {qty} shares"
            total_val = f"₹/$ {price * qty:>10,.2f}"
        else:
            holding  = "—"
            total_val = "—"
        print(f"  {symbol:<10} ₹/$ {price:>10,.2f} {holding:>16} {total_val:>18}")
    print("=" * 75)


def display_portfolio(portfolio):
    if not portfolio:
        print("\n  ⚠️  Portfolio is empty.\n")
        return

    print("\n" + "=" * 65)
    print(f"{'📊 CURRENT PORTFOLIO SUMMARY':^65}")
    print("=" * 65)
    print(f"  {'#':<4} {'Stock':<10} {'Price':>10} {'Qty':>8} {'Total Value':>15} {'%Share':>10}")
    print("-" * 65)

    results, grand_total = calculate_portfolio(portfolio)
    for i, row in enumerate(results, 1):
        pct = (row["Total Value"] / grand_total * 100) if grand_total else 0
        print(f"  {i:<4} {row['Symbol']:<10} {row['Price']:>10,.2f}"
              f" {row['Quantity']:>8} {row['Total Value']:>15,.2f} {pct:>9.1f}%")

    print("-" * 65)
    print(f"  {'💰 TOTAL INVESTMENT VALUE':.<46} {grand_total:>15,.2f}")
    print("=" * 65)


# ─────────────────────────────────────────────
#  CALCULATIONS
# ─────────────────────────────────────────────

def calculate_portfolio(portfolio):
    results, total = [], 0
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        total += value
        results.append({"Symbol": symbol, "Price": price, "Quantity": qty, "Total Value": value})
    return results, total


# ─────────────────────────────────────────────
#  STOCK SEARCH
# ─────────────────────────────────────────────

def search_stock(portfolio):
    """Search stocks by partial symbol or name."""
    print("\n--- 🔍 STOCK SEARCH ---")
    keyword = input("  Enter symbol to search (e.g. AA, TS, RE): ").strip().upper()

    if not keyword:
        print("  ❌ Please enter at least 1 character.\n")
        return

    matches = {sym: price for sym, price in STOCK_PRICES.items() if keyword in sym}

    if not matches:
        print(f"  ❌ No stock found matching '{keyword}'.\n")
        return

    print(f"\n  🔎 Results for '{keyword}':\n")
    print(f"  {'Symbol':<10} {'Price':>14} {'Your Holdings':>16} {'Total Value':>18}")
    print("  " + "-" * 62)
    for sym, price in matches.items():
        if portfolio and sym in portfolio:
            qty       = portfolio[sym]
            holding   = f"✔ {qty} shares"
            total_val = f"₹/$ {price * qty:>10,.2f}"
        else:
            holding   = "—"
            total_val = "—"
        print(f"  {sym:<10} ₹/$ {price:>10,.2f} {holding:>16} {total_val:>18}")
    print()


# ─────────────────────────────────────────────
#  TRANSACTION HISTORY
# ─────────────────────────────────────────────

def view_transaction_history():
    """Display full transaction history."""
    history = load_transactions()

    print("\n" + "=" * 75)
    print(f"{'📅 TRANSACTION HISTORY':^75}")
    print("=" * 75)

    if not history:
        print("  ⚠️  No transactions recorded yet.\n")
        print("=" * 75)
        return

    print(f"  {'#':<4} {'Date & Time':<22} {'Action':<10} {'Symbol':<10} {'Qty':>6} {'Value':>14}")
    print("-" * 75)

    for i, tx in enumerate(reversed(history), 1):   # newest first
        action_icon = {"ADDED": "➕", "REMOVED": "➖", "SET": "✏️ ", "UPDATED": "🔄"}.get(tx["action"], "•")
        print(f"  {i:<4} {tx['date']:<22} {action_icon} {tx['action']:<8} "
              f"{tx['symbol']:<10} {tx['qty']:>6}   ₹/$ {tx['value']:>10,.2f}")

    print("=" * 75)
    print(f"  Total transactions: {len(history)}\n")


# ─────────────────────────────────────────────
#  PORTFOLIO OPERATIONS
# ─────────────────────────────────────────────

def add_or_update_stock(portfolio):
    print("\n--- ADD / UPDATE STOCK ---")
    show_available_stocks(portfolio)

    symbol = input("\n  Enter Stock Symbol: ").strip().upper()
    if symbol not in STOCK_PRICES:
        print(f"  ❌ '{symbol}' not found in available stocks.\n")
        return portfolio

    try:
        qty = int(input(f"  Enter quantity to ADD for {symbol}: ").strip())
        if qty <= 0:
            print("  ❌ Quantity must be positive.\n")
            return portfolio
    except ValueError:
        print("  ❌ Invalid number.\n")
        return portfolio

    action = "UPDATED" if symbol in portfolio else "ADDED"
    if symbol in portfolio:
        portfolio[symbol] += qty
        print(f"  ✅ {symbol} updated → Total: {portfolio[symbol]} shares")
    else:
        portfolio[symbol] = qty
        print(f"  ✅ {symbol} added with {qty} shares.")

    save_portfolio(portfolio)
    save_transaction(action, symbol, qty, STOCK_PRICES[symbol])
    print("  💾 Portfolio saved automatically.")
    return portfolio


def remove_stock(portfolio):
    print("\n--- REMOVE STOCK ---")
    if not portfolio:
        print("  ⚠️  Portfolio is empty.\n")
        return portfolio

    print("\n  📋 Your Current Holdings:")
    print("  " + "-" * 35)
    for sym, qty in portfolio.items():
        print(f"  {sym:<10} {qty:>6} shares  @ ₹/$ {STOCK_PRICES[sym]:,.2f}")
    print("  " + "-" * 35)

    symbol = input("\n  Enter Stock Symbol to remove: ").strip().upper()
    if symbol not in portfolio:
        print(f"  ❌ '{symbol}' not found in your portfolio.\n")
        return portfolio

    current_qty = portfolio[symbol]
    print(f"\n  You have {current_qty} shares of {symbol}.")
    print(f"  (Enter {current_qty} to remove all)\n")

    try:
        remove_qty = int(input(f"  Shares to remove (1 - {current_qty}): ").strip())
        if remove_qty <= 0:
            print("  ❌ Must be a positive number.\n")
            return portfolio
        if remove_qty > current_qty:
            print(f"  ❌ You only have {current_qty} shares.\n")
            return portfolio
    except ValueError:
        print("  ❌ Invalid number.\n")
        return portfolio

    confirm = input(f"\n  Confirm remove {remove_qty} shares of {symbol}? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("  ℹ️  Removal cancelled.")
        return portfolio

    if remove_qty == current_qty:
        del portfolio[symbol]
        print(f"  ✅ All {remove_qty} shares of {symbol} removed.")
    else:
        portfolio[symbol] -= remove_qty
        print(f"  ✅ {remove_qty} shares removed. Remaining: {portfolio[symbol]} shares.")

    save_portfolio(portfolio)
    save_transaction("REMOVED", symbol, remove_qty, STOCK_PRICES[symbol])
    print("  💾 Portfolio saved.")
    return portfolio


def update_quantity(portfolio):
    print("\n--- UPDATE EXACT QUANTITY ---")
    if not portfolio:
        print("  ⚠️  Portfolio is empty.\n")
        return portfolio

    symbol = input("  Enter Stock Symbol: ").strip().upper()
    if symbol not in portfolio:
        print(f"  ❌ '{symbol}' not in your portfolio. Use 'Add Stock' first.\n")
        return portfolio

    old_qty = portfolio[symbol]
    print(f"  Current quantity of {symbol}: {old_qty}")
    try:
        new_qty = int(input(f"  Enter NEW quantity for {symbol}: ").strip())
        if new_qty < 0:
            print("  ❌ Quantity cannot be negative.\n")
            return portfolio
    except ValueError:
        print("  ❌ Invalid number.\n")
        return portfolio

    portfolio[symbol] = new_qty
    save_portfolio(portfolio)
    save_transaction("SET", symbol, new_qty, STOCK_PRICES[symbol])
    print(f"  ✅ {symbol} quantity set to {new_qty}. Portfolio saved.")
    return portfolio


# ─────────────────────────────────────────────
#  EXPORT  (CSV + TXT)
# ─────────────────────────────────────────────

def export_portfolio(portfolio):
    if not portfolio:
        print("\n  ⚠️  Nothing to export — portfolio is empty.\n")
        return

    results, total = calculate_portfolio(portfolio)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_file = f"portfolio_export_{timestamp}.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Symbol", "Price", "Quantity", "Total Value"])
        writer.writeheader()
        writer.writerows(results)
        writer.writerow({})
        writer.writerow({"Symbol": "TOTAL", "Price": "", "Quantity": "", "Total Value": total})

    txt_file = f"portfolio_export_{timestamp}.txt"
    with open(txt_file, "w") as f:
        f.write("=" * 65 + "\n")
        f.write(f"{'STOCK PORTFOLIO TRACKER — CodeAlpha':^65}\n")
        f.write(f"  Exported: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write("=" * 65 + "\n")
        f.write(f"  {'Stock':<10} {'Price':>10} {'Qty':>8} {'Total Value':>15}\n")
        f.write("-" * 65 + "\n")
        for row in results:
            f.write(f"  {row['Symbol']:<10} {row['Price']:>10,.2f}"
                    f" {row['Quantity']:>8} {row['Total Value']:>15,.2f}\n")
        f.write("-" * 65 + "\n")
        f.write(f"  TOTAL INVESTMENT: {total:>,.2f}\n")
        f.write("=" * 65 + "\n")

    print(f"\n  ✅ Exported → {csv_file}")
    print(f"  ✅ Exported → {txt_file}\n")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def main():
    print("\n" + "=" * 65)
    print(f"{'💹 STOCK PORTFOLIO TRACKER':^65}")
    print(f"{'CodeAlpha Python Internship — Task 2':^65}")
    print("=" * 65)

    portfolio = load_portfolio()
    if portfolio:
        print(f"\n  📂 Previous portfolio loaded! ({len(portfolio)} stocks found)")
    else:
        print("\n  📂 No saved portfolio found. Starting fresh.")

    while True:
        print("\n" + "─" * 40)
        print("  MENU")
        print("─" * 40)
        print("  1. 📋 View Portfolio")
        print("  2. ➕ Add / Update Stock")
        print("  3. ✏️  Set Exact Quantity")
        print("  4. ❌ Remove Stock")
        print("  5. 📈 View Available Stocks")
        print("  6. 🔍 Search Stock")
        print("  7. 📅 Transaction History")
        print("  8. 💾 Export to CSV & TXT")
        print("  9. 🚪 Exit")
        print("─" * 40)

        choice = input("  Enter choice (1-9): ").strip()

        if   choice == "1": display_portfolio(portfolio)
        elif choice == "2": portfolio = add_or_update_stock(portfolio)
        elif choice == "3": portfolio = update_quantity(portfolio)
        elif choice == "4": portfolio = remove_stock(portfolio)
        elif choice == "5": show_available_stocks(portfolio)
        elif choice == "6": search_stock(portfolio)
        elif choice == "7": view_transaction_history()
        elif choice == "8": export_portfolio(portfolio)
        elif choice == "9":
            print("\n  👋 Goodbye! Your portfolio is saved.\n")
            break
        else:
            print("  ❌ Invalid choice. Enter 1-9.\n")


if __name__ == "__main__":
    main()