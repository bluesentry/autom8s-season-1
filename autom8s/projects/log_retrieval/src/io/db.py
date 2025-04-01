from dataclasses import dataclass

from .crud import Read, ReadWrite, Write


@dataclass
class DBConnection:
    connection: str

    @classmethod
    def from_connection_string(cls, connection_string: str):
        connection = Something(auth=connection_string)
        return cls(conection)

    def __enter__(self):
        # Implementation for entering the database connection
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # Implementation for exiting the database connection
        self.connection.close()

    def save_entry(self, entry: type[Write]) -> None:
        # Implementation for saving data to the database
        pass

    def retrieve_entry(self, entry_id: int) -> type[Read]:
        # Implementation for retrieving data from the database
        pass

    def update_entry(self, entry: type[ReadWrite]) -> None:
        # Implementation for updating data in the database
        pass

    def delete_entry(self, entry_id: int) -> None:
        # Implementation for deleting data from the database
        pass
