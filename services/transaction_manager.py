from exceptions.exceptions import *
import datetime
import json
import os

class TransactionManager:
    # File path for storing transactions in JSON format
    log_file = "transaction_log.json"
    
    @staticmethod
    def get_current_timestamp():
        # Return the current date and time as a timestamp
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @classmethod
    def log_transaction(cls, account_number, amount, transaction_type, to_account_number=None):
        # Create a transaction record
        transaction_record = {
            'account_number': account_number,
            'amount': amount,
            'transaction_type': transaction_type,
            'date': cls.get_current_timestamp(),
            'to_account_number': to_account_number
        }
        
        # Read existing transactions from file, if the file exists
        transactions = []
        if os.path.exists(cls.log_file):
            try:
                with open(cls.log_file, 'r') as file:
                    transactions = json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Error reading transaction file. Starting with an empty log.")
        
        # Append the new transaction to the list
        transactions.append(transaction_record)
        
        # Write the updated list of transactions to the JSON file
        try:
            with open(cls.log_file, 'w') as file:
                json.dump(transactions, file, indent=4)
            print("Transaction logged successfully.")
        except IOError:
            print("Error writing to the transaction file.")
    
      # to input transactions  
    @classmethod
    def input_transaction(cls):
        try:
            account_number = int(input("Enter your account number: "))
        except ValueError:
            print("Invalid account number. Please enter a valid integer.")
            return
        
        #  transaction type (Deposit/Withdraw/Transfer)
        transaction_type = input("Enter transaction type (Deposit/Withdraw/Transfer): ").capitalize()
        
        # Validate transaction type
        if transaction_type not in ["Deposit", "Withdraw", "Transfer"]:
            print("Invalid transaction type. Please enter one of Deposit, Withdraw, or Transfer.")
            return
        
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                print("Amount should be greater than zero.")
                return
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return
        
        # Optional to_account_number for transfer
        to_account_number = None
        if transaction_type == "Transfer":
            try:
                to_account_number = int(input("Enter the recipient's account number: "))
            except ValueError:
                print("Invalid recipient account number. Please enter a valid integer.")
                return
        
        # Log the transaction
        cls.log_transaction(account_number, amount, transaction_type, to_account_number)
    
    #to view the transaction log
    @classmethod
    def display_transactions(cls):
        # Display all transactions from the JSON file
        if os.path.exists(cls.log_file):
            try:
                with open(cls.log_file, 'r') as file:
                    transactions = json.load(file)
                    print("\nTransaction Log:")
                    for transaction in transactions:
                      print("-" * 40) 
                      print(f"Account Number: {transaction['account_number']}")
                      print(f"Amount: {transaction['amount']}")
                      print(f"Transaction Type: {transaction['transaction_type']}")
                      print(f"Date: {transaction['date']}")
                    if transaction['to_account_number']:
                        print("To Account Number: {transaction['to_account_number']}")
                    print("-" * 40)  
            except (json.JSONDecodeError, IOError):
                print("Error reading the transaction file.")
        else:
            print("No transactions found.")
    # to view transaction log by date
    @classmethod
    def view_transactions_by_account_and_date_range(cls):
     try:
        account_number = int(input("Enter the account number: "))
     except ValueError:
        print("Invalid account number. Please enter a valid integer.")
        return

     start_date_str = input("Enter the start date (YYYY-MM-DD): ")
     end_date_str = input("Enter the end date (YYYY-MM-DD): ")

     try:
        # Parse the start and end dates
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

        if start_date > end_date:
            print("Start date must be earlier than or equal to the end date.")
            return
     except ValueError:
        print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
        return

    # to  check if the log file exists
     if os.path.exists(cls.log_file):
        try:
            with open(cls.log_file, 'r') as file:
                transactions = json.load(file)

                # to filter account
                filtered_transactions = [
                    transaction for transaction in transactions
                    if (transaction['account_number'] == account_number and
                        start_date <= datetime.datetime.strptime(transaction['date'], "%Y-%m-%d %H:%M:%S") <= end_date)]

                if filtered_transactions:
                    print(f"\nTransactions for account {account_number} from {start_date_str} to {end_date_str}:\n")
                    for transaction in filtered_transactions:
                        print("-" * 40) 
                        print(f"Account Number: {transaction['account_number']}")
                        print(f"Amount: {transaction['amount']}")
                        print(f"Transaction Type: {transaction['transaction_type']}")
                        print(f"Date: { transaction['date']}")
                        if transaction.get('to_account_number'):
                            print("To Account Number:", transaction['to_account_number'])
                        print("-" * 40) 
                else:
                    print(f"No transactions found for account {account_number} within the given date range.")
        except (json.JSONDecodeError, IOError):
            print("Error reading the transaction file.")
     else:
        print("No transactions found.")

    # to check account by type
    @classmethod
    def view_transactions_by_type(cls):
        try:
            account_number = int(input("Enter the account number: "))
            transaction_type = input("Enter the transaction type (Deposit/Withdraw/Transfer): ").capitalize()

            try:
                transactions = cls.get_transactions_by_type(account_number, transaction_type)
                if transactions:
                    print(f"\nTransactions of type '{transaction_type}' for account {account_number}:\n")
                    for transaction in transactions:
                       print("-" * 40) 
                       print(f"Account Number:, {transaction['account_number']}")
                       print(f"Amount:, {transaction['amount']}")
                       print(f"Transaction Type:, {transaction['transaction_type']}")
                       print(f"Date:, {transaction['date']}")
                       if transaction['to_account_number']:
                           print("To Account Number:", transaction['to_account_number'])
                       print("-" * 40)  
                else:
                    print(f"No transactions of type '{transaction_type}' found for account {account_number}.")
            except InvalidTransactionTypeException as e:
                print(f"Error: {e}")
            except AccountDoesNotExistException as e:
                print(f"Error: {e}")
        except ValueError:
            print("Invalid input. Please enter valid account details.")

    @classmethod
    def get_transactions_by_type(cls, account_number, transaction_type):

        if transaction_type not in ["Deposit", "Withdraw", "Transfer"]:
            raise InvalidTransactionTypeException(f"Invalid transaction type: {transaction_type}")

        if not os.path.exists(cls.log_file):
            raise AccountDoesNotExistException(f"No transactions found for account {account_number}.")

        try:
            with open(cls.log_file, 'r') as file:
                transactions = json.load(file)

            #to filter account 
            filtered_transactions = [
                transaction for transaction in transactions
                if (int(transaction['account_number']) == account_number and
                    transaction['transaction_type'].lower() == transaction_type.lower())
            ]
            if not filtered_transactions:
                raise AccountDoesNotExistException(f"No transactions of type '{transaction_type}' found for account {account_number}.")
            
            return filtered_transactions
        except (json.JSONDecodeError, IOError):
            print("Error reading the transaction file.")
            return []
    
    