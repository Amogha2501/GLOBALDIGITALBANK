from services.account_manager import AccountManager
from services.transaction_manager import TransactionManager
from repositories.account_repository import AccountRepository
from services.account_privileges_manager import AccountPrivilegesManager


class AccountUI:
    def __init__(self):
        AccountPrivilegesManager.load_limits()
    
    def start(self):


        while True:
            #module
            print("\n1: Login as Authority \n2: Login as User\n3: Exit")

            inp=int(input("Enter your choice: "))
            if inp==1:
                self.authority_login()
  
            elif inp==2:
                self.user_login()
            elif inp==3:
                break
            else:
                print("Invalid choice") 
                
                       
    def user_login(self):
        while True:
            print('\n\tWelcome to Global Digital Bank')
            print('\nSelect an option')
            print('1.Open Account')
            print('2.Close Account')
            print('3.Withdraw Funds')
            print('4.Deposit Funds')
            print('5.Transfer Funds')
            print('6.View Transaction Log')
            print('7.View Transaction Log by date')
            print('8.View Transaction Log by type')
            print('9.Exit')
            choice=int(input("Enter your choice: "))
            if choice==1:
                self.open_account()
            elif choice==2:
                self.close_account()
            elif choice==3:
                self.withdraw_funds()
            elif choice==4:
                self.deposit_funds()
            elif choice==5:
                self.transfer_funds()
            elif choice==6:
                TransactionManager.display_transactions()
            elif choice==7:
                TransactionManager.view_transactions_by_account_and_date_range()
            elif choice==8:
                TransactionManager.view_transactions_by_type()
            elif choice==9:
                break
            else:
                print('Invalid Choice. Please try again')
      #to open account      
    def open_account(self):
        account_type=input('Enter account type (savings/current):').strip().lower()
        name=input('Enter your name:')
        amount=float(input('Enter initial deposit amount:'))
        pin_number=int(input('Enter your pin number:')) 
        privilege=input('Enter account privilege(PREMIUM/GOLD/SILVER):').strip().upper()

        if account_type == 'savings':
            date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
            gender = input("Enter your gender (M/F): ")
            account = AccountManager().open_account(account_type, name=name, balance=amount, date_of_birth = date_of_birth, gender = gender, pin_number = pin_number, privilege = privilege)

        elif account_type == 'current':
            registration_number = input("Enter your registration number: ")
            website_url = input("Enter your website url: ")
            account = AccountManager().open_account(account_type, name=name, balance=amount, registration_number = registration_number, website_url = website_url, pin_number = pin_number, privilege = privilege)

        else:
            print("Invalid account type. Please try again")
            return
        
        print(account_type.capitalize(), "Account opened successfully. Account Number: ", account.account_number)

    # To close an account       
    def close_account(self):
        account_number = int(input("Enter your account number: "))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().close_account(account)
                print("Account closed successfully")
                account.is_active=False
            except Exception as e:
                print("Error: ", e)

        else:
            print("Account Not Found. Please try again")
    
   # To withdraw funds
    def withdraw_funds(self):
        account_number = int(input("Enter your account number: "))
        amount = float(input("Enter amount to withdraw: "))
        pin_number = int(input("Enter your pin number: "))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().withdraw(account, amount, pin_number)
                print("Amount withdrawn successfully")
            except Exception as e:
                print("Error: ", e)
        
        else:
            print("Account Not Found. Please try again.")

    def deposit_funds(self):
        account_number = int(input("Enter your account number: "))
        amount = float(input("Enter amount to deposit: "))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().deposit(account, amount)
                print("Account deposited successfully")
            except Exception as e:
                print("Error: ", e)
        
        else:
            print("Account Not Found. Please try again")
    
    # To transfer funds
    def transfer_funds(self):
        from_account_number = int(input("Enter your account number: "))
        to_account_number = int(input("Enter the account number to transfer to: "))
        amount = float(input("Enter amount to transfer: "))
        pin_number = int(input("Enter your pin number: "))
        from_account = next((acc for acc in AccountRepository.accounts if acc.account_number == from_account_number), None)
        to_account = next((acc for acc in AccountRepository.accounts if acc.account_number == to_account_number), None)
        if from_account and to_account:
            try:
                AccountManager().transfer(from_account, to_account, amount, pin_number)
                print("Amount transferred successfully")
                
            except Exception as e:
                print("Error: ", e)
        
        else:
            print("One or Both Account(s) Not Found. Please try again.")
            
   #Check transfer Limit

    def checktransferlimit(self):
        account_number=int(input("Enter the account number : "))
        acc_number = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)
        
        if acc_number:
            try:
                if acc_number.privilege=="PREMIUM" or acc_number.privilege=="GOLD" or acc_number.privilege=="SILVER":

                    transfer_limit=AccountPrivilegesManager().get_transfer_limit(acc_number.privilege)
                    print("Your Privilege : ",acc_number.privilege)
                    print("Your Transfer Limit: ",transfer_limit)
                else:
                    print("Your Privilege is not eligible for transfer limit")
            except Exception as e:
                print(e)

        else :
            print("Account Not found. Please try again")

# set  transfer limit 
#new
    def authority_login(self):
        """Handle authority login and operations."""
        print("ENTER THE AUTHORITY DETAILS")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username == "canara" and password == "2005":  
            print("Login Successful")
            self.handle_authority_options()
        else:
            print("Invalid username or password. Access denied.")

    def handle_authority_options(self):
        """Display options for authorized personnel."""
        while True:
            print("\nAuthority Menu:")
            print("1. Set Transfer Limit")
            print("2. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.set_transfer_limit()
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")

    def set_transfer_limit(self):
        """Set a new transfer limit for a privilege type."""
        privilege = input("Enter privilege type (PREMIUM/GOLD/SILVER): ").strip().upper()

        if not AccountPrivilegesManager.is_valid_privilege(privilege):
            print("Invalid privilege type. Please try again.")
            return

        try:
            new_limit = int(input("Enter the new transfer limit: ").strip())
            if new_limit <= 0:
                print("Transfer limit must be a positive number. Please try again.")
                return
        except ValueError:
            print("Invalid input. Transfer limit must be a number.")
            return

        if AccountPrivilegesManager.update_transfer_limit(privilege, new_limit):
            print(f"Transfer limit for {privilege} updated successfully to {new_limit}.")
        else:
            print("Failed to update the transfer limit. Please try again.")

