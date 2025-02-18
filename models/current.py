from models.account import Account

class Current(Account):
    def __init__(self, name, balance,registration_number,website_url,pin_number, privilege):
        super().__init__(name, balance, pin_number, privilege)
        self.registration_number=registration_number
        self.wwebsite_url=website_url