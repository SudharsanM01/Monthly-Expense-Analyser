import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar

DB_NAME = "expenses.db"


class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Monthly Expense Analysis")
        self.root.geometry("1050x700")
        self.root.minsize(950, 620)

        self.current_user = None
        self.setup_database()
        self.show_login()

    def connect_db(self):
        return sqlite3.connect(DB_NAME)

    def setup_database(self):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN / ACCOUNT ----------------

    def show_login(self):
        self.clear_window()

        frame = tk.Frame(self.root, padx=40, pady=40)
        frame.pack(expand=True)

        tk.Label(
            frame, text="Monthly Expense Analysis",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 10))

        tk.Label(
            frame, text="AI-Based Smart Savings Recommendation System",
            font=("Arial", 11)
        ).pack(pady=(0, 25))

        tk.Label(frame, text="Username").pack(anchor="w")
        self.login_username = tk.Entry(frame, width=35)
        self.login_username.pack(pady=(3, 12))

        tk.Label(frame, text="Password").pack(anchor="w")
        self.login_password = tk.Entry(frame, width=35, show="*")
        self.login_password.pack(pady=(3, 20))

        tk.Button(
            frame, text="Login", width=18,
            bg="#2563eb", fg="white",
            command=self.login
        ).pack(pady=5)

        tk.Button(
            frame, text="Create Account", width=18,
            command=self.show_register
        ).pack(pady=5)

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password.")
            return

        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT username FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cur.fetchone()
        conn.close()

        if result:
            self.current_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_register(self):
        self.clear_window()

        frame = tk.Frame(self.root, padx=40, pady=40)
        frame.pack(expand=True)

        tk.Label(
            frame, text="Create Account",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 25))

        tk.Label(frame, text="Username").pack(anchor="w")
        self.reg_username = tk.Entry(frame, width=35)
        self.reg_username.pack(pady=(3, 12))

        tk.Label(frame, text="Password").pack(anchor="w")
        self.reg_password = tk.Entry(frame, width=35, show="*")
        self.reg_password.pack(pady=(3, 12))

        tk.Label(frame, text="Confirm Password").pack(anchor="w")
        self.reg_confirm = tk.Entry(frame, width=35, show="*")
        self.reg_confirm.pack(pady=(3, 20))

        tk.Button(
            frame, text="Create Account", width=18,
            bg="#16a34a", fg="white",
            command=self.create_account
        ).pack(pady=5)

        tk.Button(
            frame, text="Back to Login", width=18,
            command=self.show_login
        ).pack(pady=5)

    def create_account(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if not username or not password:
            messagebox.showwarning("Account", "Please fill all fields.")
            return

        if password != confirm:
            messagebox.showerror("Account", "Passwords do not match.")
            return

        conn = self.connect_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username, password) VALUES(?, ?)",
                (username, password)
            )
            conn.commit()
            messagebox.showinfo(
                "Account Created",
                "Account created successfully. You can now login."
            )
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Account", "Username already exists.")
        finally:
            conn.close()

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_window()

        top = tk.Frame(self.root, bg="#1e3a8a", padx=15, pady=12)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"Monthly Expense Analysis  |  User: {self.current_user}",
            bg="#1e3a8a", fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left")

        tk.Button(
            top, text="Logout",
            command=self.logout
        ).pack(side="right")

        form = tk.LabelFrame(
            self.root, text="Add Expense",
            padx=12, pady=12
        )
        form.pack(fill="x", padx=15, pady=12)

        tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(form, width=18)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form, text="Category").grid(row=0, column=1, sticky="w")
        self.category_combo = ttk.Combobox(
            form,
            values=[
                "Food", "Transport", "Shopping", "Bills",
                "Entertainment", "Education", "Health",
                "Rent", "Travel", "Other"
            ],
            width=18,
            state="readonly"
        )
        self.category_combo.grid(row=1, column=1, padx=5, pady=5)
        self.category_combo.set("Food")

        tk.Label(form, text="Description").grid(row=0, column=2, sticky="w")
        self.description_entry = tk.Entry(form, width=28)
        self.description_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(form, text="Amount").grid(row=0, column=3, sticky="w")
        self.amount_entry = tk.Entry(form, width=15)
        self.amount_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(
            form, text="Add Expense",
            bg="#2563eb", fg="white",
            command=self.add_expense
        ).grid(row=1, column=4, padx=10)

        # Month / budget
        controls = tk.Frame(self.root)
        controls.pack(fill="x", padx=15, pady=5)

        tk.Label(controls, text="Analysis Month (YYYY-MM):").pack(side="left")
        self.month_entry = tk.Entry(controls, width=10)
        self.month_entry.insert(0, datetime.now().strftime("%Y-%m"))
        self.month_entry.pack(side="left", padx=5)

        tk.Label(controls, text="Monthly Budget:").pack(side="left", padx=(20, 0))
        self.budget_entry = tk.Entry(controls, width=12)
        self.budget_entry.insert(0, "20000")
        self.budget_entry.pack(side="left", padx=5)

        tk.Button(
            controls, text="Refresh",
            command=self.refresh_expenses
        ).pack(side="left", padx=5)

        tk.Button(
            controls, text="AI Savings Analysis",
            bg="#16a34a", fg="white",
            command=self.ai_savings_analysis
        ).pack(side="left", padx=5)

        # Expense table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("id", "date", "category", "description", "amount")
        self.tree = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", height=14
        )

        headings = {
            "id": "ID",
            "date": "Date",
            "category": "Category",
            "description": "Description",
            "amount": "Amount"
        }

        widths = {
            "id": 55,
            "date": 110,
            "category": 130,
            "description": 350,
            "amount": 120
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=15, pady=(0, 15))

        self.summary_label = tk.Label(
            bottom, text="Total: ₹0.00",
            font=("Arial", 13, "bold")
        )
        self.summary_label.pack(side="left")

        tk.Button(
            bottom, text="Delete Selected",
            bg="#dc2626", fg="white",
            command=self.delete_selected
        ).pack(side="right")

        self.refresh_expenses()

    def logout(self):
        self.current_user = None
        self.show_login()

    # ---------------- EXPENSE OPERATIONS ----------------

    def add_expense(self):
        date_text = self.date_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        amount_text = self.amount_entry.get().strip()

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Use date format YYYY-MM-DD."
            )
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid amount greater than 0."
            )
            return

        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO expenses
            (username, date, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.current_user,
            date_text,
            category,
            description,
            amount
        ))
        conn.commit()
        conn.close()

        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.refresh_expenses()

    def refresh_expenses(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        month = self.month_entry.get().strip()

        if len(month) != 7:
            month = datetime.now().strftime("%Y-%m")
            self.month_entry.delete(0, tk.END)
            self.month_entry.insert(0, month)

        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, date, category, description, amount
            FROM expenses
            WHERE username=? AND substr(date, 1, 7)=?
            ORDER BY date DESC, id DESC
        """, (self.current_user, month))

        rows = cur.fetchall()
        conn.close()

        total = 0

        for row in rows:
            self.tree.insert(
                "", "end",
                values=(row[0], row[1], row[2], row[3], f"₹{row[4]:,.2f}")
            )
            total += row[4]

        self.summary_label.config(
            text=f"{month} Total: ₹{total:,.2f}  |  {len(rows)} expenses"
        )

    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Delete",
                "Please select an expense first."
            )
            return

        item = self.tree.item(selected[0])
        expense_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete the selected expense?"
        )

        if not confirm:
            return

        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM expenses WHERE id=? AND username=?",
            (expense_id, self.current_user)
        )
        conn.commit()
        conn.close()

        self.refresh_expenses()

    # ---------------- AI / SMART ANALYSIS ----------------

    def get_month_data(self, month):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses
            WHERE username=? AND substr(date, 1, 7)=?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (self.current_user, month))

        category_rows = cur.fetchall()

        cur.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE username=? AND substr(date, 1, 7)=?
        """, (self.current_user, month))

        total = cur.fetchone()[0]

        conn.close()
        return total, category_rows

    def previous_month(self, month):
        try:
            year, mon = map(int, month.split("-"))
            if mon == 1:
                year -= 1
                mon = 12
            else:
                mon -= 1
            return f"{year:04d}-{mon:02d}"
        except ValueError:
            return None

    def ai_savings_analysis(self):
        month = self.month_entry.get().strip()

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            messagebox.showerror(
                "Invalid Month",
                "Enter the month as YYYY-MM, for example 2026-10."
            )
            return

        try:
            budget = float(self.budget_entry.get().strip())
            if budget <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Budget",
                "Enter a valid monthly budget."
            )
            return

        total, categories = self.get_month_data(month)
        previous = self.previous_month(month)
        prev_total = 0

        if previous:
            prev_total, _ = self.get_month_data(previous)

        result = tk.Toplevel(self.root)
        result.title("AI Savings Analysis")
        result.geometry("760x650")
        result.minsize(650, 550)

        text = tk.Text(
            result,
            wrap="word",
            font=("Arial", 11),
            padx=15,
            pady=15
        )
        text.pack(fill="both", expand=True)

        text.insert(tk.END, f"AI SAVINGS ANALYSIS - {month}\n")
        text.insert(tk.END, "=" * 65 + "\n\n")

        text.insert(tk.END, f"Total spending: ₹{total:,.2f}\n")
        text.insert(tk.END, f"Monthly budget: ₹{budget:,.2f}\n")
        text.insert(tk.END, f"Remaining budget: ₹{budget - total:,.2f}\n\n")

        if total == 0:
            text.insert(
                tk.END,
                "No expenses were found for this month.\n"
                "Add some expenses to receive personalized recommendations.\n"
            )
            text.config(state="disabled")
            return

        # Budget analysis
        if total > budget:
            over = total - budget
            text.insert(
                tk.END,
                f"⚠ Budget Alert: You exceeded your budget by ₹{over:,.2f}.\n\n"
            )
        else:
            saved = budget - total
            text.insert(
                tk.END,
                f"✓ Budget Status: You are within budget by ₹{saved:,.2f}.\n\n"
            )

        # Category analysis
        text.insert(tk.END, "CATEGORY-WISE SPENDING\n")
        text.insert(tk.END, "-" * 65 + "\n")

        for category, amount, count in categories:
            percentage = (amount / total) * 100
            text.insert(
                tk.END,
                f"{category}: ₹{amount:,.2f} "
                f"({percentage:.1f}%) - {count} transaction(s)\n"
            )

        text.insert(tk.END, "\n")

        # Highest category
        top_category, top_amount, top_count = categories[0]
        top_percentage = (top_amount / total) * 100

        text.insert(tk.END, "AI INSIGHT\n")
        text.insert(tk.END, "-" * 65 + "\n")
        text.insert(
            tk.END,
            f"Highest spending category: {top_category}\n"
            f"Amount: ₹{top_amount:,.2f}\n"
            f"Share of total spending: {top_percentage:.1f}%\n\n"
        )

        # Month comparison
        if previous:
            text.insert(tk.END, "MONTH-TO-MONTH COMPARISON\n")
            text.insert(tk.END, "-" * 65 + "\n")

            if prev_total == 0:
                text.insert(
                    tk.END,
                    f"No previous-month spending data was found for {previous}.\n\n"
                )
            else:
                difference = total - prev_total
                percentage_change = (difference / prev_total) * 100

                if difference > 0:
                    text.insert(
                        tk.END,
                        f"Spending increased by ₹{difference:,.2f} "
                        f"({percentage_change:.1f}%) compared with {previous}.\n\n"
                    )
                elif difference < 0:
                    text.insert(
                        tk.END,
                        f"Great! Spending decreased by ₹{abs(difference):,.2f} "
                        f"({abs(percentage_change):.1f}%) compared with {previous}.\n\n"
                    )
                else:
                    text.insert(
                        tk.END,
                        f"Spending is unchanged compared with {previous}.\n\n"
                    )

        # Smart recommendations
        text.insert(tk.END, "SMART SAVINGS RECOMMENDATIONS\n")
        text.insert(tk.END, "-" * 65 + "\n")

        recommendations = []

        if top_percentage >= 30:
            recommendations.append(
                f"• {top_category} is your biggest expense. "
                f"Try reducing this category by 10-20%."
            )
        elif top_percentage >= 20:
            recommendations.append(
                f"• {top_category} takes a significant part of your spending. "
                f"Set a weekly limit for this category."
            )

        category_rules = {
            "Food": "• Food: reduce food delivery/eating-out frequency and plan meals.",
            "Shopping": "• Shopping: use a 24-hour waiting rule before non-essential purchases.",
            "Transport": "• Transport: compare public transport, walking, cycling, or shared rides.",
            "Entertainment": "• Entertainment: set a monthly entertainment limit.",
            "Bills": "• Bills: review recurring subscriptions and unnecessary services.",
            "Travel": "• Travel: plan trips early and compare transport/accommodation costs.",
            "Education": "• Education: compare digital and offline learning resources before buying.",
            "Health": "• Health: maintain necessary health spending, but compare prices where appropriate.",
            "Rent": "• Rent: this is usually a fixed expense; focus savings on flexible categories.",
        }

        if top_category in category_rules:
            recommendations.append(category_rules[top_category])

        if total > budget:
            recommendations.append(
                f"• Reduce flexible spending by at least ₹{(total-budget):,.2f} "
                f"to return within your budget."
            )

        if prev_total > 0 and total > prev_total * 1.10:
            recommendations.append(
                "• Your spending increased by more than 10% from last month. "
                "Review the categories that increased most."
            )

        if not recommendations:
            recommendations.append(
                "• Your spending pattern is relatively balanced. "
                "Continue tracking expenses and keep a monthly savings target."
            )

        # Potential savings estimate
        flexible_target = min(top_amount * 0.15, max(total * 0.10, 0))
        if flexible_target > 0:
            recommendations.append(
                f"• Suggested savings opportunity: approximately "
                f"₹{flexible_target:,.2f} per month by reducing avoidable spending."
            )

        for item in recommendations:
            text.insert(tk.END, item + "\n")

        text.insert(tk.END, "\n")
        text.insert(
            tk.END,
            "Note: This is a rule-based AI-style recommendation engine using "
            "your expense data, category patterns, budget status, and previous-month comparison. "
            "It does not send your data to an external AI service.\n"
        )

        text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
