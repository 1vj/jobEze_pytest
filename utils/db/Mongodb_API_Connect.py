import ssl
from pymongo import MongoClient
import logging

log = logging


class Mongodb_API_Connect:

    @staticmethod
    def connect_mongo_db(hostName, key_certFile, ca_certFile):
        """
        Method to connect mongo db using hostName, key certificate and ca certificate file.
        """
        log.info("Method to connect mongo db using hostName, key certificate and ca certificate file")
        try:
            client = MongoClient(
                host=hostName,
                port=27017,
                ssl=True,
                ssl_certfile=key_certFile,
                ssl_cert_reqs=ssl.CERT_REQUIRED,
                ssl_ca_certs=ca_certFile,
                ssl_match_hostname=False,
                serverSelectionTimeoutMS=5000
            )
            return client
        except Exception as e:
            log.error("Error while connecting to mongodb", e)

    @staticmethod
    def fetch_all_data(mongoClient, dbName, collectionName):
        """
        Method to connect mongo db and fetch all data from collections.
        """
        log.info("Method to connect mongo db and fetch all data from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.find()
        return data

    @staticmethod
    def fetch_all_data_with_condition(mongoClient, dbName, collectionName, condition):
        """
        Method to connect mongo db and fetch all data with given condition from collections.
        """
        log.info("Method to connect mongo db and fetch all data with given condition from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.find(condition)
        return data

    @staticmethod
    def fetch_one_data_with_condition(mongoClient, dbName, collectionName, condition):
        """
        Method to connect mongo db and fetch first data with given condition from collections.
        """
        log.info("Method to connect mongo db and fetch first data with given condition from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.find_one(condition)
        return data

    @staticmethod
    def fetch_one_data(mongoClient, dbName, collectionName):
        """
        Method to connect mongo db and fetch first data from collections.
        """
        log.info("Method to connect mongo db and fetch first data from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.find_one()
        return data

    @staticmethod
    def insert_one_data(mongoClient, dbName, collectionName, insertData):
        """
        Method to connect mongo db and insert one data to collections.
        """
        log.info("Method to connect mongo db and insert one data to collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.insert_one(insertData)
        return data

    @staticmethod
    def insert_multiple_data(mongoClient, dbName, collectionName, insertData):
        """
        Method to connect mongo db and insert many data to collections.
        """
        log.info("Method to connect mongo db and insert many data to collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.insert_many(insertData)
        return data

    @staticmethod
    def delete_one_data(mongoClient, dbName, collectionName, deleteQuery):
        """
        Method to connect mongo db and delete one data from collections.
        """
        log.info("Method to connect mongo db and delete one data from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.delete_one(deleteQuery)
        return data

    @staticmethod
    def delete_multiple_data(mongoClient, dbName, collectionName, deleteQuery):
        """
        Method to connect mongo db and delete many data from collections.
        """
        log.info("Method to connect mongo db and delete many data from collections")
        # Database Name
        db = mongoClient[dbName]

        # Collection Name
        col = db[collectionName]
        data = col.delete_many(deleteQuery)
        return data

    @staticmethod
    def close_mongo_db_connection(mongoClient):
        mongoClient.close()


# if __name__ == '__main__':
#     mdb = Mongodb_API_Connect()
#     ca_key = "C:/Users/radha/PycharmProjects/vcdautomation/certificates/mongodb-ca.pem"
#     cer_key = "C:/Users/radha/PycharmProjects/vcdautomation/certificates/mongodb-cert-key.pem"
#     host_name ="172.21.211.202"
#     db = mdb.connect_mongo_db(host_name, cer_key, ca_key)
#     opt = mdb.fetch_all_data(db, 'building_controller','devices')
#     for op in opt:
#         print(op)
