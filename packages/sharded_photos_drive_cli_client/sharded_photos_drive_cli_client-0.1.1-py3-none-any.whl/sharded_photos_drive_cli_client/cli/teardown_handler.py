from ..shared.config.config import Config
from ..shared.mongodb.clients_repository import MongoDbClientsRepository
from ..shared.mongodb.albums_repository import AlbumsRepositoryImpl, UpdatedAlbumFields
from ..shared.gphotos.clients_repository import GPhotosClientsRepository
from ..shared.gphotos.client import GPhotosClientV2


class TeardownHandler:
    """
    A class that deletes everything.
    """

    def teardown(self, config: Config):
        """
        Deletes everything from MongoDB database (except for the root album)
        and moves all photos uploaded to Google Photos to a trash album.

        Args:
            config (Config): The config.
        """
        self.__confirm_deletion_of_everything()

        mongodb_clients_repo = MongoDbClientsRepository.build_from_config(config)
        gphoto_clients_repo = GPhotosClientsRepository.build_from_config_repo(config)
        root_album_id = config.get_root_album_id()

        # Delete all albums from DB except for the root album
        for id, client in mongodb_clients_repo.get_all_clients():
            if root_album_id.client_id == id:
                client["sharded_google_photos"]["albums"].delete_many(
                    {"_id": {"$ne": root_album_id.object_id}}
                )
            else:
                client["sharded_google_photos"]["albums"].delete_many({})

        # Update the root album to not have any child elements
        albums_repo = AlbumsRepositoryImpl(mongodb_clients_repo)
        albums_repo.update_album(
            album_id=config.get_root_album_id(),
            updated_album_fields=UpdatedAlbumFields(new_child_album_ids=[]),
        )

        # Delete all media items from the DB
        for _, client in mongodb_clients_repo.get_all_clients():
            client["sharded_google_photos"]["media_items"].delete_many({})

        # Put all the photos that Google Photos has uploaded into a folder
        # called 'To delete'
        for _, gphotos_client in gphoto_clients_repo.get_all_clients():
            trash_album_id: str | None = None
            for album in gphotos_client.albums().list_albums(
                exclude_non_app_created_data=True
            ):
                if album.title == "To delete":
                    trash_album_id = album.id
                    break

            if not trash_album_id:
                trash_album_id = gphotos_client.albums().create_album("To delete").id

            media_item_ids = [
                m.id for m in gphotos_client.media_items().search_for_media_items()
            ]
            if len(media_item_ids) > 0:
                self.__add_media_items_to_album_safely(
                    gphotos_client, trash_album_id, media_item_ids
                )

    def __confirm_deletion_of_everything(self):
        print("Do you want to delete everything this tool has ever created?")
        while True:
            raw_input = input("[Yes/Y] or [No/N]: ")
            user_input = raw_input.strip().lower()

            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                raise ValueError("Terminated teardown.")
            else:
                print("Invalid input. Please enter Yes/Y or No/N.")

    def __add_media_items_to_album_safely(
        self, client: GPhotosClientV2, album_id: str, media_item_ids: list[str]
    ):
        MAX_UPLOAD_TOKEN_LENGTH_PER_CALL = 50

        for i in range(0, len(media_item_ids), MAX_UPLOAD_TOKEN_LENGTH_PER_CALL):
            chunked_media_item_ids = media_item_ids[
                i : i + MAX_UPLOAD_TOKEN_LENGTH_PER_CALL
            ]
            client.albums().add_photos_to_album(album_id, chunked_media_item_ids)
