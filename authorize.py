"""A system that authorizes transactions following predefined rules.

    Coding challenge for the pair programming exercise for Nubank's 2023 intern-
    ship selection process."""

from dataclasses import dataclass
import sys
try:
    sys.path.append('..//')
    from violations import (Violation,
                            NotActive,
                            FirstAboveThreshold,
                            InsufficientLimit,
                            HighFreqSmallInterval,
                            DoubledTransaction)
except ModuleNotFoundError:
    pass


@dataclass
class Transaction:
    """A credit-card transaction."""

    merchant: str
    amount: int  # cents
    time: int


class Account:
    """A client's account.

    A client's account that stores their available limit, their status (active/
    inactive) and its history of successful transactions."""

    _VALIDATIONS: tuple[Violation] = (NotActive,
                                      FirstAboveThreshold,
                                      InsufficientLimit,
                                      HighFreqSmallInterval,
                                      DoubledTransaction)

    def __init__(self, active: bool = True, available_limit: int = 0) -> None:
        self.active = active
        self.available_limit = available_limit
        self.history: list[Transaction] = []

    def authorize(self, transaction: Transaction) -> dict[str, str]:
        """If authorized, registers a transaction.

        If the transaction is valid, authorizes it, adds it to the history.

        Returns the result with the account and violations (if any)."""

        infringed_violations = list(filter(lambda v: not v.validate(account=self,
                                                                    transaction=transaction),
                                           Account._VALIDATIONS))

        if not infringed_violations:
            self.history.append(transaction)
            self.available_limit -= transaction.amount

        return {'account': self,
                'violations': infringed_violations}

    def __eq__(self, other):
        return (isinstance(other, Account) and
                self.active == other.active and
                self.available_limit == other.available_limit and
                self.history == other.history)
