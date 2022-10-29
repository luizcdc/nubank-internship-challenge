"""Violation classes for authorize.py"""


class Violation(Exception):
    """An infringement of the system's business logic."""

    def __init__(self, violation_name: str = ""):
        self._violation_name = violation_name

    def __repr__(self) -> str:
        return self._violation_name

    @classmethod
    def validate(cls, account, transaction) -> bool | None:
        """Validates that the violation was not infringed."""

        raise NotImplementedError("Cannot validate generic violation")


class NotInactive(Violation):
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