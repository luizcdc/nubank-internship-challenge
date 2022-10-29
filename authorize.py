class Violation(Exception):
    def __init__(self, violation_name: str = ""):
        self._violation_name = violation_name

    def __repr__(self) -> str:
        return self._violation_name

    @classmethod
    def validate(cls, account, transaction) -> bool | None:
        raise Exception("NOT IMPLEMENTED")


class NotInactive(Violation):
    def __init__(self):
        super().__init__(violation_name="account-not-active")

    @classmethod
    def validate(cls, account, transaction) -> bool:
        return account.active


class Transaction:
    def __init__(self, merchant: str, amount: int, time: int):
        self.merchant = merchant
        self.amount = amount
        self.time = time


class Account:
    validations: tuple[Violation] = (NotInactive)

    def __init__(self, active: bool = True, available_limit: int = 0) -> None:
        self.active = active
        self.available_limit = available_limit
        self.history: list[Transaction] = []

    def authorize(self, transaction: Transaction) -> dict[str, str]:
        """If authorized, registers a transaction

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
