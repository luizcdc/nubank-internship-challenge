from datetime import datetime
import unittest
import sys
try:
    sys.path.append('..//')
    from authorize import Account, Transaction, NotInactive
except ModuleNotFoundError:
    pass


class TestAuthorize(unittest.TestCase):
    account_1 = Account(True, 100)
    account_2 = Account(False, 100)

    def setUp(self):
        self.account_1 = Account(True, 100)
        self.account_2 = Account(False, 100)

    def test_active_account(self):
        now = datetime.now()
        transaction1 = Transaction('Burguer King', 10, now)
        account1_after = Account(
            True, 90)
        account1_after.history.append(transaction1)
        transaction2 = Transaction('Paris 6', 100, now)
        self.assertEqual(self.account_1.authorize(transaction1),
                         {'account': account1_after,
                          'violations': []})
        self.assertEqual(self.account_2.authorize(transaction2),
                         {'account': Account(False, 100),
                          'violations': [NotInactive]})
