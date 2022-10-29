"""Um sistema que autoriza ou rejeita transações seguindo regras predefinidas

    Desafio de código para o exercício de pair programming do processo seletivo para
    estágio 2023 do Nubank."""

from dataclasses import dataclass


class Violation(Exception):
    """An infringement of the authorizer's business logic."""

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


@dataclass
class Transaction:
    """A credit-card transaction."""
    merchant: str
    amount: int
    time: int


class Account:
    """A client's account.

    A client's account that stores their available limit, their status (active/
    inactive) and its history of successful transactions."""

    validations: tuple[Violation] = (NotInactive,)

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
                                           Account.validations))

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
