class AccountRepository:
    # Class attributes to store all accounts and the account counter
    accounts = []
    account_counter = 1000

    # Method to generate a new account number
    @classmethod
    def generate_account_number(cls):
        cls.account_counter += 1
        return cls.account_counter

    # Method to save an account
    @classmethod
    def save_account(cls, account):
        cls.accounts.append(account)
    
    # Method to get all accounts
    def get_all_accounts(self):
        return self.accounts
