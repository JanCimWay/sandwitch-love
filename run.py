import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a vaid string of data from the user
    via the terminal, which must be a string of 6 numbers sepearted
    by comas. The loop will repeatedly request date, until it is valid
    """
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be in six numbers, seperated by comas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter Your data here: ")

        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print("Data is Valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if strungs cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]  # first test - integer
        if len(values) != 6:  # second test - are there 6 values
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False  # this is for WHILE statement in get_sales

    return True  # this is for WHILE statement in get_sales


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...""\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplius is definied as the sales figure substracted from the stock:
    - Positive surplis indicates waste
    - Negative surplus indiscates extra made whe stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # pprint(stock)  # this was used for pprint insted print
    # during postprocess installed in the beginning
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        # special for loop case when one or more lists are used
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    # upper line converts to list of int not str
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)


print("Welcome to Love Sandwitches Data automation")
main()
