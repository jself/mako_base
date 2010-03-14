from django.db import transaction

def transaction_setup():
    transaction.enter_transaction_management()
    transaction.managed(True)

def trnasaction_teardown():
    transaction.rollback()
    transaction.leave_transaction_management()
    transaction.managed(False)
