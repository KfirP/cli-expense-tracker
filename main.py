from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import typer


@dataclass
class Expense:
    """Class for keeping track of an expense"""
    id: int
    description: str
    amount: Decimal
    record_date: datetime

app = typer.Typer()

def load_data(filename: str = "expenses.csv") -> tuple[list[str], dict[int, Expense]]:
    expenses: dict[int, Expense] = {}
    headers: list[str] = []
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, [])
            for row in reader:
                expense = Expense(int(row[0]), row[3], Decimal(row[2]), datetime.fromisoformat(row[1]))
                expenses[expense.id] = expense
    except FileNotFoundError:
        pass
    return headers, expenses

def save_data(expenses: dict[int, Expense]) -> None:
    headers = ['id', 'Record Date', 'Amount', 'Description']
    data = [[expense.id, expense.record_date, f"{expense.amount:.2f}", expense.description] for expense in expenses.values()]
    with open("expenses.csv", mode='w', newline="", encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(data)

@app.command()
def add(description: str, amount: float):
    _, expenses = load_data()
    new_id = max(expenses, default=0) + 1
    expense = Expense(new_id, description, Decimal(str(amount)), datetime.now())
    expenses[expense.id] = expense
    save_data(expenses)
    print(f"# Expense added successfully (ID: {expense.id})")

@app.command("list")
def list_expenses():
    headers, expenses = load_data()
    print(f"# {'\t'.join(headers)}")
    for expense in expenses.values():
        print(f"# {expense.id}\t{expense.record_date}\t${expense.amount}\t{expense.description}")

if __name__ == "__main__":
    app()
