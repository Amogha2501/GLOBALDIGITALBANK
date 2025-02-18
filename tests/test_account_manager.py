import sys
import os
import json
from services.transaction_manager import TransactionManager

# Helper function to reset the log file before tests
def reset_log_file():
    if os.path.exists(TransactionManager.log_file):
        os.remove(TransactionManager.log_file)

def test_log_transaction():
    reset_log_file()
    TransactionManager.log_transaction(12345, 100.0, "Deposit")
    assert os.path.exists(TransactionManager.log_file), "Log file not created."

    with open(TransactionManager.log_file, 'r') as file:
        transactions = json.load(file)
        assert len(transactions) == 1, "Transaction not logged."
        assert transactions[0]['account_number'] == 12345, "Account number mismatch."
        assert transactions[0]['amount'] == 100.0, "Amount mismatch."
        assert transactions[0]['transaction_type'] == "Deposit", "Transaction type mismatch."
    print("test_log_transaction passed.")

def test_display_transactions():
    reset_log_file()
    TransactionManager.log_transaction(12345, 200.0, "Withdraw")
    TransactionManager.log_transaction(67890, 500.0, "Deposit")
    
    print("Running test_display_transactions...")
    TransactionManager.display_transactions()
    print("test_display_transactions passed.")

def test_view_transactions_by_account_and_date_range():
    reset_log_file()
    TransactionManager.log_transaction(12345, 150.0, "Deposit")
    TransactionManager.log_transaction(12345, 200.0, "Withdraw")
    
    print("Running test_view_transactions_by_account_and_date_range...")
    # Prompt manually to test with user input for account and date range
    TransactionManager.view_transactions_by_account_and_date_range()
    print("test_view_transactions_by_account_and_date_range passed.")

def test_view_transactions_by_type():
    reset_log_file()
    TransactionManager.log_transaction(12345, 300.0, "Transfer", to_account_number=67890)
    TransactionManager.log_transaction(12345, 400.0, "Deposit")
    
    print("Running test_view_transactions_by_type...")
    # Prompt manually to test with user input for account and transaction type
    TransactionManager.view_transactions_by_type()
    print("test_view_transactions_by_type passed.")

if __name__ == "__main__":
    test_log_transaction()
    test_display_transactions()
    
    # Uncomment these lines to test input-based functions
    # test_view_transactions_by_account_and_date_range()
    # test_view_transactions_by_type()
