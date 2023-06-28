import threading
from typing import Dict

from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult


class Database:
    """
        Contains a singleton instance of mongo database to interact with
    """
    _instance = None
    _database = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)

                    if "host" in kwargs:
                        host = kwargs["host"]
                    else:
                        host = "localhost"

                    if "port" in kwargs:
                        port = kwargs["port"]
                    else:
                        port = 27017

                    if "database" in kwargs:
                        database = kwargs["database"]
                    else:
                        database = "bienestar_emocional"

                    cls._database = MongoClient(host, port).get_database(database)
        return cls._instance

    @staticmethod
    def insert_user_data(data: Dict) -> InsertOneResult:
        """
        Insert data into user_data collection
        :param data: data to insert
        :return: InsertOneResult of the execution
        """
        collection = Database._database.get_collection('user_data')
        return collection.insert_one(data)

    @staticmethod
    def insert_daily_questionnaires(data: Dict) -> InsertManyResult:
        """
        Insert data into daily_questionnaires collection
        :param data: data to insert
        :return: InsertManyResult of the execution
        """
        collection = Database._database.get_collection('daily_questionnaires')

        processed_data = []

        for key in data["data"]:
            for element in data["data"][key]:
                values = element
                values.update({"type": key, "userId": data["userId"]})
                values.pop("id")
                processed_data.append(values)
        return collection.insert_many(processed_data)

    @staticmethod
    def insert_one_off_questionnaires(data: Dict) -> InsertManyResult:
        """
        Insert data into one_off_questionnaires collection
        :param data: data to insert
        :return: InsertManyResult of the execution
        """
        collection = Database._database.get_collection('one_off_questionnaires')

        processed_data = []

        for key in data["data"]:
            for element in data["data"][key]:
                values = element
                values.update({"type": key, "userId": data["userId"]})
                values.pop("id")
                processed_data.append(values)
        return collection.insert_many(processed_data)

    @staticmethod
    def get_daily_questionnaires_average(start: int, end: int) -> Dict:
        """
            Obtain the average score of all scored measures filter by timestamps
            :param start: filter by greater than or equals this value
            :param end: filter by less than this value
            :return: Dict with measure and score
        """
        collection = Database._database.get_collection('daily_questionnaires')
        query = collection.aggregate(
            [
                {
                    "$match":
                        {
                            "createdAt":
                                {
                                    "$gte": start,
                                    "$lt": end
                                },
                            "score":
                                {
                                    "$gte": 0,
                                }
                        }
                },
                {
                    "$group":
                        {
                            "_id": "$type",
                            "average":
                                {
                                    "$avg": "$score"
                                }
                        }
                }
            ]
        )
        return {item["_id"]: round(item["average"], 2) for item in query}

    @staticmethod
    def insert_user_databg(databg: Dict) -> InsertOneResult:
        """
        Insert background data into user_databg collection
        :param databg: data to insert
        :return: InsertOneResult of the execution
        """
        collection = Database._database.get_collection('user_databg')
        return collection.insert_one(databg)
