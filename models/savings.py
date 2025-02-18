from models.account import Account
class Savings(Account):
    def __init__(self,name,balance,date_of_birth,gender,pin_number,privilege):
        super().__init__(name,balance,pin_number,privilege)
        self.date_of_birth=date_of_birth
        self.gender=gender   
    