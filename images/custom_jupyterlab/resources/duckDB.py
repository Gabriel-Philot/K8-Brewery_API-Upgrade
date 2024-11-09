from resources.utils.utils import load_config
import duckdb

class DuckDBMinIOConnector:
    def __init__(self):
        """
        Initializes the DuckDB connection with MinIO and loads the connection settings and paths.
        """
        # Load the MinIO and paths settings
        config = load_config()
        
        self.minio_endpoint = config['minio_dev']['endpoint_url_duckdb']
        self.minio_access_key = config['minio_dev']['access_key']
        self.minio_secret_key = config["minio_dev"]["secret_key"]
        self.brew_paths = config["storages"]["brew_paths_duckdb"]

        # Configure the connection
        self.conn = self._create_duckdb_connection()
    
    def _create_duckdb_connection(self) -> duckdb.DuckDBPyConnection:
        """
        Establishes a connection with the DuckDB and configures the MinIO access.

        Returns:
            duckdb.DuckDBPyConnection: DuckDB connection object.
        """
        try:
            print("Connecting to DuckDB")
            conn = duckdb.connect(database=':memory:')
            
            # Install and load the necessary extensions
            print("Installing and loading HTTPFS and Delta extensions")
            conn.execute("INSTALL httpfs;")
            conn.execute("LOAD httpfs;")
            conn.execute("INSTALL delta;")
            conn.execute("LOAD delta;")
            
            # Create the S3 secret for accessing MinIO
            print("Creating and configuring the S3 secret")
            conn.execute(f"""
                CREATE SECRET delta_s3 (
                    TYPE S3,
                    KEY_ID '{self.minio_access_key}',
                    SECRET '{self.minio_secret_key}',
                    REGION '',
                    ENDPOINT '{self.minio_endpoint}',
                    URL_STYLE 'path',
                    USE_SSL 'false'
                );
            """)
            
            print("Connection with DuckDB established and secret configured")
            return conn
        except Exception as e:
            print(f"Error connecting to DuckDB: {e}")
            return None

    def execute_query(self, layer: str, file_format: str, query: str):
            """
            Executes a SQL query on the specified layer (Bronze, Silver or Gold) with the appropriate file format.

            Args:
                layer (str): The layer of the data (bronze, silver or gold).
                file_format (str): The file format of the layer ('json', 'delta', etc.).
                query (str): The SQL query to be executed.

            Returns:
                DataFrame: The result of the query as a DuckDB DataFrame.
            """
            # Checks the layer path
            layer_path = self.brew_paths.get(layer)
            if not layer_path:
                print(f"Error: Layer '{layer}' not found in the configurations.")
                return None

            # Defines the table name based on the layer
            table_name = f"{layer}_data"

            # Builds the query to access the data based on the file format
            try:
                print(f"Trying to load data from path {layer_path} in format {file_format} and execute the query...")
                if file_format.lower() == 'json':
                    self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_json_auto('{layer_path}*.json')")
                elif file_format.lower() == 'delta':
                    self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM delta_scan('{layer_path}')")
                else:
                    print(f"File format '{file_format}' not supported for layer {layer}.")
                    return None

                # Replaces the table name in the query
                query_with_table = query.replace("{{table}}", table_name)
                result = self.conn.execute(query_with_table).fetchdf()
                print(f"Query executed successfully on layer {layer}.")
                return result
            except Exception as e:
                print(f"Error loading data and executing query: {e}")
                return None
    
    def close_connection(self):
        """Closes the connection with DuckDB."""
        if self.conn:
            self.conn.close()
            print("Connection with DuckDB closed.")
