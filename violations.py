"""Violation classes for authorize.py"""


class Violation(Exception):
    """An infringement of the system's business logic."""

    def __init__(self, violation_name: str = ""):
        self._violation_name = violation_name

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self._violation_name

    @classmethod
    def validate(cls, account, transaction) -> bool | None:
        """Validates that the violation was not infringed."""

        raise NotImplementedError("Cannot validate generic violation")


class NotActive(Violation):
    """Violation that signals that the account was not active."""

    def __init__(self):
        super().__init__(violation_name="account-not-active")

    @classmethod
    def validate(cls, account, transaction) -> bool:
        """Validates that the violation was not infringed."""

        return account.active


class FirstAboveThreshold(Violation):
    THRESHOLD = 0.9

    def __init__(self):
        super().__init__(violation_name="first-transaction-above-threshold")

    @classmethod
    def validate(cls, account, transaction) -> bool:
        """Validates that the violation was not infringed."""

        return (True if account.history else
                (transaction.amount <=
                 account.available_limit * FirstAboveThreshold.THRESHOLD))


class InsufficientLimit(Violation):
    def __init__(self):
        super().__init__(violation_name="first-transaction-above-threshold")

    @classmethod
    def validate(cls, account, transaction) -> bool:
        """Validates that the violation was not infringed."""

        return (transaction.amount <= account.available_limit)


class HighFreqSmallInterval(Violation):
    def __init__(self):
        super().__init__(violation_name="high-frequency-small-interval")
        # TODO: REFACTOR TO ACCOUNT FOR TRANSACTIONS OUT OF ORDER

    @classmethod
    def validate(cls, account, transaction) -> bool:
        """Validates that the violation was not infringed."""
        TWO_MINUTES_S = 120

        if len(account.history) < 2:
            return True

        pre_prev = account.history[-2]
        return pre_prev.time < (transaction.time - TWO_MINUTES_S)


class DoubledTransaction(Violation):
    __TWO_MIN_IN_SEC = 120

    def __init__(self):
        super().__init__(violation_name="doubled-transaction")

    @classmethod
    def __doubled__(cls, transaction_1, transaction_2) -> bool:
        return (transaction_1.amount == transaction_2.amount and
                transaction_1.merchant == transaction_2.merchant and
                abs(transaction_2.time - transaction_1.time) <= cls.__TWO_MIN_IN_SEC)

    @classmethod
    def validate(cls, account, transaction) -> bool:
        """Validates that the violation was not infringed."""

        if not account.history:
            return True

        if len(account.history) == 1:
            prev = account.history[-1]
            return not cls.__doubled__(prev, transaction)

        if len(account.history) > 1:
            pre_prev, prev = account.history[-2:]
            return not cls.__doubled__(prev, transaction) and not cls.__doubled__(pre_prev, transaction)
