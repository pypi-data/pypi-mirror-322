from dataclasses import InitVar, dataclass, field
from datetime import date

from .account import Account
from .transaction import RepeatingTransaction, Transaction


@dataclass(kw_only=True)
class Transfer(Transaction):
    """Record of a transfer between two accounts."""

    from_account: InitVar[Account]
    to_account: InitVar[Account]
    from_transaction: Transaction = field(init=False)
    to_transaction: Transaction = field(init=False)

    def __post_init__(self, from_account: Account, to_account: Account):
        """
        Create the from and to transactions, add them to the respective accounts,
        and set their parent to this transfer.
        """
        self.from_transaction = Transaction(
            self.description,
            -self.amount,
            self.date,
            cleared=self.cleared,
        )
        self.to_transaction = Transaction(
            self.description,
            self.amount,
            self.date,
            cleared=self.cleared,
        )

        self.from_transaction.parent = self.to_transaction.parent = self

        from_account.transactions.add(self.from_transaction)
        to_account.transactions.add(self.to_transaction)


@dataclass(kw_only=True)
class RepeatingTransfer(Transfer, RepeatingTransaction):
    """
    A transfer between two accounts that repeats on a schedule described by a
    `dateutil.rrule.rrule` or `dateutil.rrule.rruleset`.
    """

    @property
    def last_cleared(self) -> date | None:
        return super().last_cleared

    @last_cleared.setter
    def last_cleared(self, date: date | None):
        self._last_cleared = date
        self.from_transaction.last_cleared = self.to_transaction.last_cleared = date  # type: ignore

    def __post_init__(self, from_account: Account, to_account: Account):
        """
        Create the from and to repeating transactions, add them to the
        respective accounts, and set their parent to this repeating transfer.
        """
        self.from_transaction = RepeatingTransaction(
            self.description,
            -self.amount,
            parent=self,
            schedule=self.schedule,
        )

        self.to_transaction = RepeatingTransaction(
            self.description,
            self.amount,
            parent=self,
            schedule=self.schedule,
        )

        self.from_transaction.last_cleared = self.to_transaction.last_cleared = (
            self.last_cleared
        )

        from_account.repeating_transactions.add(self.from_transaction)
        to_account.repeating_transactions.add(self.to_transaction)
