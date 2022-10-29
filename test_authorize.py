from datetime import datetime
import unittest
import sys
try:
    sys.path.append('..//')
    from authorize import Account, Transaction, NotInactive, FirstAboveThreshold
except ModuleNotFoundError:
    pass


class TestAuthorize(unittest.TestCase):
    account_1 = Account(True, 100)
    account_2 = Account(False, 100)

    def setUp(self):
        self.account_1 = Account(True, 100)
        self.account_2 = Account(False, 100)
        self.now = datetime.now()

    def test_not_inactive(self):
        now = self.now
        SMALL_VALUE = 1
        account_true = self.account_1
        account_false = self.account_2

        assert account_true.active is True
        self.assertTrue(NotInactive.validate(self.account_1,
                                             Transaction('merchant_1',
                                                         SMALL_VALUE,
                                                         now)))

        assert account_false.active is False
        self.assertFalse(NotInactive.validate(self.account_2,
                                              Transaction('merchant_1',
                                                          SMALL_VALUE,
                                                          now)))

    def test_first_transaction_above_threshold(self):
        now = self.now
        LIMIT = self.account_1.available_limit
        account = self.account_1

        UNDER_VALUE = 50
        THRESHOLD_VALUE = 90
        OVER_VALUE = 99
        assert UNDER_VALUE < FirstAboveThreshold.THRESHOLD * LIMIT
        assert THRESHOLD_VALUE == FirstAboveThreshold.THRESHOLD * LIMIT
        assert OVER_VALUE > FirstAboveThreshold.THRESHOLD * LIMIT

        self.assertTrue(FirstAboveThreshold.validate(account,
                                                     Transaction('merchant_1',
                                                                 UNDER_VALUE,
                                                                 now)))

        self.assertTrue(FirstAboveThreshold.validate(account,
                                                     Transaction('merchant_1',
                                                                 THRESHOLD_VALUE,
                                                                 now)))
        self.assertFalse(FirstAboveThreshold.validate(account,
                                                      Transaction('merchant_1',
                                                                  OVER_VALUE,
                                                                  now)))

    def test_authorize_active_account(self):
        now = self.now
        SMALL_VALUE = 1
        transaction = Transaction(merchant='merchant_1',
                                  amount=SMALL_VALUE,
                                  time=now)

        account_active = self.account_1
        account_active_after = Account(account_active.active,
                                       (account_active.available_limit -
                                        SMALL_VALUE))
        account_active_after.history.append(transaction)

        account_inactive = self.account_2
        account_inactive_after = Account(active=account_inactive.active,
                                         available_limit=account_inactive.available_limit)

        assert account_active.active is True
        self.assertEqual(account_active.authorize(transaction),
                         {'account': account_active_after,
                          'violations': []})

        assert account_inactive.active is False
        self.assertEqual(account_inactive.authorize(transaction),
                         {'account': account_inactive_after,
                          'violations': [NotInactive]})

    def test_authorize_subtracts_limit(self):
        now = self.now
        SMALL_VALUE = 1
        MEDIUM_VALUE = self.account_1.available_limit // 2

        account_small = Account(self.account_1.active,
                                self.account_1.available_limit)
        limit_after_small = account_small.available_limit - SMALL_VALUE
        transaction_small = Transaction(merchant='merchant_1',
                                        amount=SMALL_VALUE,
                                        time=now)

        assert account_small.active is True
        assert SMALL_VALUE <= account_small.available_limit
        account_small.authorize(transaction_small)
        temp_newlimit_small = account_small.available_limit
        self.assertEqual(temp_newlimit_small, limit_after_small)

        account_medium = Account(self.account_1.active,
                                 self.account_1.available_limit)
        limit_after_medium = account_medium.available_limit - MEDIUM_VALUE
        transaction_medium = Transaction(merchant='merchant_1',
                                         amount=MEDIUM_VALUE,
                                         time=now)

        assert account_medium.active is True
        assert MEDIUM_VALUE <= account_medium.available_limit
        account_medium.authorize(transaction_medium)
        temp_newlimit_medium = account_medium.available_limit
        self.assertEqual(temp_newlimit_medium, limit_after_medium)

    def test_authorize_adds_transaction(self):
        raise NotImplementedError
