

class BonusCard(object):
    def __init__(self, uuid, balance=0, transactions=({},)):
        self.uuid = uuid
        self.balance = balance
        self.transactions = transactions
