import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime

conn = sqlite3.connect('expense_data.db')
cursor = conn.cursor()

def create_table():
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT,
            label TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL
             
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            member_name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shared_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            date TEXT,
            payer TEXT,
            description TEXT,
            amount REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            date TEXT,
            payer TEXT,
            receiver TEXT,
            amount REAL
        )
    ''')

    conn.commit()
payments = {}

def record_expense(description, amount, category):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)', (description, amount, category))
    conn.commit()
    conn.close()
    
    update_treeview()

def list_expenses():
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    return expenses

def edit_expense(expense_id, new_description, new_amount, new_category):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET description=?, amount=?, category=? WHERE id=?',
                   (new_description, new_amount, new_category, expense_id))
    conn.commit()
    conn.close()
 
    update_treeview()

def summarize_expenses_page():
    summarize_window = tk.Toplevel(root)
    summarize_window.title('Summarize Expenses')
    summarize_window.geometry("700x300")

    # Get and summarize expenses
    expenses = list_expenses()
    summary = summarize_expenses(expenses)

    # Display summary
    summary_label = tk.Label(summarize_window, text='Expense Summary:')
    summary_label.place(x=100,y=50)

    for category, total_amount in summary.items():
        summary_text = f"{category}: ${total_amount:.2f}"
        category_label = tk.Label(summarize_window, text=summary_text)
        category_label.place(x=200,y=50)

# Function to summarize expenses
def summarize_expenses(expenses):
    summary = {}

    for expense in expenses:
        category = expense[3]  # Assuming the category is at index 3
        amount = expense[2]  # Assuming the amount is at index 2

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    return summary

def delete_expense(expense_id):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
    conn.commit()
    conn.close()
    
    update_treeview()

def update_treeview():
    # Clear existing data in the treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Retrieve and insert new data into the treeview
    expenses = list_expenses()
    for expense in expenses:
        treeview.insert("", "end", values=expense)



def record_expense_fn(description, amount, category):
    if not description or not amount or not category:
        messagebox.showerror('Error', 'Please fill in all fields.')
        return

    try:
        amount_float = float(amount)
    except ValueError:
        messagebox.showerror('Error', 'Invalid amount. Please enter a valid number.')
        return

    # Assuming you have a function named 'record_expense' for recording the expense
    try:
        record_expense(description, amount_float, category)
        messagebox.showinfo('Success', 'Expense recorded successfully!')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to record expense: {str(e)}')

# Example of using the function



# Function to handle the "Record Expense" option
def record_expense_page():
    record_window = tk.Toplevel(root)
    record_window.title('Record Expense')
    record_window.geometry("700x300")

    description_label = tk.Label(record_window, text='Description:')
    description_label.place(x=100,y=50)
    description_entry = tk.Entry(record_window)
    description_entry.place(x=370,y=53)

    amount_label = tk.Label(record_window, text='Amount:')
    amount_label.place(x=100,y=100)
    amount_entry = tk.Entry(record_window)
    amount_entry.place(x=370,y=103)

    # Dropdown menu for selecting expense categories
    category_label = tk.Label(record_window, text='Category:')
    category_label.place(x=100,y=150)
    categories = ["Food", "Bills", "Rent", "Entertainment", "Others"]
    category_var = tk.StringVar(record_window)
    category_var.set(categories[0])
    category_dropdown = tk.OptionMenu(record_window, category_var, *categories)
    category_dropdown.place(x=370,y=153)

    record_button = tk.Button(record_window, text='Record Expense', command=lambda: record_expense_fn(
        description_entry.get(),
        amount_entry.get(),
        category_var.get()
        
    ))
    record_button.place(x=300,y=200)

# Function to handle the "List Expenses" option
def list_expenses_page():
    expenses = list_expenses()
    update_treeview()



# Function to handle the "Edit Expense" option
def edit_expense_page():
    edit_window = tk.Toplevel(root)
    edit_window.title('Edit Expense')
    edit_window.geometry("700x300")

    expense_id_label = tk.Label(edit_window, text='Expense ID:')
    expense_id_label.place(x=100, y=50)
    expense_id_entry = tk.Entry(edit_window)
    expense_id_entry.place(x=370, y=53)

    new_description_label = tk.Label(edit_window, text='New Description:')
    new_description_label.place(x=100, y=100)
    new_description_entry = tk.Entry(edit_window)
    new_description_entry.place(x=370, y=103)

    new_amount_label = tk.Label(edit_window, text='New Amount:')
    new_amount_label.place(x=100, y=150)
    new_amount_entry = tk.Entry(edit_window)
    new_amount_entry.place(x=370, y=153)

    # Dropdown menu for selecting new expense categories
    new_category_label = tk.Label(edit_window, text='New Category:')
    new_category_label.place(x=100, y=200)
    categories = ["Food", "Bills", "Rent", "Entertainment", "Others"]
    new_category_var = tk.StringVar(edit_window)
    new_category_var.set(categories[0])
    new_category_dropdown = tk.OptionMenu(edit_window, new_category_var, *categories)
    new_category_dropdown.place(x=370, y=200)

    def edit_expense_safe():
        try:
            expense_id = int(expense_id_entry.get())
            new_description = new_description_entry.get()
            new_amount = float(new_amount_entry.get())
            new_category = new_category_var.get()

            # Additional checks if needed (e.g., validation of expense_id)
            # ...

            # Assuming you have a function named 'edit_expense' for editing the expense
            edit_expense(expense_id, new_description, new_amount, new_category)
            messagebox.showinfo('Success', 'Expense edited successfully!')
            edit_window.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please enter valid values for Expense ID and Amount.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to edit expense: {str(e)}')

    edit_button = tk.Button(edit_window, text='Edit Expense', command=edit_expense_safe)
    edit_button.place(x=300, y=250)



def delete_expense_fn(expense_id_entry):
    try:
        expense_id = int(expense_id_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Invalid expense ID. Please enter a valid number.')
        return

    if not expense_id:
        messagebox.showerror('Error', 'Please fill in the field.')
        return

    # Your logic for deleting the expense goes here
    delete_expense(expense_id)
    messagebox.showinfo('Success', 'Expense deleted successfully!')

# Function to handle the "Delete Expense" option
def delete_expense_page():
    delete_window = tk.Toplevel(root)
    delete_window.title('Delete Expense')
    delete_window.geometry("700x300")

    expense_id_label = tk.Label(delete_window, text='Expense ID:')
    expense_id_label.place(x=100, y=50)
    expense_id_entry = tk.Entry(delete_window)
    expense_id_entry.place(x=370, y=53)

    # Pass expense_id_entry as an argument to the lambda function
    delete_button = tk.Button(delete_window, text='Delete Expense', command=lambda: delete_expense_fn(expense_id_entry))
    delete_button.place(x=300, y=200)



def create_budget_page():
    create_budget_window = tk.Toplevel(root)
    create_budget_window.title('Create Budget')
    create_budget_window.geometry("700x300")

    # Get budget categories
    budget_categories = ["Food", "Bills", "Rent", "Entertainment", "Others"]

    # Dropdown menu for selecting budget category
    category_label = tk.Label(create_budget_window, text='Select Budget Category:')
    category_label.place(x=100, y=50)
    category_var = tk.StringVar(create_budget_window)
    category_var.set(budget_categories[0])
    category_dropdown = tk.OptionMenu(create_budget_window, category_var, *budget_categories)
    category_dropdown.place(x=370, y=50)

    # Entry for entering budget amount
    amount_label = tk.Label(create_budget_window, text='Enter Budget Amount:')
    amount_label.place(x=100, y=100)
    amount_entry = tk.Entry(create_budget_window)
    amount_entry.place(x=370, y=103)

    def save_budget_safe():
        try:
            category = category_var.get()
            amount = float(amount_entry.get())

            # Additional checks if needed (e.g., validation of category or amount)
            # ...

            # Assuming you have a function named 'save_budget' for saving the budget
            save_budget(category, amount)
            messagebox.showinfo('Success', 'Budget created successfully!')
            create_budget_window.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please enter a valid number for Budget Amount.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create budget: {str(e)}')

    # Button to create the budget
    create_button = tk.Button(create_budget_window, text='Create Budget', command=save_budget_safe)
    create_button.place(x=300, y=200)


# Function to save the budget in the database
def save_budget(category, amount):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()

    # Check if a budget for the category already exists
    cursor.execute('SELECT * FROM budgets WHERE category=?', (category,))
    existing_budget = cursor.fetchone()

    if existing_budget:
        # Update existing budget
        cursor.execute('UPDATE budgets SET amount=? WHERE category=?', (amount, category))
    else:
        # Insert new budget
        cursor.execute('INSERT INTO budgets (category, amount) VALUES (?, ?)', (category, amount))

    conn.commit()
    conn.close()


# ... (other functions)

# Function to handle the "Create Budget" option
# Function to handle the "Create Budget" option
def create_budget_option():
    create_budget_page()

def view_budgets_page():
    view_budgets_window = tk.Toplevel(root)
    view_budgets_window.title('View Budgets')
    view_budgets_window.geometry("700x300")

    # Retrieve and display budget data from the database
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budgets')
    budgets = cursor.fetchall()
    conn.close()

    # Display budget data in a listbox or any other suitable widget
    for budget in budgets:
        budget_info = f"Category: {budget[1]}, Amount: {budget[2]}"
        tk.Label(view_budgets_window, text=budget_info).pack(pady=10)
# ... (other code)


def edit_budget_page():
    edit_budget_window = tk.Toplevel(root)
    edit_budget_window.title('Edit Budget')
    edit_budget_window.geometry("700x300")

    budget_id_label = tk.Label(edit_budget_window, text='Budget ID:')
    budget_id_label.place(x=100, y=50)
    budget_id_entry = tk.Entry(edit_budget_window)
    budget_id_entry.place(x=370, y=53)

    new_amount_label = tk.Label(edit_budget_window, text='New Amount:')
    new_amount_label.place(x=100, y=100)
    new_amount_entry = tk.Entry(edit_budget_window)
    new_amount_entry.place(x=370, y=103)

    # Dropdown menu for selecting the budget category to edit
    category_label = tk.Label(edit_budget_window, text='Budget Category:')
    category_label.place(x=100, y=150)

    # Retrieve and display budget categories in the dropdown
    categories = get_budget_categories()
    category_var = tk.StringVar(edit_budget_window)
    category_var.set(categories[0] if categories else "")
    category_dropdown = tk.OptionMenu(edit_budget_window, category_var, *categories)
    category_dropdown.place(x=370, y=150)

    def edit_budget_safe():
        try:
            budget_id = int(budget_id_entry.get())
            new_amount = float(new_amount_entry.get())
            category = category_var.get()

            # Additional checks if needed (e.g., validation of budget_id or new_amount)
            # ...

            # Assuming you have a function named 'edit_budget' for editing the budget
            edit_budget(budget_id, new_amount, category)
            messagebox.showinfo('Success', 'Budget edited successfully!')
            edit_budget_window.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please enter valid values for Budget ID and Amount.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to edit budget: {str(e)}')

    edit_button = tk.Button(edit_budget_window, text='Edit Budget', command=edit_budget_safe)
    edit_button.place(x=300, y=200)


# Add this function to get budget categories
def get_budget_categories():
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM budgets')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# Add this function to edit a budget
def edit_budget(budget_id, new_amount, category):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE budgets SET amount=? WHERE id=?', (new_amount, budget_id))
    conn.commit()
    conn.close()
    
    update_treeview()  # Update the treeview to reflect the changes



def label_expense_page():
    label_window = tk.Toplevel(root)
    label_window.title('Label Expense')
    label_window.geometry("700x300")

    expense_id_label = tk.Label(label_window, text='Expense ID:')
    expense_id_label.place(x=100, y=50)
    expense_id_entry = tk.Entry(label_window)
    expense_id_entry.place(x=370, y=53)

    label_label = tk.Label(label_window, text='Label:')
    label_label.place(x=100, y=100)
    label_entry = tk.Entry(label_window)
    label_entry.place(x=370, y=103)

    def label_expense_safe():
        try:
            expense_id = int(expense_id_entry.get())
            label = label_entry.get()

            # Additional checks if needed (e.g., validation of expense_id or label)
            # ...

            # Assuming you have a function named 'label_expense' for labeling the expense
            label_expense(expense_id, label)
            messagebox.showinfo('Success', 'Expense labeled successfully!')
            label_window.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please enter valid values for Expense ID.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to label expense: {str(e)}')

    label_button = tk.Button(label_window, text='Label Expense', command=label_expense_safe)
    label_button.place(x=300, y=200)


# Function to handle the labeling of expenses
def label_expense(expense_id, label):
    conn = sqlite3.connect('expense_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE expenses SET label=? WHERE id=?', (label, expense_id))
    conn.commit()
    conn.close()
  
    update_treeview()


def send_notification_page():
    notification_window = tk.Toplevel(root)
    notification_window.title('Send Notification')
    notification_window.geometry("700x300")

    message_label = tk.Label(notification_window, text='Enter Notification Message:')
    message_label.place(x=100,y=50)

    message_entry = tk.Entry(notification_window)
    message_entry.place(x=370,y=53)

    send_button = tk.Button(notification_window, text='Send Notification', command=lambda: send_notification(message_entry.get()))
    send_button.place(x=300,y=200)

def send_notification(message):
    messagebox.showinfo('Notification', message)


def shared_expense_tracking_page():



    def create_group(group_name):
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO groups (group_name) VALUES (?)', (group_name,))
        conn.commit()
        conn.close()

    def create_group_page():
        create_group_window = tk.Toplevel(root)
        create_group_window.title('Create Group')
        create_group_window.geometry("700x300")

        group_name_label = tk.Label(create_group_window, text='Group Name:')
        group_name_label.place(x=100, y=50)
        group_name_entry = tk.Entry(create_group_window)
        group_name_entry.place(x=370, y=53)

        def create_group_safe():
            try:
                group_name = group_name_entry.get()

                # Check if the group name is empty
                if not group_name:
                    messagebox.showerror('Error', 'Group Name cannot be empty.')
                    return

                # Additional checks if needed (e.g., validation of group_name)
                # ...

                # Assuming you have a function named 'create_group' for creating the group
                create_group(group_name)
                messagebox.showinfo('Success', 'Group created successfully!')
                create_group_window.destroy()
            except ValueError:
                messagebox.showerror('Error', 'Invalid input. Please enter a valid Group Name.')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to create group: {str(e)}')

        create_group_button = tk.Button(create_group_window, text='Create Group', command=create_group_safe)
        create_group_button.place(x=300, y=200)

    
        


      


        

    def add_member_to_group(group_name, member_name):
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO group_members (group_name, member_name) VALUES (?, ?)', (group_name, member_name))
        conn.commit()
        conn.close()

    def group_exists(group_name):
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM groups WHERE group_name=?', (group_name,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    
    def add_member_to_group_page():
        add_member_window = tk.Toplevel(root)
        add_member_window.title('Add Member to Group')
        add_member_window.geometry("700x300")

        group_name_label = tk.Label(add_member_window, text='Group Name:')
        group_name_label.place(x=100, y=50)
        group_name_entry = tk.Entry(add_member_window)
        group_name_entry.place(x=370, y=53)

        group_exists_label = tk.Label(add_member_window, text='')
        group_exists_label.place(x=350, y=120)

        def check_group_exists_safe():
            try:
                group_name = group_name_entry.get()

                # Check if the group name is empty
                if not group_name:
                    messagebox.showerror('Error', 'Group Name cannot be empty.')
                    return

                # Assuming you have a function named 'check_group_exists' for checking if the group exists
                check_group_exists(group_name, group_exists_label)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to check if group exists: {str(e)}')

        check_group_button = tk.Button(add_member_window, text='Check if Group Exists', command=check_group_exists_safe)
        check_group_button.place(x=370, y=80)

        member_name_label = tk.Label(add_member_window, text='Member Name:')
        member_name_label.place(x=100, y=150)
        member_name_entry = tk.Entry(add_member_window)
        member_name_entry.place(x=370, y=153)

        def add_member_safe():
            try:
                group_name = group_name_entry.get()
                member_name = member_name_entry.get()

                # Check if any of the fields are empty
                if not group_name or not member_name:
                    messagebox.showerror('Error', 'Both Group Name and Member Name are required.')
                    return

                # Assuming you have a function named 'add_member' for adding a member to the group
                add_member(group_name, member_name, add_member_window)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add member: {str(e)}')

        add_member_button = tk.Button(add_member_window, text='Add Member', command=add_member_safe)
        add_member_button.place(x=300, y=200)


    def check_group_exists(group_name, label_widget):
        if group_exists(group_name):
            label_widget.config(text=f'Group "{group_name}" exists.')
        else:
            label_widget.config(text=f'Group "{group_name}" does not exist. Create the group first.')

    def add_member(group_name, member_name, add_member_window):
        if group_exists(group_name):
            add_member_to_group(group_name, member_name)
            messagebox.showinfo('Member Added', f'Member "{member_name}" added to group "{group_name}" successfully!')
            add_member_window.destroy()
        else:
            messagebox.showerror('Group Not Found', f'Group "{group_name}" does not exist. Create the group first.')
    def get_groups():
        conn = sqlite3.connect('expense_data.db')  # Update with your database file
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT group_name FROM group_members')
        groups = [row[0] for row in cursor.fetchall()]
        conn.close()
        return groups


    def get_group_members(group_name):
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT member_name FROM group_members WHERE group_name = ?', (group_name,))
        members = [member[0] for member in cursor.fetchall()]
        conn.close()
        return members


    def record_shared_expense_page():
        record_shared_expense_window = tk.Toplevel(root)
        record_shared_expense_window.title('Record Shared Expense')
        record_shared_expense_window.geometry("700x300")

        # Dropdown menu to select the group
        group_label = tk.Label(record_shared_expense_window, text='Select Group:')
        group_label.place(x=100, y=50)

        # Get the existing groups
        groups = get_groups()

        if not groups:
            messagebox.showinfo('Error', 'No groups found. Please create a group first or add members to it.')
            record_shared_expense_window.destroy()
            return

        group_var = tk.StringVar(record_shared_expense_window)
        group_var.set(groups[0])
        group_dropdown = tk.OptionMenu(record_shared_expense_window, group_var, *groups)
        group_dropdown.place(x=370, y=50)

        # Entry for payer's name
        payer_label = tk.Label(record_shared_expense_window, text='Payer:')
        payer_label.place(x=100, y=100)
        payer_entry = tk.Entry(record_shared_expense_window)
        payer_entry.place(x=370, y=103)

        # Entry for expense description
        description_label = tk.Label(record_shared_expense_window, text='Description:')
        description_label.place(x=100, y=150)
        description_entry = tk.Entry(record_shared_expense_window)
        description_entry.place(x=370, y=153)

        # Entry for amount
        amount_label = tk.Label(record_shared_expense_window, text='Amount:')
        amount_label.place(x=100, y=200)
        amount_entry = tk.Entry(record_shared_expense_window)
        amount_entry.place(x=370, y=203)

        def save_shared_expense_safe():
            try:
                selected_group = group_var.get()
                payer = payer_entry.get()
                description = description_entry.get()
                amount = float(amount_entry.get())

                # Check if any of the fields are empty
                if not selected_group or not payer or not description or not amount:
                    messagebox.showerror('Error', 'All fields must be filled in.')
                    return

                # Assuming you have a function named 'save_shared_expense' for recording the shared expense
                save_shared_expense(selected_group, payer, description, amount)
                
                record_shared_expense_window.destroy()
            except ValueError:
                messagebox.showerror('Error', 'Invalid input. Please enter a valid number for Amount.')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to record shared expense: {str(e)}')

        # Button to record the shared expense
        record_expense_button = tk.Button(record_shared_expense_window, text='Record Shared Expense',
                                          command=save_shared_expense_safe)
        record_expense_button.place(x=300, y=250)



 
    def save_shared_expense(group_name, payer, description, amount):
        # Check if the group exists
        groups = get_groups()
        if group_name not in groups:
            messagebox.showerror("Error", "Group not found. Please create the group first.")
            return

        # Check if the payer is a member of the group
        group_members = get_group_members(group_name)
        if payer not in group_members:
            messagebox.showerror("Error", "Payer is not a member of this group. Please add the member first.")
            return

        # Get the current date
        date = datetime.date.today()

        # Save the shared expense to the database
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO shared_expenses (group_name, date, payer, description, amount) VALUES (?, ?, ?, ?, ?)',
                       (group_name, date, payer, description, amount))
        conn.commit()
        conn.close()

        messagebox.showinfo('Shared Expense Recorded', f"Expense of ${amount} recorded for {group_name} by {payer} on {date} with description: {description}")



   


    def record_payment_page():
        record_payment_window = tk.Toplevel(root)
        record_payment_window.title('Record Payment')
        record_payment_window.geometry("700x300")

        # Dropdown menu to select the group
        group_label = tk.Label(record_payment_window, text='Select Group:')
        group_label.place(x=100,y=50)

        # Get the existing groups
        groups = get_groups()

        if not groups:
            messagebox.showinfo('Error', 'No groups found. Please create a group first or add members to it.')
            record_payment_window.destroy()
            return

        group_var = tk.StringVar(record_payment_window)
        group_var.set(groups[0])
        group_dropdown = tk.OptionMenu(record_payment_window, group_var, *groups)
        group_dropdown.place(x=370,y=50)

        # Entry for payer's name
        payer_label = tk.Label(record_payment_window, text='Payer:')
        payer_label.place(x=100,y=100)
        payer_entry = tk.Entry(record_payment_window)
        payer_entry.place(x=370,y=103)

        # Entry for receiver's name
        receiver_label = tk.Label(record_payment_window, text='Receiver:')
        receiver_label.place(x=100,y=150)
        receiver_entry = tk.Entry(record_payment_window)
        receiver_entry.place(x=370,y=153)

        # Entry for amount
        amount_label = tk.Label(record_payment_window, text='Amount:')
        amount_label.place(x=100,y=200)
        amount_entry = tk.Entry(record_payment_window)
        amount_entry.place(x=370,y=203)

        # Button to record the payment
        record_payment_button = tk.Button(record_payment_window, text='Record Payment',
                                          command=lambda: record_payment(
                                              group_var.get(),
                                              payer_entry.get(),
                                              receiver_entry.get(),
                                              amount_entry.get(),
                                              groups
                                          ))
        record_payment_button.place(x=300,y=250)


    payments = {}

    def record_payment(group_name, payer, receiver, amount, groups):
        # Record a payment between group members
        if group_name not in groups:
            messagebox.showinfo('Error', 'Group not found. Please create the group first.')
            return

        # Assuming each group is a list of members
        if payer not in get_group_members(group_name):
            messagebox.showinfo('Error', 'Payer is not a member of this group. Please add the member first.')
            return

        if receiver not in get_group_members(group_name):
            messagebox.showinfo('Error', 'Receiver is not a member of this group. Please add the member first.')
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showinfo('Error', 'Please enter a valid amount.')
            return

        date = datetime.date.today()

        # Add the payment to the payments dictionary
        # Note: Define payments as a global variable if it's not already defined
        global payments
        if group_name not in payments:
            payments[group_name] = [] # local

        payments[group_name].append((date, payer, receiver, amount))

        cursor.execute("""insert into payments (group_name,date,payer,receiver,amount) values ('{}','{}','{}','{}',{});""".format(group_name,date,payer,receiver,amount))
        conn.commit()

        messagebox.showinfo('Payment Recorded', f"Payment of ${amount} recorded from {payer} to {receiver} on {date}.")

    # Assuming you have a global variable payments
    payments = {}    


    def list_shared_expenses_page():
        # Create a new window
        list_shared_expenses_window = tk.Toplevel(root)
        list_shared_expenses_window.title('List Shared Expenses')
        list_shared_expenses_window.geometry("700x300")

        # Dropdown menu to select the group
        group_label = tk.Label(list_shared_expenses_window, text='Select Group:')
        group_label.place(x=100,y=50)

        # Get the existing groups
        groups = get_groups()

        if not groups:
            messagebox.showinfo('Error', 'No groups found. Please create a group first or add memebrs to it.')
            list_shared_expenses_window.destroy()
            return

        group_var = tk.StringVar(list_shared_expenses_window)
        group_var.set(groups[0])
        group_dropdown = tk.OptionMenu(list_shared_expenses_window, group_var, *groups)
        group_dropdown.place(x=370,y=50)

        # Button to list shared expenses
        list_shared_expenses_button = tk.Button(list_shared_expenses_window, text='List Shared Expenses',
                                                command=lambda: display_shared_expenses(group_var.get()))
        list_shared_expenses_button.place(x=300,y=200)

    def display_shared_expenses(group_name):
        # List shared expenses for a group
        if group_name not in get_groups():
            messagebox.showinfo('Error', 'Group not found. Please create the group first or add members to it.')
            return

        shared_expenses_list = get_shared_expenses(group_name)

        if not shared_expenses_list:
            messagebox.showinfo('Info', f'No expenses recorded yet for {group_name}.')
            return

        list_shared_expenses_window = tk.Toplevel(root)
        list_shared_expenses_window.title(f'Shared Expenses for {group_name}')

        # Create a TreeView to display shared expenses
        shared_expenses_columns = ("Date", "Payer", "Amount", "Description")
        shared_expenses_treeview = ttk.Treeview(list_shared_expenses_window, columns=shared_expenses_columns, show="headings")

        # Set column headings
        for col in shared_expenses_columns:
            shared_expenses_treeview.heading(col, text=col)

        shared_expenses_treeview.pack(pady=10)

        # Insert shared expenses data into the TreeView
        for expense in shared_expenses_list:
            shared_expenses_treeview.insert("", "end", values=expense)


    def get_shared_expenses(group_name):
    # Connect to the SQLite database
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()

        # Check if the group exists
        cursor.execute('SELECT * FROM groups WHERE group_name=?', (group_name,))
        group_exists = cursor.fetchone()
        if not group_exists:
            conn.close()
            return None  # Group not found

        # Retrieve shared expenses for the given group
        cursor.execute('SELECT * FROM shared_expenses WHERE group_name=?', (group_name,))
        shared_expenses = cursor.fetchall()

        # Close the database connection
        conn.close()

        return shared_expenses


    def list_payments_option():
        list_payments_window = tk.Toplevel(root)
        list_payments_window.title('List Payments')
        list_payments_window.geometry("700x300")

        # Dropdown menu to select the group
        group_label = tk.Label(list_payments_window, text='Select Group:')
        group_label.place(x=100, y=50)

        # Get the existing groups
        groups = get_groups()

        if not groups:
            messagebox.showinfo('Error', 'No groups found. Please create a group first .')
            list_payments_window.destroy()
            return

        group_var = tk.StringVar(list_payments_window)
        group_var.set(groups[0])
        group_dropdown = tk.OptionMenu(list_payments_window, group_var, *groups)
        group_dropdown.place(x=370, y=50)

        # Button to display payments
        display_payments_button = tk.Button(list_payments_window, text='Display Payments',
                                            command=lambda: display_payments(group_var.get()))
        display_payments_button.place(x=300, y=200)

    def get_payments(group_name):
        conn = sqlite3.connect('expense_data.db')  # Update with your database file
        cursor = conn.cursor()
        cursor.execute("SELECT date, payer, receiver, amount FROM payments WHERE group_name = ?", (group_name,))
        payments = cursor.fetchall()
        conn.close()
        return payments

    

   


    def calculate_payment_status(group_name):
        # Check if the group exists
        groups = get_groups()
        if group_name not in groups:
            messagebox.showerror("Error", "Group not found. Please create the group first.")
            return

        # Get shared expenses for the group
        shared_expenses = get_shared_expenses(group_name)

        # Get payments for the group
        group_payments = get_group_payments(group_name)

        # Calculate total expenses for each member
        member_expenses = {member: 0 for member in get_group_members(group_name)}

        for expense in shared_expenses:
            _, payer, _, amount = expense
            member_expenses[payer] += amount

        # Calculate total payments for each member
        member_payments = {member: 0 for member in get_group_members(group_name)}

        for payment in group_payments:
            if len(payment) != 4:
                # Handle the case where the tuple doesn't have the expected length
                messagebox.showerror("Error", f"Invalid payment tuple: {payment}")
                continue

            _, payer, receiver, amount = payment
            member_payments[payer] -= amount
            member_payments[receiver] += amount

        # Calculate the final payment status
        payment_status = {member: member_payments[member] + member_expenses[member] for member in member_expenses}

        # Display the payment status
        messagebox.showinfo('Payment Status', f'Payment status for {group_name}:\n{payment_status}')


    def get_group_payments(group_name):
        conn = sqlite3.connect('expense_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE group_name=?', (group_name,))
        payments = cursor.fetchall()
        conn.close()
        return payments

   

    def calculate_payment_status_option():
        calculate_window = tk.Toplevel(root)
        calculate_window.title('Calculate Payment Status')
        calculate_window.geometry("700x300")

        # Dropdown menu to select the group
        group_label = tk.Label(calculate_window, text='Select Group:')
        group_label.place(x=100,y=50)

        # Get the existing groups
        groups = get_groups()

        if not groups:
            messagebox.showinfo('Error', 'No groups found. Please create a group first.')
            calculate_window.destroy()
            return

        group_var = tk.StringVar(calculate_window)
        group_var.set(groups[0])
        group_dropdown = tk.OptionMenu(calculate_window, group_var, *groups)
        group_dropdown.place(x=370,y=50)

        # Button to calculate payment status
        calculate_button = tk.Button(calculate_window, text='Calculate Payment Status',
                                      command=lambda: calculate_payment_status(group_var.get()))
        calculate_button.place(x=300,y=200)


    def create_expense_tracking_window():
    # Function to list who owes whom within a group
        def list_who_owes_whom():
            selected_group = group_var.get()
            
            if not selected_group:
                messagebox.showinfo('Error', 'Please select a group.')
                return

            if selected_group not in get_groups():
                messagebox.showinfo('Error', 'Group not found. Please create the group first.')
                return

            shared_expenses_list = get_shared_expenses(selected_group)
            if not shared_expenses_list:
                messagebox.showinfo('Info', f'No expenses recorded yet for {selected_group}.')
                return

            members = get_group_members(selected_group)
            member_balance = {member: 0.0 for member in members}

            for date, payer, _, amount in shared_expenses_list:
                # Calculate each member's share
                share_per_member = amount / len(members)

                # Deduct the share from the payer's balance
                member_balance[payer] -= amount

                # Add the share to each member's balance
                for member in members:
                    if member != payer:
                        member_balance[member] += share_per_member

            # Determine who owes whom
            transactions = []
            for member, balance in member_balance.items():
                if balance < 0:
                    for other_member, other_balance in member_balance.items():
                        if other_member != member and other_balance > 0:
                            while member_balance[member] < 0 and member_balance[other_member] > 0:
                                amount = min(abs(member_balance[member]), member_balance[other_member])
                                transactions.append((other_member, member, amount))
                                member_balance[member] += amount
                                member_balance[other_member] -= amount

            # Display who owes whom
            if transactions:
                message = "Who owes whom:\n"
                for transaction in transactions:
                    message += f"{transaction[0]} owes {transaction[1]} ${transaction[2]:.2f}\n"
                messagebox.showinfo('Who Owes Whom', message)
            else:
                messagebox.showinfo('Info', 'No one owes anything within the group.')

        # Main GUI setup
        root = tk.Tk()
        root.title('Expense Tracking System')
        root.geometry("700x300")

        # Create SQLite database and table
        create_table()

        # Get the list of groups
        groups = get_groups()

        # Dropdown menu for selecting the group
        group_var = tk.StringVar(root)
        group_dropdown = ttk.Combobox(root, textvariable=group_var, values=groups)
        group_dropdown.place(x=300,y=50)
        group_dropdown.set("Select Group")

        # Button to execute the list_who_owes_whom function
        execute_button = tk.Button(root, text='Execute', command=list_who_owes_whom)
        execute_button.place(x=300,y=200)

        # Run the Tkinter event loop
        root.mainloop()
   
     
# Function to retrieve and display payments from the database
    def display_payments(group_name):
        # Check if the group exists
        groups = get_groups()
        if group_name not in groups:
            messagebox.showerror("Error", "Group not found. Please create the group first.")
            return

        # Retrieve payments from the database
        payments = get_payments(group_name)
        

        # Display payments in a new window

        if not payments:
           messagebox.showinfo('No Payments', 'No payments have been made from the selected group.')
           return
        else:
            # Create a treeview to display payments
            payments_display_window = tk.Toplevel(root)
            payments_display_window.title("Payments")
            tree = ttk.Treeview(payments_display_window, columns=('Date', 'Payer', 'Receiver', 'Amount'), show='headings')
            tree.heading('Date', text='Date')
            tree.heading('Payer', text='Payer')
            tree.heading('Receiver', text='Receiver')
            tree.heading('Amount', text='Amount')
            tree.pack(pady=10)

            for payment in payments:
                tree.insert('', 'end', values=payment)
        

      
      



      

  

    shared_expense_window = tk.Toplevel(root)
    shared_expense_window.title('Shared Expense Tracking')
    shared_expense_window.geometry("700x300")

    # Update the options list for shared expenses
    shared_options = [
        "Create Group",
        "Add Member to Group",
        "Record Shared Expense",
        "Record Payment",
        "List Shared Expenses",
        "List Payments",
        "Calculate Payment Status",
        "List Who Owes Whom",
        "Back to Main Menu"
    ]


    selected_shared_option = tk.StringVar(shared_expense_window)
    selected_shared_option.set(shared_options[0])

    shared_dropdown_menu = tk.OptionMenu(shared_expense_window, selected_shared_option, *shared_options)
    shared_dropdown_menu.place(x=370,y=50)
    Only_label = tk.Label(shared_expense_window, text="Choose your desired Task:",font=("Monsterret",11),fg="black")
    Only_label.place(x=100,y=50)

    shared_execute_button = tk.Button(shared_expense_window, text='Execute',
                                      command=lambda: execute_shared_option(selected_shared_option.get()))
    shared_execute_button.place(x=300,y=200)
    

    def execute_shared_option(option):
        if option == "Create Group":
           create_group_page()
        elif option == "Add Member to Group":
             add_member_to_group_page()
        elif option == "Record Shared Expense":
             record_shared_expense_page()
        elif option == "Record Payment":
             record_payment_page()
        elif option == "List Shared Expenses":
             list_shared_expenses_page()
        elif option == "List Payments":
             list_payments_option()
        elif option == "Calculate Payment Status":
             calculate_payment_status_option()
        elif option == "List Who Owes Whom":
             create_expense_tracking_window()
        elif option == "Back to Main Menu":
             shared_expense_window.destroy()
# Main GUI setup
root = tk.Tk()
root.title('Expense Tracking System')

# Create SQLite database and table
create_table()

# Dropdown menu
options = [
    "Record Expense",
    "List Expenses",
    "Edit Expense",
    "Delete Expense",
    "Label Expense",
    "Summarize Expenses",
    "Shared Expense Tracking",
    "Create a Budget",
    "View Budgets",
    "Edit Budget",
    "Send Notification",
    "Exit"
]

selected_option = tk.StringVar(root)
selected_option.set(options[0])

category_var = tk.StringVar(root)
dropdown_menu =ttk.Combobox(root, textvariable=category_var, values=options)
dropdown_menu.pack(pady=10)

style_heading = ttk.Style()
style_heading.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

# Create a style for the data cells
style_data = ttk.Style()
style_data.configure("Treeview", font=("Helvetica", 10))

# TreeView
treeview_columns = ("ID", "Description", "Amount", "Category")
treeview = ttk.Treeview(root, columns=treeview_columns, show="headings")

# Configure styles for heading and data cells
for col in treeview_columns:
    treeview.heading(col, text=col)
    treeview.column(col, anchor='center')

treeview.pack(pady=10)

# Button to execute the selected option
execute_button = tk.Button(root, text='Execute', command=lambda: execute_selected_option(category_var.get()))
execute_button.pack()

# Function to execute the selected option
def execute_selected_option(option):
    if option == "Record Expense":
        record_expense_page()
    elif option == "List Expenses":
        list_expenses_page()
    elif option == "Edit Expense":
        edit_expense_page()
    elif option == "Delete Expense":
        delete_expense_page()
    elif option == "Label Expense":
        label_expense_page()
    elif option == "Summarize Expenses":
        summarize_expenses_page()
    elif option == "Shared Expense Tracking":
        shared_expense_tracking_page()
    elif option == "Create a Budget":
        create_budget_option()
    elif option == "View Budgets":
        view_budgets_page()
    elif option == "Edit Budget":
        edit_budget_page()
    elif option == "Send Notification":
        send_notification_page()
    # Add more conditions for other options as needed
    elif option == "Exit":
        root.destroy()

# Run the Tkinter event loop
root.mainloop()
