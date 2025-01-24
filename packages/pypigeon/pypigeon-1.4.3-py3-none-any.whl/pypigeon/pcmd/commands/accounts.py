from pypigeon.pigeon_core.api.account import account_create_account
from pypigeon.pigeon_core.api.account import account_delete_account
from pypigeon.pigeon_core.api.account import account_list_accounts
from pypigeon.pigeon_core.models import AccountCreateAccountBody

from .base_commands import BaseCommands


class AccountsCommands(BaseCommands):
    """Operations on accounts"""

    @BaseCommands._with_arg("name")
    def new(self) -> None:
        """Create a new account."""
        rv = account_create_account.sync(
            body=AccountCreateAccountBody(name=self.args.name), client=self.core
        )

        self._output(rv.to_dict())

    def list(self) -> None:
        """List all accounts."""
        rv = account_list_accounts.sync(client=self.core)

        self._output(rv.to_dict())

    @BaseCommands._with_arg("account_id")
    def delete(self) -> None:
        """Remove an account."""
        rv = account_delete_account.sync(
            account_id=self.args.account_id, client=self.core
        )
        assert rv
