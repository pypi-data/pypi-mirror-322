from pypigeon.pigeon_core.api.collections import collections_create_collection
from pypigeon.pigeon_core.api.collections import collections_delete_collection_version
from pypigeon.pigeon_core.api.collections import collections_get_collections
from pypigeon.pigeon_core.models import NewCollection

from .base_commands import BaseCommands


class CollectionCommands(BaseCommands):
    """Operations on collections"""

    def list(self) -> None:
        """List all visible collections."""
        collections = collections_get_collections.sync(client=self.core)

        self._output(collections.to_dict())

    @BaseCommands._with_arg("name", help="Collection name, required")
    @BaseCommands._with_arg(
        "-d", "--description", help="Collection description", default=""
    )
    def new(self) -> None:
        """Create a new collection."""
        collection = collections_create_collection.sync(
            body=NewCollection(
                name=self.args.name,
                description=self.args.description,
            ),
            client=self.core,
        )

        self._output(collection.to_dict())

    @BaseCommands._with_arg("collection_id", help="Collection ID")
    @BaseCommands._with_arg(
        "-v", "--version_id", help="Collection version ID", default="LIVE"
    )
    def delete(self) -> None:
        """Delete a collection."""
        rv = collections_delete_collection_version.sync(
            collection_id=self.args.collection_id,
            version_id=self.args.version_id,
            client=self.core,
        )
        assert rv
