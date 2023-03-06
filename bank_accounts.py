"""
Made by Ze Sheng
"""

import pandas as pd

def init_bank_accounts(accounts, deposits, withdrawals):
    """
    Loads the given 3 files, stores the information for individual bank accounts in a
    dictionary and calculates the account balance
    Pandas is a powerful language in data processing, here I choose to use pandas to parse all data.

    All codes in this part are first coded in Google Colab for easy plotting.

    return 'bank_accounts' dict
    """

    # TODO: use pd.read_table() and pd.read_csv to get all datas as dataframes
    account_df = pd.read_table(accounts,sep='|',names=['account_number','first_name','last_name'])
    deposite_df = pd.read_csv(deposits, sep=',',
                              names=['account_number', 'deposite1', 'deposite2', 'deposite3', 'deposite4'])
    withdrawal_df = pd.read_csv(withdrawals,sep='\,',
                               names=['account_number','withdrawal1','withdrawal2','withdrawal3'])

    # TODO: Use pd.merge() to merge all dataframes and remove all NAN values
    result = pd.merge(withdrawal_df, deposite_df, on='account_number')
    result = pd.merge(account_df, result, on='account_number')
    result = result.fillna(0).copy()

    # TODO: Create a new column called 'balance' by calculating balances using deposits and withdrawals
    all_deposit = round(result['deposite1'] + result['deposite2'] + result['deposite3'] + result['deposite4'], 2)
    all_withdrawals = round(result['withdrawal1'] + result['withdrawal2'] + result['withdrawal3'], 2)
    result['balance'] = all_deposit - all_withdrawals

    # TODO: Create dicts as {account_number : {firstname: brandaon, lastname: krakowsky, balance: 1234}}
    bank_accounts = {}
    sigle_account = {}
    all_array_list = result.values
    for i in range(0, len(all_array_list)):
        sigle_account = {'first_name': all_array_list[i][1].strip(), 'last_name': all_array_list[i][2].strip(),
                       'balance': round(all_array_list[i][-1], 2)}
        bank_accounts[str(all_array_list[i][0])] = sigle_account

    return bank_accounts


def get_account_info(bank_accounts, account_number):
    """
    Returns the account information for the given account_number as a dictionary
    If the account doesn't exist, returns None
    """
    # TODO: Get the balance of a given account
    try:
        balance = bank_accounts[account_number]
    except KeyError:
        return None
    else:
        return balance


def withdraw(bank_accounts, account_number, amount):
    """
    Withdraws the given amount from the account with the given account_number
    Rounds the new balance to 2 decimal places (Uses round_balance() function)
    If the account doesn't exist, prints a friendly message
    Raises a Runtime Error if the given amount is greater than the available balance
    Prints the new balance

    Return nothing
    """


    try:
        amount = round(float(amount), 2)
        # If the number is larger than balances, raise a RuntimeError
        if amount < 0:
            print('Amount should larger than 0!')
            return
        if amount > bank_accounts[str(account_number)]['balance']:
            raise RuntimeError('Amount greater than available balance!')
    except KeyError:  # if the account does not exist, then print an error msg
        print('Sorry, that account doesn\'t exist. ')
    else:
        bank_accounts[str(account_number)]['balance'] = bank_accounts[str(account_number)]['balance'] - amount
        round_balance(bank_accounts, str(account_number))
        print('Withdrawals success.')
        print('Your new balance is: ', bank_accounts[str(account_number)]['balance'])


def deposit(bank_accounts, account_number, amount):
    """
    Deposits the given amount into the account with the given account_number
    Rounds the new balance to 2 decimal places (Uses round_balance() function)
    If the account doesn't exist, prints a friendly message
    Prints the new balance

    Return nothing
    """
    try:
        amount = round(float(amount), 2)
        if amount < 0:
            print('Amount should larger than 0!')
            return
        # Deposits the given amount into the account with the given account_number
        bank_accounts[str(account_number)]['balance'] = bank_accounts[str(account_number)]['balance'] + amount
        round_balance(bank_accounts, str(account_number))
        print('Deposit success.')
        print('Your new balance is: ', bank_accounts[str(account_number)]['balance'])
    except KeyError:  # if the account doesn't exist
        print('Sorry, that account doesn\'t exist. ')


def purchase(bank_accounts, account_number, amounts):
    """
    Makes a purchase with the total of the given amounts from the account with the given account_number
    amounts is a list of floats
    If the account doesn't exist, prints a friendly message
    Calculates the total purchase amount + 6% sales tax
    Raises a Runtime Error if the total purchase amount is greater than the available
    balance
    Prints the new balance
    """
    # TODO: Calculate sum of a real list or calculate sum of the comma separated list
    if isinstance(amounts, list):
        sum_amounts = sum(amounts)
    else:
        amounts = amounts.split(',')
        sum_amounts = 0
        for num in amounts:
            sum_amounts += float(num)

    # TODO: Calculate difference between price and balance and raise RuntimeError if price is larger
    total_amounts = sum_amounts + calculate_sales_tax(sum_amounts)
    try:
        if total_amounts < 0:
            print('Amount should larger than 0!')
            return
        # if purchase price is larger than balance
        flag = total_amounts - bank_accounts[str(account_number)]['balance'] > 0
        if flag:
            raise RuntimeError
    except KeyError:  # if the account doesn't exist
        print('Sorry, that account doesn\'t exist.')
    else:
        bank_accounts[str(account_number)]['balance'] = bank_accounts[str(account_number)]['balance'] - total_amounts
        round_balance(bank_accounts, str(account_number))
        print('Successfully withdrawal.')
        print('Your current account balance is: ', bank_accounts[str(account_number)]['balance'])



def sort_accounts(bank_accounts, sort_type, sort_direction):
    """
    Converts the key:value pairs in the given bank_accounts dictionary to a list of tuples
    and sorts based on the given sort_type and sort_direction
    Returns the sorted list of tuples
    If the sort_type argument is the string ‘account_number’, sorts the list of tuples based
    on the account number (e.g. ‘3’, '5') in the given sort_direction (e.g. 'asc', 'desc')
    """
    # TODO: Return None if input is invalid (not account_number, first_name, last_name and balance)
    if sort_type != 'account_number' and sort_type != 'first_name' and sort_type != 'last_name' and sort_type != 'balance':
        print('Invalid sort type.')
        return None

    # TODO: Default sort direction is 'desc':
    if sort_direction != 'asc' and sort_direction != 'desc':
        sort_direction = 'desc'

    # TODO: Convert dict to dataframes:
    new_accounts_df = pd.DataFrame.from_dict(bank_accounts)
    new_accounts_df = new_accounts_df.T.reset_index().copy()


    # TODO: Sort within different types using Pandas
    if sort_type == 'account_number':
        if sort_direction == 'asc':
            new_accounts_df = new_accounts_df.sort_index()
        if sort_direction == 'desc':
            new_accounts_df = new_accounts_df.sort_index(ascending=False)

    if sort_type == 'first_name':
        if sort_direction == 'asc':
            new_accounts_df = new_accounts_df.sort_values(by='first_name', ascending=True)
        if sort_direction == 'desc':
            new_accounts_df = new_accounts_df.sort_values(by='first_name', ascending=False)

    if sort_type == 'last_name':
        if sort_direction == 'asc':
            new_accounts_df = new_accounts_df.sort_values(by='last_name', ascending=True)
        if sort_direction == 'desc':
            new_accounts_df = new_accounts_df.sort_values(by='last_name', ascending=False)

    if sort_type == 'balance':
        if sort_direction == 'asc':
            new_accounts_df = new_accounts_df.sort_values(by='balance', ascending=True)
        if sort_direction == 'desc':
            new_accounts_df = new_accounts_df.sort_values(by='balance', ascending=False)

    # TODO: Convert dataframes to dicts:
    ans = []
    single_account = {}
    all_array_list = new_accounts_df.values
    for i in range(0, len(all_array_list)):
        single_account = {'first_name': all_array_list[i][1], 'last_name': all_array_list[i][2],
                         'balance': all_array_list[i][-1]}
        single_tuple = (all_array_list[i][0], single_account)
        ans.append(single_tuple)

    return ans
    # new_accounts = sorted(bank_accounts, key = lambda i : i[int('account_number')])


def export_statement(bank_accounts, account_number, output_file):
    """
    Exports the given account information to the given output file in the following format:
    First Name: Huize
    Last Name: Huang
    Balance: 34.57
    If the account doesn’t exist, print a friendly message and do nothing
    """

    try:
        account_info = bank_accounts[str(account_number)]
    except KeyError: # the account doesn't exist
        print('Sorry, that account doesn\'t exist.')
    else:
        file = open(output_file, mode='w')
        words = 'First Name: ' + account_info['first_name'] + '\n' + \
                'Last Name: '+account_info['last_name']+'\n'+  \
                'Balance: '+str(round(account_info['balance'], 2))+'\n'
        print(words)
        file.write(words)

def round_balance(bank_accounts, account_number):
    """
    Rounds the account balance of the given account_number to two decimal places
    """
    bank_accounts[account_number]['balance'] = round(bank_accounts[account_number]['balance'], 2)


def calculate_sales_tax(amount):
    """
    Calculates and returns a 6% sales tax for the given amount
    """
    return amount * 0.06


def get_input(msg):
    while True:
        try:
            user_input = input(msg)
            user_input = int(user_input)
        except ValueError:
            print('Invalid Input! Please make sure that your input is an integer between 0 - 6. \n')
        else:
            if user_input <= 6 and user_input >= 0:
                return user_input
            else:
                print('Please input integer between 0 - 6. \n')


def isvalid_amount(num):
    """
    Check if the input is numeric.
    """
    # For a single amount input:
    try:
        float(num)
    except ValueError:
        return False
    else:
        return True


def isvalid_amount_list(num):
    """
    Check if the list is a numeric list
    """
    try:
        for num in num.split(','):
            float(num)
    except ValueError:
        return False
    else:
        return True


def main():

    # TODO: read the files to get information of all accounts by calling init_bank_accounts() function:
    account_file = 'accounts.txt'
    deposit_file = 'deposits.csv'
    withdraw_file = 'withdrawals.csv'
    # initialize accounts
    bank_accounts = init_bank_accounts(account_file, deposit_file, withdraw_file)

    # TODO: Main program:
    while True:
        # TODO: Print welcome words
        print('\nWelcome to the bank!   What would you like to do?')
        WELCOME_WORDS = """
               1: Get account info
               2: Make a deposit
               3: Make a withdrawal
               4: Make a purchase
               5: Sort accounts
               6: Export a statement
               0: Leave the bank
               """
        print(WELCOME_WORDS)

        # TODO: Get the input from users:
        input_msg = "Enter 0 - 6 to choose a service."
        user_input = get_input(input_msg)

        # TODO: Find service (check):
        # 1. Get account information:
        if user_input == 1:
            account_number = input('\n Please enter your account number: \n')
            account_info = get_account_info(bank_accounts, account_number)
            if account_info is None:
                print('Sorry, that account doesn\'t exist.')
            else:
                print('\nHere is your account information\n', account_info)

        # 2. Make a deposit:
        elif user_input == 2:
            account_number = input('\nPlease enter your account number:\n ')
            deposit_amount = input('Please Enter deposit amount:\n')
            if not isvalid_amount(deposit_amount):
                print('Invalid deposit amount.')
            else:
                deposit(bank_accounts, account_number, deposit_amount)

        # 3. Make a withdrawal:
        elif user_input == 3:
            account_number = input('\nPlease enter your account number:\n ')
            withdraw_amount = input('Please enter your withdrawal amount\n')
            if not isvalid_amount(withdraw_amount):
                print('Invalid withdrawal amount.')
            else:
                withdraw(bank_accounts, account_number, withdraw_amount)

        # 4. Make a purchase:
        elif user_input == 4:
            account_number = input('\nPlease enter your account number:\n ')
            purchase_amount = input('Please enter your purchase bills (as comma separated list)')
            if not isvalid_amount_list(purchase_amount):
                print('Invalid purchase amount')
            else:
                purchase(bank_accounts, account_number, purchase_amount)

        # 5. Sort accounts:
        elif user_input == 5:
            sort_type = input('\nPlease enter you sort type: (\'account_number\','
                              ' \'first_name\', \'last_name\', or \'balance\')\n')
            sort_direction = input('Sort direction (\'asc\' or \'desc\')?')
            sorted_accounts = sort_accounts(bank_accounts, sort_type, sort_direction)
            if sorted_accounts is not None:
                for t in sorted_accounts:
                    print(t)
                    #print('\n')
            else:
                print(sorted_accounts)

        # 6. Export a statement:
        elif user_input == 6:
            account_number = input('\nPlease enter your account number:\n')
            output_file = str(account_number) + '.txt'
            export_statement(bank_accounts, account_number, output_file)



        print('---------------------------------------------------------------------')


if __name__ == '__main__':
    main()