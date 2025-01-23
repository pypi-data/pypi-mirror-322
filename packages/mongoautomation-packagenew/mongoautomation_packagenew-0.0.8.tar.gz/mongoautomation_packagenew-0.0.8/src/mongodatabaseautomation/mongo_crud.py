from pymongo import MongoClient
from typing import Any, Optional
import pandas as pd
import json


class mongo:
    __collection: Optional[str] = None  # private/protected variable
    __database: Optional[str] = None
    client: Optional[MongoClient] = None

    def __init__(self, client_url: str, database_name: str, collection_name: Optional[str] = None):
        self.client_url: str = client_url
        self.database_name: str = database_name
        self.collection_name: Optional[str] = collection_name

    def create_mongo_client(self, collection: Optional[str] = None) -> MongoClient:
        self.client = MongoClient(self.client_url)
        return self.client
    
    def create_database(self, collection: Optional[str] = None) -> Any:
        if mongo.__database is None:  # Check if self.database is None
            client = self.create_mongo_client(collection)
            self.database = client[self.database_name]  # Initialize self.database here
        return self.database

    def set_new_database(self, database: str) -> None:
        self.database = self.create_mongo_client()[database]
        mongo.__database = database
        self.database_name = database

    def set_new_collection(self, collection_name: str) -> None:
        self.collection = self.__connect_database()[collection_name]
        mongo.__collection = collection_name
        self.collection_name = collection_name

    def __connect_database(self) -> Any:
        if mongo.__database is None:
            self.database = self.create_mongo_client()[self.database_name]
        return self.database

    def create_collection(self, collection_name: Optional[str] = None) -> Any:
        if mongo.__collection is None:
            database = self.create_database(collection_name)
            self.collection = database[self.collection_name]
            mongo.__collection = collection_name

        if mongo.__collection != collection_name:
            database = self.create_database(collection_name)
            self.collection = database[self.collection_name]
            mongo.__collection = collection_name

        return self.collection

    def insert_record(self, record: dict, collection_name: str) -> None:
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("record must be a dict")
            collection = self.create_collection(collection_name)
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection = self.create_collection(collection_name)
            collection.insert_one(record)
        else:
            raise TypeError("record must be a dict or list of dicts")

    def bulk_insert(self, datafile: str, collection_name: Optional[str] = None) -> None:
        self.path = datafile

        if self.path.endswith('.csv'):
            dataframe = pd.read_csv(self.path, encoding='utf-8')
        elif self.path.endswith(".xlsx"):
            dataframe = pd.read_excel(self.path)
        else:
            raise ValueError("Unsupported file format")
        # Explicitly ensure to_json() result is valid
        json_data = dataframe.to_json(orient='records') or "[]"
        datajson = json.loads(json_data)
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)

    def update_record(
        self,
        query: dict,
        update_data: dict,
        collection_name: Optional[str] = None,
        update_all: bool = False,
    ) -> int:
        collection = self.create_collection(collection_name)

        if update_all:
            result = collection.update_many(query, {"$set": update_data})
        else:
            result = collection.update_one(query, {"$set": update_data})

        return result.modified_count

    def delete_record(
        self,
        query: dict,
        collection_name: Optional[str] = None,
        delete_all: bool = False,
    ) -> int:
        collection = self.create_collection(collection_name)

        if delete_all:
            result = collection.delete_many(query)
        else:
            result = collection.delete_one(query)

        return result.deleted_count
