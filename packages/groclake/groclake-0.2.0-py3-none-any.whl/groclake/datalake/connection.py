# connection.
import mysql.connector
import redis
from elasticsearch import Elasticsearch
import datetime


class Connection:
    def __init__(self):
        self.connection = None

    def connect(self):
        raise NotImplementedError("Subclasses must implement the connect method.")

    def read(self, query):
        raise NotImplementedError("Subclasses must implement the read method.")

class SQLConnection(Connection):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.cursor = None  # Initialize the cursor attribute

    def connect(self):
        if not self.connection:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor(dictionary=True)  # Create a cursor with dictionary support

    def read(self, query, params=None, multiple=False, parsed=True):
        """
        Executes a SELECT query and retrieves the result.

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters for the SQL query.
            fetch_all (bool): Whether to fetch all results or a single result.
            parsed (bool): Whether to parse results into a dictionary.

        Returns:
            list or dict: Query result as a list of dictionaries (fetch_all=True),
                          or a single dictionary (fetch_all=False and parsed=True).
        """
        cursor = self.connection.cursor(dictionary=parsed)
        try:
            cursor.execute(query, params)

            if multiple:
                # Fetch all rows and return as a list
                result = cursor.fetchall()
            else:
                # Fetch a single row
                result = cursor.fetchone()

            # Return an empty dictionary or list if no result is found
            if multiple and not result:
                return []
            elif not multiple and not result:
                return {} if parsed else None

            return result
        except mysql.connector.Error as err:
            raise Exception(f"MySQL query error: {err}")
        finally:
            cursor.close()

    def write(self, query, params=None):
        """
        Executes a write query and commits the transaction.

        Args:
            query (str): The SQL query to execute.
            params (tuple or None): Parameters to pass to the query.

        Returns:
            int: The last inserted ID if applicable.
        """
        if not self.connection:
            raise Exception("Connection not established. Call connect() first.")
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing write query: {e}")
            raise

    def close(self):
        """Closes the connection and cursor."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None


    #Add close method here as well

class RedisConnection(Connection):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def connect(self):
        self.connection = redis.StrictRedis(**self.config)

    def read(self, query):
        if not self.connection:
            raise Exception("Connection not established.")
        if query == "dbsize":
            return self.connection.dbsize()
        else:
            raise ValueError("Unsupported query for Redis.")

    def get(self, key):
        return self.connection.get(key)

    def set(self, key, value, cache_ttl=86400):
        """
        Set a value in Redis with an optional TTL (time-to-live).

        Args:
            key (str): The key to set in Redis.
            value (any): The value to associate with the key.
            cache_ttl (int): Time-to-live in seconds (default: 1 day).
        """
        self.connection.set(key, value, ex=cache_ttl)


class ESConnection(Connection):
    def __init__(self, es_host, es_port, es_api_key=None):
        super().__init__()
        self.es_host = es_host
        self.es_port = es_port
        self.api_key = es_api_key
        self.connection = None  # Initialize connection here

    def connect(self):
        """
        Establishes a connection to Elasticsearch
        """
        self.connection = Elasticsearch(
            f"http://{self.es_host}:{self.es_port}/",
            api_key=self.api_key
        )

    def read(self, query):
        """
        Executes a query to Elasticsearch, here 'query' contains 'index' dynamically passed in.
        """
        if not self.connection:
            raise Exception("Connection not established.")

        # Access 'index' dynamically from 'query' dictionary
        index = query.get('index')
        body = query.get('body')

        es_response = self.connection.count(index=index, body=body)
        return es_response.get("count", 0)

    def write(self, query, params=None):
        """
        Executes a write query to Elasticsearch, where 'index' is dynamically passed in.
        """
        if not self.connection:
            raise Exception("Connection not established.")

        index = query.get('index')
        body = query.get('body')

        try:
            response = self.connection.index(index=index, body=body)
            return response
        except Exception as e:
            raise Exception(f"Error executing write query: {e}")

    def search(self, query=None, index=None, body=None):
        """
        Executes a search query to Elasticsearch.
        Accepts a dictionary query or individual index and body arguments.
        """
        if not self.connection:
            raise Exception("Connection not established.")

        # Validate index and body
        if not index or not body:
            raise ValueError("Both 'index' and 'body' are required for the search query.")

        try:
            response = self.connection.search(index=index, body=body)
            return response
        except Exception as e:
            raise Exception(f"Error executing search query: {e}")
