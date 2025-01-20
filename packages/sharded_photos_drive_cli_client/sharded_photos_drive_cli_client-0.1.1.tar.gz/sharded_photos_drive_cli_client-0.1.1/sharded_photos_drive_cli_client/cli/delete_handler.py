import logging


from .utils import get_diffs_from_path
from ..shared.config.config import Config
from ..shared.mongodb.clients_repository import MongoDbClientsRepository
from ..shared.mongodb.albums_repository import AlbumsRepositoryImpl
from ..shared.mongodb.media_items_repository import MediaItemsRepositoryImpl
from ..shared.gphotos.clients_repository import GPhotosClientsRepository
from ..backup.diffs import Diff
from ..backup.processed_diffs import DiffsProcessor
from ..backup.backup_photos import PhotosBackup

logger = logging.getLogger(__name__)


class DeleteHandler:
    """A class that handles deleting content from cli."""

    def delete(self, path: str, config: Config):
        """
        Deletes content from the system.

        Args:
            path (str): The path.
            config (Config): The config object
        """
        # Set up the repos
        mongodb_clients_repo = MongoDbClientsRepository.build_from_config(config)
        gphoto_clients_repo = GPhotosClientsRepository.build_from_config_repo(config)
        albums_repo = AlbumsRepositoryImpl(mongodb_clients_repo)
        media_items_repo = MediaItemsRepositoryImpl(mongodb_clients_repo)

        # Get the diffs
        diffs = [
            Diff(modifier="-", file_path=path) for path in get_diffs_from_path(path)
        ]

        # Process the diffs with metadata
        diff_processor = DiffsProcessor()
        processed_diffs = diff_processor.process_raw_diffs(diffs)
        for processed_diff in processed_diffs:
            logger.debug(f"Processed diff: {processed_diff}")

        # Process the diffs
        backup_service = PhotosBackup(
            config,
            albums_repo,
            media_items_repo,
            gphoto_clients_repo,
            mongodb_clients_repo,
        )
        backup_results = backup_service.backup(processed_diffs)
        logger.debug(f"Backup results: {backup_results}")
