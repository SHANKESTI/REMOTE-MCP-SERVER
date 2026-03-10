from fastmcp import FastMCP
import os
import sqlite3
import json

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "expenses.db")
CATEGORIES_PATH = os.path.join(BASE_DIR, "categories.json")

# -----------------------------
# Create MCP Server
# -----------------------------
mcp = FastMCP("ExpenseTracker")

# -----------------------------
# Load Categories
# -----------------------------
def load_categories():
    if not os.path.exists(CATEGORIES_PATH):
        return {}
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CATEGORIES = load_categories()


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
        """)

init_db()


# -----------------------------
# Validate Category
# -----------------------------
def validate_category(category, subcategory):

    category = category.lower()

    if category not in CATEGORIES:
        return False, f"Invalid category '{category}'. Available: {list(CATEGORIES.keys())}"

    if subcategory:
        if subcategory not in CATEGORIES[category]:
            return False, f"Invalid subcategory '{subcategory}' for '{category}'. Available: {CATEGORIES[category]}"

    return True, ""


# -----------------------------
# 1️⃣ Add Expense
# -----------------------------
@mcp.tool()
def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    """
    Add a new expense entry.

    Category and subcategory must exist in categories.json
    """

    valid, message = validate_category(category, subcategory)

    if not valid:
        return {"status": "error", "message": message}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category.lower(), subcategory, note)
        )
        conn.commit()

    return {
        "status": "success",
        "expense_id": cursor.lastrowid,
        "category": category,
        "subcategory": subcategory
    }


# -----------------------------
# 2️⃣ List Expenses
# -----------------------------
@mcp.tool()
def list_expenses(start_date: str, end_date: str):
    """
    List expenses between two dates.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
            """,
            (start_date, end_date)
        )

        columns = [c[0] for c in cur.description]
        rows = cur.fetchall()

    return [dict(zip(columns, row)) for row in rows]


# -----------------------------
# 3️⃣ Summarize Expenses
# -----------------------------
@mcp.tool()
def summarize(start_date: str, end_date: str, category: str | None = None):
    """
    Summarize total expenses by category.
    """

    query = """
    SELECT category, SUM(amount) as total_amount
    FROM expenses
    WHERE date BETWEEN ? AND ?
    """

    params = [start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " GROUP BY category ORDER BY total_amount DESC"

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(query, params)

        columns = [c[0] for c in cur.description]
        rows = cur.fetchall()

    return [dict(zip(columns, row)) for row in rows]


# -----------------------------
# 4️⃣ Edit Expense
# -----------------------------
@mcp.tool()
def edit_expense(expense_id: int, date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    """
    Edit an existing expense entry.
    """

    valid, message = validate_category(category, subcategory)

    if not valid:
        return {"status": "error", "message": message}

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            UPDATE expenses
            SET date = ?, amount = ?, category = ?, subcategory = ?, note = ?
            WHERE id = ?
            """,
            (date, amount, category.lower(), subcategory, note, expense_id)
        )
        conn.commit()

    return {"status": "updated", "expense_id": expense_id}


# -----------------------------
# 5️⃣ Delete Expense
# -----------------------------
@mcp.tool()
def delete_expense(expense_id: int):
    """
    Delete an expense from the database.
    """

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )
        conn.commit()

    return {"status": "deleted", "expense_id": expense_id}


# -----------------------------
# MCP Resource for Categories
# -----------------------------
@mcp.resource("expense://categories", mime_type="application/json")
def categories_resource():
    """
    Provide categories.json to Claude.
    """

    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# Run MCP Server
# -----------------------------
if __name__ == "__main__":
    print("ExpenseTracker MCP Server Running...")
    mcp.run()