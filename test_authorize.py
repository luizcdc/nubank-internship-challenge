from datetime import datetime
import unittest
import sys
try:
    sys.path.append('..//')
    from authorize import Account, Transaction
    from violations import (NotActive,
                            FirstAboveThreshold,
                            InsufficientLimit,
                            HighFreqSmallInterval,
                            DoubledTransaction)

except ModuleNotFoundError:
    pass


class TestAuthorize(unittest.TestCase):
    account_1 = Account(True, 100)
    account_2 = Account(False, 100)

    def setUp(self):
        self.account_1 = Account(True, 100)
        self.account_2 = Account(False, 100)
        self.now = datetime.now().timestamp()

    def test_not_active(self):
        now = self.now
        SMALL_VALUE = 1
        account_true = self.account_1
        account_false = self.account_2

        assert account_true.active is True
        self.assertTrue(NotActive.validate(self.account_1,
                                           Transaction('merchant_1',
                                                       SMALL_VALUE,
                                                       now)))

        assert account_false.active is False
        self.assertFalse(NotActive.validate(self.account_2,
                                            Transaction('merchant_1',
                                                        SMALL_VALUE,
                                                        now)))

    def test_insufficient_limit(self):
        now = self.now

        LOWER_VALUE = self.account_1.available_limit - 1
        EQUAL_VALUE = self.account_1.available_limit
        LARGER_VALUE = self.account_1.available_limit + 1

        account_sufficient = Account(self.account_1.active,
                                     self.account_1.available_limit)

        self.assertTrue(InsufficientLimit.validate(account_sufficient,
                                                   Transaction('merchant_1',
                                                               LOWER_VALUE,
                                                               now)))

        self.assertTrue(InsufficientLimit.validate(account_sufficient,
                                                   Transaction('merchant_1',
                                                               EQUAL_VALUE,
                                                               now)))

        self.assertFalse(InsufficientLimit.validate(account_sufficient,
                                                    Transaction('merchant_1',
                                                                LARGER_VALUE,
                                                                now)))

    def test_high_freq_small_interval(self):
        NOW = self.now
        TWO_MINUTES_AGO = NOW - 120
        ONE_MINUTE_AGO = NOW - 60

        account = Account(self.account_1.active,
                          self.account_1.available_limit)

        account.history.extend([Transaction('merchant_1',
                                            100,
                                            TWO_MINUTES_AGO),
                                Transaction('merchant_2',
                                            200,
                                            ONE_MINUTE_AGO)])

        self.assertFalse(HighFreqSmallInterval.validate(account,
                                                        Transaction('merchant_3',
                                                                    300,
                                                                    NOW)))

        self.assertTrue(HighFreqSmallInterval.validate(account,
                                                       Transaction('merchant_3',
                                                                   200,
                                                                   NOW+1000)))

    def test_doubled_transaction(self):
        NOW = self.now
        TWO_MINUTES_AGO = NOW - 120
        ONE_MINUTE_AGO = NOW - 60

        account = Account(self.account_1.active,
                          self.account_1.available_limit)

        account.history.extend([Transaction('merchant_1',
                                            100,
                                            TWO_MINUTES_AGO),
                                Transaction('merchant_2',
                                            200,
                                            ONE_MINUTE_AGO)])

        self.assertFalse(DoubledTransaction.validate(account,
                                                     Transaction('merchant_1',
                                                                 100,
                                                                 NOW)))

        self.assertFalse(DoubledTransaction.validate(account,
                                                     Transaction('merchant_2',
                                                                 200,
                                                                 NOW)))
        self.assertTrue(DoubledTransaction.validate(account,
                                                    Transaction('merchant_1',
                                                                150,
                                                                NOW)))

        self.assertTrue(DoubledTransaction.validate(account,
                                                    Transaction('merchant_5',
                                                                100,
                                                                NOW)))

        self.assertTrue(DoubledTransaction.validate(account,
                                                    Transaction('merchant_6',
                                                                123,
                                                                NOW)))

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
                          'violations': [NotActive]})

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

        assert account_active.active is True
        self.assertTrue(transaction in (account_active
                                        .authorize(transaction)['account']
                                        .history))
