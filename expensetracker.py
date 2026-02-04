import mysql.connector
from datetime import datetime

#Database Connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sreeja_99",
        database="expensesdb"
    )
    print("Connection established successfully!")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()

mycursor = mydb.cursor()
while True:   
    # MENU 
    print("\n Expense Tracker ")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expenses")
    print("4. Delete Expenses")
    print("5. Exit")

    main_choice = input("Enter choice (1-5): ")

    # ADD EXPENSE
    if main_choice == "1":
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
                exit()

            category = input("Enter category (Food, Entertainment, Travel, Utilities, Other): ")
            date_input = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
            note = input("Enter note: ")

            sql = """
            INSERT INTO expenses (amount, category, date, note)
            VALUES (%s, %s, %s, %s)
            """
            mycursor.execute(sql, (amount, category, date, note))
            mydb.commit()
            print("Expense added successfully!")

        except ValueError:
            print("Invalid input!")

    # VIEW EXPENSES
    elif main_choice == "2":
        print("\n View Expenses")
        print("1. View all expenses")
        print("2. Filter by date range")
        print("3. Filter by category")

        choice = input("Enter choice (1-3): ")

        if choice == "1":
            mycursor.execute("SELECT id, amount, category, date, note FROM expenses")

        elif choice == "2":
            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")
            mycursor.execute(
                "SELECT id, amount, category, date, note FROM expenses WHERE date BETWEEN %s AND %s",
                (start, end)
            )

        elif choice == "3":
            category = input("Enter category: ")
            mycursor.execute(
                "SELECT id, amount, category, date, note FROM expenses WHERE category = %s",
                (category,)
            )
        else:
            print("Invalid choice")
            exit()

        rows = mycursor.fetchall()

        if not rows:
            print("No expenses found.")
            exit()

        total = 0
        for row in rows:
            print(row[0], row[1], row[2], row[3], row[4])
            total += row[1]

        print("Total Amount:", total)

    # UPDATE EXPENSES
    elif main_choice == "3":
        x=int(input("Enter expense id: "))
        mycursor.execute("SELECT * FROM expenses WHERE id = %s",(x,))
        if(mycursor.fetchone()==None):
            print("invalid id")
        else:
            amount = float(input("Enter new amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
            else:
                category = input("Enter new category: ")
                date_input = input("Enter new date (YYYY-MM-DD): ")
                date = datetime.strptime(date_input, "%Y-%m-%d").date()
                note = input("Enter new note: ")

                mycursor.execute(
                    """
                    UPDATE expenses
                    SET amount = %s, category = %s, date = %s, note = %s
                    WHERE id = %s
                    """,
                    (amount, category, date, note, x)
                )
                mydb.commit()

    #DELETE EXPENSES
    elif main_choice == "4":
        x = int(input("Enter expense id to delete: "))

        mycursor.execute("SELECT id FROM expenses WHERE id = %s", (x,))
        if(mycursor.fetchone()==None):
            print("Invalid ID")
        else:
            mycursor.execute("DELETE FROM expenses WHERE id = %s", (x,))
            mydb.commit()

    elif main_choice == "5":
        break
    else:
        print("Invalid option")
            
mycursor.close()
mydb.close()
    
