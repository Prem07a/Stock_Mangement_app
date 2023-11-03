import decimal
import re
from tkinter import messagebox

import mysql.connector
from PIL import Image
from customtkinter import *

print("""
Stock Market Management System

This Python program is a part of a stock market management system. It provides functionality for users to register,
log in, view their wallet balance, buy and sell shares of different companies, and manage their portfolio.
The program uses a graphical user interface (GUI) created using the 'customtkinter' library and displays images
using the Python Imaging Library (PIL). It also interacts with a MySQL database for user registration, login,
and managing user wallets and shares.

The main functionality of the program includes:
- User registration with details like full name, PAN card, Aadhar number, phone number, and initial balance.
- User login with phone number and password authentication.
- Display of the user's wallet balance.
- Buying and selling shares of different companies, where stock prices are fetched from a database.
- Managing the user's portfolio, displaying the number of shares owned for each company.

The code is organized into functions that handle various tasks, such as connecting to the database, checking user
credentials, adding money to the wallet, buying and selling shares, and updating the user's portfolio.
The GUI is built using the 'customtkinter' library, allowing for user-friendly interaction.\n\n""")

print("""
Author: Prem Gaikwad
Roll No.: 32355
Date: 15 Oct 2023
Subject: DBMS
Database: MySQL
""")

print("""
   _____           _                    _____ _             _           _ 
  / ____|         | |                  / ____| |           | |         | |
 | (___  _   _ ___| |_ ___ _ __ ___   | (___ | |_ __ _ _ __| |_ ___  __| |
  \___ \| | | / __| __/ _ \ '_ ` _ \   \___ \| __/ _` | '__| __/ _ \/ _` |
  ____) | |_| \__ \ ||  __/ | | | | |  ____) | || (_| | |  | ||  __/ (_| |
 |_____/ \__, |___/\__\___|_| |_| |_| |_____/ \__\__,_|_|   \__\___|\__,_|
          __/ |                                                           
         |___/                                                            
""")

app = CTk()
app.geometry("500x400")
set_appearance_mode("dark")
set_default_color_theme("blue")
app.title("DBMS")
frame = CTkFrame(master=app)
img_label = CTkLabel(master=app)
wallet_frame = CTkFrame(master=app)
port = CTkFrame(master=app)
stock_frame = CTkFrame(master=app)


def connect_to_database():
    """
    Connect to the Stock Market Database.

    This function establishes a connection to a MySQL database named 'stock_market_db' using the provided credentials.
    The connection is essential for performing database operations, such as retrieving data, updating records, and
    managing user information.

    Returns:
        mysql.connector.MySQLConnection: A connection object to the 'stock_market_db' database.

    Raises:
        MySQLConnectionError: If the connection to the database cannot be established.

    """

    try:
        with open("database_credentials.txt", "r") as file:
            lines = file.readlines()

        credentials = {}
        for line in lines:
            key, value = line.strip().split(": ")
            credentials[key] = value

        return mysql.connector.connect(
            host=credentials["Host"],
            user=credentials["User"],
            password=credentials["Password"],
            database=credentials["Database"]
        )

    except FileNotFoundError:
        print("Database credentials file not found.")
        sys.exit()
    except Exception as e:
        print(f"Failed to connect to the database: {str(e)}")
        sys.exit()


connection = connect_to_database()
cursor = connection.cursor()


def get_wallet_balance(user_id):
    """
        Retrieve the wallet balance for a specific user.

        This function queries the 'wallets' table in the database to fetch the balance associated with a given 'user_id.'
        The wallet balance represents the amount of money available for a specific user to trade stocks within the Stock
        Market Management System.

        Args:
            user_id (int): The unique identifier of the user for whom the wallet balance is requested.

        Returns:
            float or None: The wallet balance as a floating-point number or None if the user doesn't have a wallet or
            the user ID is invalid.
    """
    cursor.execute(f"SELECT balance FROM wallets WHERE user_id = {user_id}")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def update_wallet_balance(user_id, new_balance):
    """
    Update the wallet balance for a specific user in the database.

    This function updates the wallet balance associated with a given 'user_id' in the 'wallets' table of the database.
    It performs an SQL UPDATE operation to set the new balance.

    Args:
        user_id (int): The unique identifier of the user whose wallet balance needs to be updated.
        new_balance (float): The new wallet balance to be set for the user.

    Returns:
        None
    """
    sql = "UPDATE wallets SET balance = %s WHERE user_id = %s"
    val = (new_balance, user_id)

    # Clear any pending results
    cursor.fetchall()

    cursor.execute(sql, val)
    connection.commit()
    frame_count = 0
    frames_to_destroy = []

    for widget in app.winfo_children():
        if "frame" in widget.winfo_name():
            frames_to_destroy.append(widget)
            frame_count += 1
    for frame in frames_to_destroy:
        frame.destroy()
    logged_in(user_id)


def add_money_to_wallet(user_id, amount):
    """
    Add money to a user's wallet balance in the database.

    This function adds a specified amount to the wallet balance of a user in the 'wallets' table of the database.
    It first checks if the user's wallet exists and then performs the addition operation.

    Args:
        user_id (int): The unique identifier of the user whose wallet balance should be updated.
        amount (float or decimal.Decimal): The amount to be added to the user's wallet balance.

    Returns:
        None
    """
    current_balance = get_wallet_balance(user_id)
    if current_balance is not None:
        # Convert the amount to decimal
        try:
            amount_decimal = decimal.Decimal(amount)
        except decimal.InvalidOperation as e:
            messagebox.showerror("Error", "Please add a valid Number")
            amount_decimal = 0
        new_balance = current_balance + amount_decimal
        update_wallet_balance(user_id, new_balance)
    else:
        print("User wallet not found. Please check the user ID.")


def add(userid):
    """
        Function to prompt the user for an amount and add it to their wallet balance.

        This function displays an input dialog to the user, allowing them to enter an amount to add to their wallet balance.
        It then calls the add_money_to_wallet function to update the user's wallet balance in the database.

        Args:
            userid (int): The unique identifier of the user whose wallet balance should be updated.

        Returns:
            None
    """
    new_bal = CTkInputDialog(text="Enter Amount To Add", title="Balance").get_input()
    if new_bal == None:
        return
    add_money_to_wallet(userid, new_bal)


def check_shares(user_id):
    """
    Function to retrieve and format the shares owned by a user.

    This function queries the database to retrieve the shares owned by a user and formats the result as a dictionary
    where the keys are company identifiers and the values are the number of shares owned by the user.

    Args:
        user_id (int): The unique identifier of the user for whom to retrieve share information.

    Returns:
        dict: A dictionary where keys are company identifiers and values are the number of shares owned by the user.
    """
    sql = "SELECT c.company_name, s.shares_owned FROM shares s JOIN companies c ON s.company_id = c.company_id WHERE user_id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    results = cursor.fetchall()
    storage = {"Tata Motors": "TATA", "Infosys": "INFO", "Reliance Industries": "RELIANCE", "ICICI Bank": "ICICI",
               "HDFC Ltd": "HDFC"}

    if results:
        data = {}
        for company, shares in results:
            data[storage[company]] = shares
        return data
    else:
        return {}


def update_user_shares(user_id, company_id, new_share_count):
    """
    Function to update the number of shares owned by a user for a specific company.

    This function updates the number of shares owned by a user for a specific company in the database.

    Args:
        user_id (int): The unique identifier of the user.
        company_id (int): The unique identifier of the company for which to update the shares.
        new_share_count (int): The new number of shares to set for the user and company.

    Returns:
        None
    """
    sql = "UPDATE shares SET shares_owned = %s WHERE user_id = %s AND company_id = %s"
    val = (new_share_count, user_id, company_id)
    cursor.execute(sql, val)
    connection.commit()


def get_stock_price(company_id):
    """
    Function to retrieve the stock price of a company.

    This function retrieves the stock price of a company from the database using its unique identifier.

    Args:
        company_id (int): The unique identifier of the company for which to retrieve the stock price.

    Returns:
        float: The stock price of the specified company, or 0.0 if the company is not found.
    """
    sql = "SELECT stock_price FROM companies WHERE company_id = %s"
    val = (company_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return 0.0


def add_shares_to_portfolio(user_id, company_id, shares):
    """
    Function to add shares of a company to a user's portfolio.

    This function inserts a new entry into the 'shares' table, representing the addition of shares of a specific company
    to a user's portfolio.

    Args:
        user_id (int): The unique identifier of the user.
        company_id (int): The unique identifier of the company.
        shares (int): The number of shares to be added to the user's portfolio.

    Returns:
        None
    """
    sql = "INSERT INTO shares (user_id, company_id, shares_owned) VALUES (%s, %s, %s)"
    val = (user_id, company_id, shares)
    cursor.execute(sql, val)
    connection.commit()


def get_user_shares(user_id, company_id):
    """
    Retrieve the number of shares owned by a user for a specific company.

    This function queries the 'shares' table to retrieve the number of shares owned by a user for a specific company.

    Args:
        user_id (int): The unique identifier of the user.
        company_id (int): The unique identifier of the company.

    Returns:
        int: The number of shares owned by the user for the specified company.
    """
    sql = "SELECT shares_owned FROM shares WHERE user_id = %s AND company_id = %s"
    val = (user_id, company_id)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


def buy_shares(user_id, company):
    """
    Buy shares of a specific company for a user.

    This function allows a user to buy shares of a specific company by providing the number of shares to purchase.
    It calculates the purchase amount, checks the user's wallet balance, and updates the database accordingly.

    Args:
        user_id (int): The unique identifier of the user.
        company (str): The identifier of the company to buy shares from (e.g., "TATA", "INFO", "RELIANCE", etc.).

    Returns:
        None
    """
    global wallet_frame
    global port
    global stock_frame
    ids = {"TATA": "1", "INFO": "2", "RELIANCE": "3", "ICICI": "4", "HDFC": "5"}
    company_id = ids[company]
    shares_to_buy = CTkInputDialog(text="Enter Number of Shares To Buy", title=company).get_input()
    if shares_to_buy:
        shares_to_buy = int(shares_to_buy)
    else:
        return

    stock_price = get_stock_price(company_id)
    purchase_amount = shares_to_buy * float(stock_price)
    wallet_balance = float(get_wallet_balance(user_id))

    current_shares = get_user_shares(user_id, company_id)

    if wallet_balance >= purchase_amount:
        new_balance = wallet_balance - purchase_amount
        update_wallet_balance(user_id, new_balance)

        if current_shares > 0:
            # The user already owns shares in this company; update the share count.
            new_shares = current_shares + shares_to_buy
            update_user_shares(user_id, company_id, new_shares)
        else:
            # The user does not own shares in this company; insert a new entry.
            add_shares_to_portfolio(user_id, company_id, shares_to_buy)

        messagebox.showinfo("Done", f"{company} Shares Bought Successfully")
        frame_count = 0
        frames_to_destroy = []

        for widget in app.winfo_children():
            if "frame" in widget.winfo_name():
                frames_to_destroy.append(widget)
                frame_count += 1
        # Then, destroy each of the identified frames
        for frame in frames_to_destroy:
            frame.destroy()

        logged_in(user_id)

    else:
        messagebox.showerror("Error", "Insufficient balance to make the purchase.")


def remove_shares_from_portfolio(user_id, company_id, shares):
    """
    Remove a specified number of shares from a user's portfolio for a specific company.

    Parameters:
    - user_id (int): The unique identifier of the user whose portfolio needs to be updated.
    - company_id (int): The unique identifier of the company for which shares are being removed.
    - shares (int): The number of shares to be removed from the user's portfolio.

    Returns:
    - None

    Functionality:
    This function checks if the user has a sufficient number of shares for a specific company and, if so, removes the
    specified number of shares from the user's portfolio. If the user does not have enough shares, it prints a message
    indicating the insufficiency.
    """
    current_shares = get_user_shares(user_id, company_id)

    if current_shares >= shares:
        new_share_count = current_shares - shares
        update_user_shares(user_id, company_id, new_share_count)
    else:
        print("You do not have enough shares to make the sale.")


def sell_shares(user_id, company):
    """
       Sell shares of a specific company for a user.

       Args:
           user_id (int): The unique identifier of the user.
           company (str): The identifier of the company to sell shares of (e.g., "TATA", "INFO", "RELIANCE", etc.).

       This function allows a user to sell shares of a specific company by providing the number of shares to sell.
       It calculates the sale amount, checks the user's share balance, and updates the database accordingly.

       If the user has enough shares to sell, the function deducts the sold shares from their portfolio, updates
       the wallet balance, and displays a success message.

       If the user does not have enough shares to make the sale, an error message is shown.

       Returns:
           None
       """
    global stock_frame
    global port
    global wallet_frame
    ids = {"TATA": "1", "INFO": "2", "RELIANCE": "3", "ICICI": "4", "HDFC": "5"}
    company_id = ids[company]
    shares_to_sell = CTkInputDialog(text="Enter Number of Shares To Sell", title=company).get_input()

    if shares_to_sell:
        shares_to_sell = int(shares_to_sell)
    else:
        return

    user_shares = int(get_user_shares(user_id, company_id))
    if user_shares >= shares_to_sell:
        stock_price = float(get_stock_price(company_id))
        sale_amount = shares_to_sell * stock_price
        wallet_balance = float(get_wallet_balance(user_id))
        new_balance = wallet_balance + sale_amount  # Update wallet balance with the sale amount
        update_wallet_balance(user_id, new_balance)  # Update the wallet balance in the database
        remove_shares_from_portfolio(user_id, company_id, shares_to_sell)
        messagebox.showinfo("Done", f"You have sold {shares_to_sell} shares of {company}.")
        frame_count = 0
        frames_to_destroy = []

        for widget in app.winfo_children():
            if "frame" in widget.winfo_name():
                frames_to_destroy.append(widget)
                frame_count += 1
        for frame in frames_to_destroy:
            frame.destroy()
        logged_in(user_id)
    else:
        messagebox.showerror("Error", "You do not have enough shares to make the sale.")


def out():
    """
    Closes the Profile and open the login page

    :return: None
    """
    global wallet_frame
    global port
    global stock_frame
    global top
    try:
        top.destroy()
    except:
        pass

    wallet_frame.destroy()
    port.destroy()
    stock_frame.destroy()

    page1()


def view(user_id, company):
    global top
    try:
        top.destroy()
    except:
        pass
    top = CTkToplevel(app)
    top.geometry("300x300")
    top.title(company)
    comp = CTkImage(Image.open(f"./images/{company}.png"), size=(200, 220))
    comp_l = CTkLabel(master=top, text="", image=comp)
    comp_l.pack()
    ids = {"TATA": "1", "INFO": "2", "RELIANCE": "3", "ICICI": "4", "HDFC": "5"}

    price = get_stock_price(ids[company])
    price_label = CTkLabel(master=top, text=f"₹ {price}", font=("Roboto", 16))
    price_label.pack()
    buy_button = CTkButton(master=top, text="Buy", width=120, height=40, hover_color="green", font=("Roboto", 24),
                           command=lambda: buy_shares(user_id, company))
    buy_button.place(x=20, y=250)

    sell_button = CTkButton(master=top, text="Sell", width=120, height=40, hover_color="red", font=("Roboto", 24),
                            command=lambda: sell_shares(user_id, company))
    sell_button.place(x=160, y=250)


def logged_in(userid):
    """
    Handle the user's interface when they are logged in.

    Args:
        userid (int): The unique identifier of the logged-in user.

    This function updates the user interface to display their wallet balance, portfolio of shares, and available stocks
    for purchase. It creates frames, labels, and buttons for these purposes.

    Returns:
        None
    """
    global frame
    global img_label
    global wallet_frame
    global port
    global stock_frame
    frame.destroy()
    img_label.destroy()
    balance = get_wallet_balance(userid)
    wallet_frame = CTkFrame(master=app, width=220, height=50)
    wallet_frame.grid(row=0, column=0, padx=10, pady=10)

    bal = CTkLabel(master=wallet_frame, text="Balance: ₹", font=("Roboto", 15))
    bal.place(x=20, y=10)
    if balance >= 1000000:
        display = str(round(balance / 1000000, 2)) + " M"
    elif balance >= 1000:
        display = str(round(balance / 1000, 2)) + " K"
    else:
        display = str(balance)
    amt = CTkLabel(master=wallet_frame, text=display, font=("Roboto", 15))
    amt.place(x=90, y=10)
    btn = CTkButton(master=wallet_frame, text="Add +", width=60, height=20, command=lambda: add(userid))
    btn.place(x=150, y=13)

    port = CTkFrame(master=app, width=220, height=320)
    port.grid(row=1, column=0, padx=10, pady=(0, 10))
    txt = CTkLabel(master=port, text="Portfolio", font=("Roboto", 24))
    txt.place(x=60, y=5)
    shares_data = check_shares(userid)
    for i, share in enumerate(shares_data):
        suitcase = CTkImage(dark_image=Image.open("./images/bagw.png"), light_image=Image.open("./images/bagb.png"),
                            size=(20, 15))
        bag = CTkLabel(master=port, text="", image=suitcase)
        bag.place(x=8, y=58 + 40 * i)
        stock_label = CTkLabel(master=port, text=f"{share} : {shares_data[share]} shares", font=("Roboto", 16))

        stock_label.place(x=30, y=60 + 40 * i)

    stock_frame = CTkFrame(master=app, width=250, height=380)
    stock_frame.grid(row=0, column=1, rowspan=2)

    # Add a heading for the stock frame
    stock_heading = CTkLabel(master=stock_frame, text="Watchlist", font=("Roboto", 24))
    stock_heading.place(x=80, y=5)

    # Create a list of stocks with their names and identifiers
    portfolio_stocks = [
        {"name": "TATA Motors", "identifier": "TATA"},
        {"name": "InfoSys", "identifier": "INFO"},
        {"name": "Reliance", "identifier": "RELIANCE"},
        {"name": "ICICI Bank", "identifier": "ICICI"},
        {"name": "HDFC Bank", "identifier": "HDFC"}
    ]

    for i, stock_data in enumerate(portfolio_stocks):
        stock_name = stock_data["name"]
        stock_label = CTkLabel(master=stock_frame, text=stock_name, font=("Roboto", 16))
        stock_label.place(x=80, y=60 + 60 * i)

        eye = CTkImage(Image.open("./images/eye.png"), size=(17, 10))
        viw_btn = CTkButton(master=stock_frame, text="View", width=80, height=20, hover_color="purple", image=eye,
                            command=lambda stock=stock_data["identifier"]: view(userid, stock))
        viw_btn.place(x=90, y=95 + 60 * i)
    lg = CTkImage(Image.open("./images/logout.png"), size=(20, 22))
    logout = CTkButton(master=port, text="Logout", command=out, image=lg)
    logout.place(x=40, y=280)


def check(user, aadhar, pan, phone, pass1, pass2, balance):
    """
       Check the provided user registration details for validity and create a new user if they are valid.

       Args:
           user (str): The full name of the user.
           aadhar (str): The Aadhar number of the user.
           pan (str): The PAN card number of the user.
           phone (str): The phone number of the user.
           pass1 (str): The user's chosen password.
           pass2 (str): Confirmation of the chosen password.
           balance (str): Initial balance for the user's wallet.

       This function checks whether the provided details are valid and complete. It validates Aadhar number, PAN card number,
       phone number, and password. If the details are valid, it proceeds to create a new user with the provided information.

       Returns:
           None
    """
    if user != "" and aadhar != "" and pan != "" and phone != "" and pass1 != "" and balance != "":
        # Validate Aadhar number (12 digits)
        if not re.match(r'^\d{12}$', aadhar):
            messagebox.showerror("Error", "Invalid Aadhar number")
            return

        # Validate PAN number (10 characters, uppercase, alphanumeric)
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
            messagebox.showerror("Error", "Invalid PAN number")
            return

        # Validate Indian phone number (10 digits starting with 7, 8, or 9)
        if not re.match(r'^[789]\d{9}$', phone):
            messagebox.showerror("Error", "Invalid phone number")
            return

        if pass1 == pass2:
            AddUser(user, pan, aadhar, phone, pass1, balance)
            messagebox.showinfo("Done", "Registered Successfully")
            page1()
        else:
            messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showerror("Error", "Fill in all details")


def AddUser(full_name, pan_number, aadhar_number, phone_number, password, initial_balance):
    """
       Register a new user in the database.

       Args:
           full_name (str): The full name of the user.
           pan_number (str): The PAN card number of the user.
           aadhar_number (str): The Aadhar number of the user.
           phone_number (str): The phone number of the user.
           password (str): The user's chosen password.
           initial_balance (str): Initial balance for the user's wallet.

       This function inserts a new user record into the 'users' table and creates a corresponding wallet entry with the
       initial balance in the 'wallets' table.

       Returns:
           None
    """
    user_sql = "INSERT INTO users (full_name, pan_number, aadhar_number, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
    user_val = (full_name, pan_number, aadhar_number, phone_number, password)

    cursor.execute(user_sql, user_val)
    connection.commit()

    cursor.execute("SELECT LAST_INSERT_ID() AS user_id")
    user_id = cursor.fetchone()[0]

    wallet_sql = "INSERT INTO wallets (user_id, balance) VALUES (%s, %s)"
    wallet_val = (user_id, initial_balance)

    cursor.execute(wallet_sql, wallet_val)
    connection.commit()

    print("User registered successfully!")


def login_check(phone_number, password):
    """
    Validate user credentials and perform login.

    Args:
        phone_number (str): The user's phone number.
        password (str): The user's password.

    This function checks if the provided phone number and password match an entry in the database. If the credentials are
    valid, it performs a login by calling the 'logged_in' function.

    Returns:
        None
    """
    global frame
    global img_label
    sql = "SELECT user_id FROM users WHERE phone_number = %s AND password = %s"
    val = (phone_number, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        frame.destroy()
        img_label.destroy()
        logged_in(result[0])
    else:
        messagebox.showerror("Error", "Invalid Credentials")


def backfnc():
    """
    This Function Takes the Application to previous Page
    :return: None
    """
    global frame
    global img_label
    frame.destroy()
    img_label.destroy()
    page1()


def login():
    """
    Create the login interface and handle login functionality.

    This function creates the login user interface, allowing users to enter their phone number and password. When the
    "Login" button is clicked, it calls the 'login_check' function to validate the credentials and perform the login.

    Returns:
        None
    """
    global frame
    global img_label
    frame.destroy()
    frame = CTkFrame(master=app, width=200, height=400)
    frame.grid(row=0, column=1)

    name = CTkLabel(master=frame, text="StockUp", font=("Roboto", 24))
    name.place(x=65, y=20)
    img_logo = CTkImage(Image.open("./images/logo.png"), size=(50, 50))
    logo = CTkLabel(master=frame, image=img_logo, text="")
    logo.place(x=15, y=10)
    # Phone Number Entry
    phone_entry = CTkEntry(master=frame, placeholder_text="Phone Number")
    phone_entry.place(x=30, y=150)

    password_entry = CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.place(x=30, y=190)

    login_button = CTkButton(master=frame, text="Login",
                             command=lambda: login_check(phone_entry.get(), password_entry.get()))
    login_button.place(x=30, y=230)

    back = CTkButton(master=frame, text="Back",
                     command=backfnc, hover_color="orange")
    back.place(x=30, y=270)


def signup():
    """
    Create the sign-up interface and handle user registration.

    This function creates the sign-up user interface, allowing users to provide their full name, Aadhar number, PAN card
    number, phone number, password, password confirmation, and initial balance. When the "Sign-Up" button is clicked, it
    calls the 'check' function to validate the provided information and, if successful, calls the 'AddUser' function to
    register the user.

    Returns:
        None
    """
    global frame
    frame.destroy()
    frame = CTkFrame(master=app, width=200, height=400)
    frame.grid(row=0, column=1)

    name = CTkLabel(master=frame, text="StockUp", font=("Roboto", 24))
    name.place(x=65, y=20)
    img_logo = CTkImage(Image.open("./images/logo.png"), size=(50, 50))
    logo = CTkLabel(master=frame, image=img_logo, text="")
    logo.place(x=15, y=10)

    # UserName
    username = CTkEntry(master=frame, placeholder_text="Full Name")
    username.place(x=30, y=60)

    # Aadhar Number Entry
    aadhar_entry = CTkEntry(master=frame, placeholder_text="Aadhar Number")
    aadhar_entry.place(x=30, y=100)

    # PAN Card Entry
    pan_entry = CTkEntry(master=frame, placeholder_text="PAN Card")
    pan_entry.place(x=30, y=140)

    # Phone Number Entry
    phone_entry = CTkEntry(master=frame, placeholder_text="Phone Number")
    phone_entry.place(x=30, y=180)

    # Password Entry
    password_entry = CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.place(x=30, y=220)

    # Password Confirmation Entry
    password_confirm_entry = CTkEntry(master=frame, placeholder_text="Confirm Password", show="*")
    password_confirm_entry.place(x=30, y=260)

    # Balance
    balance = CTkEntry(master=frame, placeholder_text="Balance")
    balance.place(x=30, y=300)

    sign_btn = CTkButton(master=frame, text="Sign-Up",
                         command=lambda: check(username.get(), aadhar_entry.get(), pan_entry.get(), phone_entry.get(),
                                               password_confirm_entry.get(), password_entry.get(), balance.get()))
    sign_btn.place(x=30, y=335)
    bck = CTkButton(master=frame, text="Back",
                    command=backfnc, hover_color="orange")
    bck.place(x=30, y=370)


def close():
    """
    It Closes the Application

    :return: None
    """
    app.destroy()


def change_theme():
    """
    Changes the Theme from light to dark and visa-vera

    :return: None
    """
    set_appearance_mode("light") if app._get_appearance_mode() == "dark" else set_appearance_mode("dark")


def page1():
    """
    Create the initial page of the application.

    This function sets up the initial page of the application, which includes a background image, the application logo,
    and buttons to either log in or sign up.

    Returns:
        None
    """
    global frame
    global img_label
    frame.destroy()
    img_label.destroy()
    wallet_frame.destroy()
    port.destroy()
    stock_frame.destroy()
    img = CTkImage(Image.open("./images/login.jpg"), size=(300, 400))
    img_label = CTkLabel(master=app, image=img, text="")
    img_label.grid(row=0, column=0)

    frame = CTkFrame(master=app, width=200, height=400)
    frame.grid(row=0, column=1)

    img_logo = CTkImage(Image.open("./images/logo.png"), size=(50, 50))
    logo = CTkLabel(master=frame, image=img_logo, text="")
    logo.place(x=15, y=10)

    name = CTkLabel(master=frame, text="StockUp", font=("Roboto", 24))
    name.place(x=65, y=20)
    l_img = CTkImage(Image.open("./images/loginImg.png"), size=(21, 21))
    login_button = CTkButton(master=frame, text=" Login    ", command=login, image=l_img)
    login_button.place(x=30, y=140)
    s_img = CTkImage(Image.open("./images/signup.png"), size=(25, 21))
    sign_btn = CTkButton(master=frame, text="Sign-Up", command=signup, image=s_img)
    sign_btn.place(x=30, y=180)

    close_btn = CTkButton(master=frame, text="Close App", command=close, fg_color="green", hover_color="red")
    close_btn.place(x=30, y=230)

    t = CTkImage(dark_image=Image.open("./images/dark.png"), light_image=Image.open("./images/light.png"),
                 size=(66, 34))
    theme = CTkButton(master=frame, text="", image=t, fg_color="transparent", hover=False, width=66, height=34,
                      command=change_theme)
    theme.place(x=60, y=270)


page1()
# view()
app.mainloop()
print("""
App Closed...
""")
""" Code Ends """
