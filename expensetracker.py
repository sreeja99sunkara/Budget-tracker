import mysql.connector
from datetime import datetime


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

# Create a cursor object
mycursor = mydb.cursor()


try:
    amount = float(input("Enter amount: "))
    if amount <= 0:
        print("Amount must be greater than 0")
        exit()

    category = input("Enter category (Food, Entertainment, Travel, Utilities, Other): ")

    date_input = input("Enter date (YYYY-MM-DD): ")
    date = datetime.strptime(date_input, "%Y-%m-%d").date()

    note = input("Enter note: ")

except ValueError:
    print("Invalid input! Please enter correct values.")
    exit()

sql="""
INSERT INTO expenses (amount, category, date, note)
VALUES (%s, %s,%s, %s);
"""

values = (amount, category, date, note)

try:
    mycursor.execute(sql, values)
    mydb.commit()
    print("Expense added successfully!")
except mysql.connector.Error as err:
    print(f"Error inserting data: {err}")
    
mycursor.close()
mydb.close()
