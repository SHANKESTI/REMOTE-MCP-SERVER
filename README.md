# Expense Tracker MCP Server

A **Model Context Protocol (MCP) server** that allows AI assistants such as Claude to manage personal expenses using natural language.
This server exposes tools for adding, listing, summarizing, editing, and deleting expenses while organizing them using structured categories and subcategories.

The project demonstrates how AI agents can interact with external tools and databases using MCP.

---

## Features

* Add new expenses
* List expenses within a date range
* Summarize spending by category
* Edit existing expense records
* Delete expense records
* Category and subcategory validation using `categories.json`
* SQLite database storage
* MCP resource for categories so AI assistants can understand valid expense types

---

## Project Structure

```
expense-mcp-server
│
├── main.py            # MCP server implementation
├── categories.json    # Expense categories and subcategories
├── expenses.db        # SQLite database (auto-generated)
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

---

## Technologies Used

* Python
* FastMCP
* SQLite
* Model Context Protocol (MCP)

---

## Installation

Clone the repository:

```
git clone https://github.com/your-username/expense-mcp-server.git
cd expense-mcp-server
```

Create and activate a virtual environment:

```
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the MCP Server

Start the server:

```
uv run fastmcp dev inspector main.py
uv run fastmcp run main.py          
```

Claude Desktop or any MCP-compatible client can now connect to the server and use the available tools.--  uv run fastmcp install claude-desktop main.py 

---

## Available MCP Tools

### Add Expense

Adds a new expense entry.

Example parameters:

```
{
  "date": "2026-03-07",
  "amount": 500,
  "category": "education",
  "subcategory": "courses",
  "note": "Udemy course"
}
```

---

### List Expenses

Retrieve all expenses between two dates.

Example:

```
{
  "start_date": "2026-03-01",
  "end_date": "2026-03-31"
}
```

---

### Summarize Expenses

Summarizes total spending grouped by category.

Example:

```
{
  "start_date": "2026-03-01",
  "end_date": "2026-03-31"
}
```

---

### Edit Expense

Update an existing expense record.

Example:

```
{
  "expense_id": 1,
  "date": "2026-03-07",
  "amount": 600,
  "category": "education",
  "subcategory": "courses",
  "note": "Updated Udemy course price"
}
```

---

### Delete Expense

Remove an expense entry.

Example:

```
{
  "expense_id": 1
}
```

---

## Categories Resource

The MCP server exposes a resource:

```
expense://categories
```

This allows AI assistants to access the list of valid categories and subcategories defined in `categories.json`.

---

## Example AI Interaction

User prompt:

```
Add 500 rupees for a Udemy course on March 7
```

AI calls:

```
add_expense(
  date="2026-03-07",
  amount=500,
  category="education",
  subcategory="courses",
  note="Udemy course"
)
```

---

## Future Improvements

* Automatic category detection from natural language
* Monthly analytics and spending insights
* Budget alerts and recommendations
* Remote MCP deployment with cloud hosting
* Web dashboard for expense visualization

---


