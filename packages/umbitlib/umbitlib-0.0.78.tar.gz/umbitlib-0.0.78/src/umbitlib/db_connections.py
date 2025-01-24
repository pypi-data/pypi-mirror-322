#%%
# Imports
import keyring as kr
import pandas as pd
import time
from urllib import parse
from typing import Protocol, Dict, Optional
import yaml
import sqlalchemy as sa
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Protocol
from warnings import filterwarnings
filterwarnings("ignore")
from umbitlib.helpers import convert_seconds
from umbitlib.helpers import generate_sqlalchemy_dtypes
#####################################################################################################################
# LEGACY
#####################################################################################################################
# Security
class SecurityHandler:
    """
    A class for handling security operations for various services.

    This class provides methods for initializing security instances and accessing service credentials.

    Args:
        service_name (str): The desired service name for security operations.
        NOTE: Valid service names: {'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'}

    Raises:
        ValueError: If the provided service_name is not one of the valid options.

    Example:
        orc = SecurityHandler('oracle')
    """

    _VALID_SERVICE_NAMES = {'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc', 'umb_auto1', 'umb_auto2'}

    def __init__(self, service_name, username=None):
        """
        Initializes a security instance

        Args:
        service_name (str): The desired service_name for security operations.
        username (str): The user name associated with the service_name

        Raises:
        ValueError: If the provided service_name is not one of the valid options.

        Example:
        orc = SecurityHandler('oracle')
        orc = SecurityHandler('oracle','u0062202')
        """

        self._service_name = service_name.lower()
        self._username = username

        if self._service_name not in self._VALID_SERVICE_NAMES:
            raise ValueError(f"Invalid service_name '{self._service_name}'. Valid options are: {', '.join(self._VALID_SERVICE_NAMES)}")

        self._security_obj = kr.get_credential(service_name=self._service_name, username=self._username)
        self._username = self._security_obj.username
        self._password = parse.quote_plus(self._security_obj.password)

    # Use of the @property decorator with no accompanying setter method ensures that the service_name cannot be set 
    # to another value after initialization. (Unless the user calls _service_name which is technically private)
    @property
    def service_name(self):
        """
        str: The selected service_name for security operations.
        """
        return self._service_name
    
    @property
    def username(self):
        """
        str: The selected username for security operations.
        """
        return self._username
    
    @property
    def password(self):
        """
        str: The encoded password for the service.
        """
        return self._password

# Engine Handler
class DatabaseEngine(SecurityHandler):
    """
    A class for managing database connections with various engines.

    This class inherits from SecurityHandler and provides methods to create database connections
    for different database engines, such as Oracle and PostgreSQL.

    Args:
        service_name (str): The desired service name for security operations, inherited from SecurityHandler.

    Example:
        engine = DatabaseEngine('oracle')
    """

    def __init__(self, service_name):
        """
        Initializes a database engine instance and establishes a connection to the specified database.

        Args:
            service_name (str): The desired service name for security operations, inherited from SecurityHandler.

        Example:
            engine = DatabaseEngine('oracle')
        """
        super().__init__(service_name)

        try:
            import sys
            sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
            import db_conn_vars

        except ModuleNotFoundError as e:
            print(f"Security file not found: {e}")
            pass

        if self.service_name in ['oracle', 'oracle_serv_acc', 'umb_auto1', 'umb_auto2']:
            self._dsn = db_conn_vars.ODB_NAME
            self.engine = sa.create_engine(f"oracle+cx_oracle://{self.username}:{self._password}@{self._dsn}", echo=False)  # Set echo=True for debugging

        elif self.service_name in ['postgres_dev', 'postgres_prod', 'postgres_serv_acc']:
            if self.service_name == 'postgres_dev':
                self._db = db_conn_vars.PG_DEV_DB
                self._host = db_conn_vars.PG_DEV_HOST
                self._port = db_conn_vars.PG_DEV_PORT
            elif self.service_name == 'postgres_prod':
                self._db = db_conn_vars.PG_PROD_DB
                self._host = db_conn_vars.PG_PROD_HOST
                self._port = db_conn_vars.PG_PROD_PORT

            self.engine = create_engine(f"postgresql://{self.username}:{self._password}@{self._host}:{self._port}/{self._db}")

# SQL Handler
class SqlHandler(DatabaseEngine):
    """
    A class for executing SQL statements against databases.

    This class inherits from DatabaseEngine and provides methods for executing SQL queries on the database
    and uploading DataFrames to the database tables making a usable connection and other standard SQL functions.

    Args:
        service_name (str): The desired service name for security operations, inherited from DatabaseEngine.

    Example:
        sql_handler = SqlHandler('oracle')
    """

    def __init__(self, service_name):
        """
        Initializes an SQL handler instance.

        Args:
            service_name (str): The desired service name for security operations, inherited from DatabaseEngine.

        Example:
            sql_handler = SqlHandler('oracle')
        """
        super().__init__(service_name)


    def connect(self, conn_success_msg: bool = True):
        """
        Creates a connection to a database.  Requires that the programmer closes the connection in a separate statment.

        Args:
            conn_success_msg (bool): Determines if connection successful message will print out or not. Default = True

        Returns:
            A connection to the specified database
        
        Example:
            sql_handler = SqlHandler('oracle')

            sql_conn = sql_handler.connect()

                //your code here//

            sql_conn.close()
        """
        try:
            sql_connection = self.engine.connect()
            if conn_success_msg:
                print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful. Use of this function requires manual closing of this connection upon end of use.")
            return sql_connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None


    def query(self, sql_query, conn_success_msg: bool = True, sql_success_msg: bool = True):
        """
        Execute a SQL query on the database and return the result as a DataFrame.

        Args:
            sql_query (str): The SQL query to execute.
            conn_success_msg (bool): Turns on or off the output of the connection success message (default is True)
            query_success_msg (bool): Turns on or off the output of the query success message and runtime (default is True)

        Returns:
            pandas.DataFrame: A DataFrame containing the query result.

        Example:
            sql_handler = SqlHandler('oracle')

            df = sql_handler.query('SELECT * FROM your_table')
        """
        try:
            with self.engine.connect() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful")
                sql_text = sa.text(sql_query)
                tic = time.perf_counter()
                result_df = pd.read_sql(sql_text, con=connection)
                toc = time.perf_counter() 

                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
            
            return result_df
        except Exception as e:
            print(f"Error executing query against {self.service_name}: {e}.")
            return None
        
    
    def upload_df(self, dataframe, table_name, table_mgmt='truncate', index=False, dtype=None, conn_success_msg: bool = True, sql_success_msg: bool = True):
        """
        Upload a DataFrame to the database. By default, this function converts the dataframe column types to sqlalchmeny column types when uploading.
        A user can override this auto-conversion by passing their own dict of column typing where the key is the column_name and the value
        is the sqlalchemy_column_type.  

        Args:
            dataframe (pandas.DataFrame): The DataFrame to upload.
            table_name (str): The name of the table to upload the DataFrame to.
            if_exists (str, optional): How to behave if the table already exists. Defaults to 'truncate'. ('truncate', 'replace', 'append', 'fail')
            index (bool, optional): Whether to include the DataFrame index as a column. Defaults to False.
            dtype (dict, optional): Overrides the auto type detection with user-defined type mapping that is applied to the columns. Defaults to None.
            conn_success_msg (bool): Turns on or off the output of the connection success message (default is True)
            query_success_msg (bool): Turns on or off the output of the query success message and runtime (default is True)

        Example:
            sql_handler = SqlHandler('oracle')

            sql_handler.upload_df(your_dataframe, 'my_table')

            Example without auto_dtype:
                import sqlalchemy as sa

                my_dtypes = {'int_col': sa.types.INTEGER(),
                            'str_col': sa.types.VARCHAR(length=30),
                            'bool_col': sa.types.BOOLEAN(),
                            'dt': sa.types.DATE()}

                sql_handler.upload_df(your_dataframe, 'my_table' , dtype=my_dtypes)

        Notes:
            For full list of acceptable types see https://docs.sqlalchemy.org/en/20/core/type_basics.html#types-sqlstandard 
            under the SQL Standard and Multiple Vendor “UPPERCASE” Types section

            The automatic conversion is based on the dataframe's datatypes. Hence, if a date field is listed as an object datatype 
            in the dataframe the auto-conversion will set it as a VARCHAR.  To rectify this, please cast your dataframe columns to 
            the desired data types prior to using this function or override the auto-conversion using the dtype argument.  
            In the example given if the auto-conversion is overridden and a date (which is an object datatype in the df) is set to 
            a sqlalchemy date then it will upload as a date.
        """
        try:
            pg_dtype = generate_sqlalchemy_dtypes(dataframe)

            if dtype is not None:
                pg_dtype = dtype
            
            # Upload DataFrame
            with self.engine.begin() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful")

                tic = time.perf_counter()
                if table_mgmt == 'truncate':
                    trunc_sql = sa.text(f'TRUNCATE TABLE {table_name}')
                    connection.execute(trunc_sql)
                    dataframe.to_sql(table_name, connection, if_exists='append', index=index, dtype=pg_dtype)
                else:
                    dataframe.to_sql(table_name, connection, if_exists=table_mgmt, index=index, dtype=pg_dtype)
                toc = time.perf_counter() 

                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Sql executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
                
            print(f"DataFrame uploaded successfully to {self.service_name}.")
            
        except Exception as e:
            print(f"Error uploading DataFrame to {self.service_name}:", str(e))

    
    def drop_table(self, table_name, conn_success_msg: bool = True, sql_success_msg: bool = True):
        """
        Drop a table from the database.

        Args:
            table_name (str): The name of the table to drop.
            conn_success_msg (bool, optional): Whether to print connection success message.
                Defaults to True.
            sql_success_msg (bool, optional): Whether to print SQL execution success message.
                Defaults to True.

        Returns:
            None

        Raises:
            Exception: If there's an error executing the DROP TABLE statement.

        Example:
            sql_handler = SqlHandler('postgres_dev')
            
            sql_handler.drop_table('my_table')
        """

        try:    
            with self.engine.begin() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful")

                drop_sql = sa.text(f"DROP TABLE IF EXISTS {table_name};")
                tic = time.perf_counter()    
                connection.execute(drop_sql)
                toc = time.perf_counter()

                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Sql executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass

            print(f"Table {table_name} dropped successfully from {self.service_name}.")
            
        except Exception as e:
            print(f"Error executing DROP TABLE from {self.service_name}:", str(e))
            
#####################################################################################################################
# UPDATED
#####################################################################################################################
# Security Handling
class CredentialProvider(Protocol):
    """Protocol for providing credentials.
    Defines the interface for retrieving credentials for a given service and username.
    """
    def get_credentials(self, service_name: str, username: Optional[str]) -> Dict[str, str]:
        """Protocol method to get credentials"""

class KeyringCredentialProvider:
    """Provides credentials using the system's keyring.

    This class implements the CredentialProvider protocol by using the 'keyring' library
    to store and retrieve credentials.
    """
    def get_credentials(self, service_name: str, username: Optional[str] = None) -> Dict[str, str]:
        """Gets credentials from a credential store.

        Args:
            service_name: The name of the service for which to retrieve credentials.
            username: The username for which to retrieve credentials. Can be None.

        Returns:
            A dictionary containing the 'username' and 'password'.

        Raises:
            Any exception raised by the underlying credential store if credentials are not found or an error occurs.
        """
        security_obj = kr.get_credential(service_name=service_name, username=username)
        if security_obj is None:
            raise ValueError(f"No credentials found for service: {service_name}, username: {username}")
        return {
            "username": security_obj.username,
            "password": parse.quote_plus(security_obj.password),
        }

# TNS Configuration Loading
class TNSConfigLoader(Protocol):
    """Protocol for loading TNS (Transparent Network Substrate) addresses from a configuration file.
    Defines the interface for retrieving a specific address from a TNS configuration.
    """
    def load_tns_address(self, config_file: str, entry_name: str, address_name: str) -> Dict:
        """Protocol method for loading a tns config file"""

class YamlTNSConfigLoader:
    """Loads TNS addresses from a YAML configuration file.

    This class implements the TNSConfigLoader protocol by parsing a YAML file
    containing TNS entries and addresses.
    """
    class TNSConfigError(Exception):
        """Custom exception for TNS configuration errors."""
        pass

    def load_tns_address(self, config_file: str, entry_name: str, address_name: str) -> Dict:
        """Loads a TNS address from a YAML configuration file.

        Args:
            config_file: The path to the YAML configuration file.
            entry_name: The name of the TNS entry to retrieve.
            address_name: The name of the address within the entry to retrieve.

        Returns:
            A dictionary containing the address information.

        Raises:
            TNSConfigError: If the configuration file is not found, contains invalid YAML, or if the specified entry or address is not found.
        """
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
                tns_entries = config.get("tns_entries")
                if not tns_entries:
                    raise self.TNSConfigError("Key 'tns_entries' not found in config.")

                tns_entry = tns_entries.get(entry_name)
                if not tns_entry:
                    raise self.TNSConfigError(f"TNS entry '{entry_name}' not found.")

                description = tns_entry.get("DESCRIPTION")
                if not description:
                    raise self.TNSConfigError(f"Key 'DESCRIPTION' not found in entry '{entry_name}'.")

                address_list = description.get("ADDRESS_LIST")
                if address_list:
                    matching_addresses = [
                        address_data["ADDRESS"]
                        for address_data in address_list
                        if address_data.get("ADDRESS", {}).get("NAME") == address_name
                    ]
                    if matching_addresses:
                        return matching_addresses[0]
                    else:
                        raise self.TNSConfigError(f"Address with name '{address_name}' not found in entry '{entry_name}'.")
                else:
                    address = description.get("ADDRESS")
                    if address and address.get("NAME") == address_name:
                        return address
                    else:
                        raise self.TNSConfigError(f"Address with name '{address_name}' not found in entry '{entry_name}'.")

        except FileNotFoundError:
            raise self.TNSConfigError(f"Config file '{config_file}' not found.") from None
        except yaml.YAMLError as e:
            raise self.TNSConfigError(f"Invalid YAML in '{config_file}': {e}") from e
        except self.TNSConfigError as e:
            raise
        except Exception as e:
            raise self.TNSConfigError(f"An unexpected error occurred: {e}") from e

# Database Engine Factory
class DatabaseEngineFactory(Protocol):
    """Protocol for creating database engines.

    Defines the interface for creating a SQLAlchemy Engine object for a given database.
    """
    def create_engine(self, db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine:
        """Protocol method for creating a sql engine."""

class OracleEngineFactory:
    """Creates Oracle database engines.

    This class implements the DatabaseEngineFactory protocol for creating
    SQLAlchemy Engine objects for Oracle databases using cx_Oracle.
    """
    def create_engine(self, db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine:
        """Creates an Oracle database engine.

        Args:
            db_name: The TNS name or connection string alias.
            tns: This parameter is not used for Oracle connections in this implementation.
            username: The database username.
            password: The database password.

        Returns:
            A SQLAlchemy Engine object for Oracle.
        """
        return create_engine(
            f"oracle+cx_oracle://{username}:{password}@{db_name}",
            echo=False
        )

class PostgresEngineFactory:
    """Creates PostgreSQL database engines.

    This class implements the DatabaseEngineFactory protocol for creating
    SQLAlchemy Engine objects for PostgreSQL databases.
    """
    def create_engine(self, db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine:
        """Creates a PostgreSQL database engine.

        Args:
            db_name: The name of the database.
            tns: A dictionary containing TNS information, specifically 'HOST' and 'PORT'.
            username: The database username.
            password: The database password.

        Returns:
            A SQLAlchemy Engine object for PostgreSQL.
        Raises:
            KeyError: If the 'HOST' or 'PORT' keys are not present in the tns dictionary.
        """
        return create_engine(
            f"postgresql://{username}:{password}@{tns['HOST']}:{tns['PORT']}/{db_name}"
        )

# Database Engine Controller
class DatabaseEngineController:
    def __init__(self, config_file: str, credential_provider: CredentialProvider, tns_config_loader: TNSConfigLoader):
        self.config_file = config_file
        self.credential_provider = credential_provider
        self.tns_config_loader = tns_config_loader
        self.factories: Dict[str, DatabaseEngineFactory] = {
            "oracle": OracleEngineFactory(),
            "oracle_serv_acc": OracleEngineFactory(),
            "umb_auto1": OracleEngineFactory(),
            "umb_auto2": OracleEngineFactory(),
            "postgres_dev": PostgresEngineFactory(),
            "postgres_prod": PostgresEngineFactory(),
            "postgres_serv_acc": PostgresEngineFactory(),
        }
        self.db_names = {
            "oracle": 'DWRAC_UMB_UUMG',
            "oracle_serv_acc": 'DWRAC_UMB_UUMG',
            "umb_auto1": 'DWRAC_UMB_UUMG',
            "umb_auto2": 'DWRAC_UMB_UUMG',
            "postgres_dev": 'umbdb',
            "postgres_prod": 'umbdb',
            "postgres_serv_acc": 'umbdb',
        }

    def get_engine(self, service_name: str, username: Optional[str] = None) -> sa.engine.Engine:
        credentials = self.credential_provider.get_credentials(service_name, username)
        db_name = self.db_names.get(service_name)
        if not db_name:
            raise ValueError(f"Unsupported service name: {service_name}")

        factory = self.factories.get(service_name)
        if not factory:
            raise ValueError(f"No factory found for service_name '{service_name}'.")

        tns = self.tns_config_loader.load_tns_address(self.config_file, db_name, service_name)
        return factory.create_engine(db_name, tns, credentials["username"], credentials["password"])

# Sql Manager
class SqlManagerFactory:
    """Factory for creating SqlManager instances.

    This factory provides a convenient way to create SqlManager objects with
    default configurations and dependencies which can be overwritten when necessary.

    Example:
    oracle = SqlManagerFactor.create_sql_manager(service_name='oracle', username='u0062202')
    oracle.query('select * from clarity_org.zc_state)

    overriding a default:
    oracle = SqlManagerFactor.create_sql_manager(service_name='oracle', username='u0062202' config_file='path/to/some/other/config/file')

    """

    @staticmethod
    def create_sql_manager(
        service_name: Optional[str] = None,
        username: Optional[str] = None,
        config_file: Optional[str] = None,
        credential_provider: Optional[CredentialProvider] = None,
        tns_config_loader: Optional[TNSConfigLoader] = None,
    ) -> "SqlManager":  # Forward reference for type hinting
        
        """Creates and returns an SqlManager instance."""
        config_file = config_file or r"C:\Cloud\Box\UMB_DataScience\Configs\db_config.yaml"
        credential_provider = credential_provider or KeyringCredentialProvider()
        tns_config_loader = tns_config_loader or YamlTNSConfigLoader()

        controller = DatabaseEngineController(config_file, credential_provider, tns_config_loader)
        engine = controller.get_engine(service_name, username)
        return SqlManager(engine)

class SqlManager:
    """Manages SQL database interactions using a SQLAlchemy engine.

    This class provides methods for executing SQL statements, uploading DataFrames,
    and querying the database. It encapsulates the database engine and provides
    a higher-level interface for database operations.
    """
    def __init__(self, engine: sa.engine.Engine):
        self.engine = engine

    def execute_sql(self, sql_stmt):
        """Executes a raw SQL statement against the database.

        This method uses a transaction to ensure atomicity of the SQL operation.

        Args:
            sql_stmt (str): The SQL statement to execute.

        Returns:
            bool: True if the SQL statement executed successfully, False otherwise.
                   Returns False if there was an exception during execution.

        Raises:
            SQLAlchemyError: If there is an error during database operation.
            Exception: If any other unexpected error occurs.

        Example:
            >>> db_manager = DatabaseManager(engine)
            >>> success = db_manager.execute_sql("CREATE TABLE my_table (id INT)")
            >>> if success:
            ...     print("Table created successfully")
            ... else:
            ...     print("Failed to create table")

        """
        try:
            with self.engine.begin() as connection: 
                print(f"Executing SQL: {sql_stmt}")
                connection.execute(sa.text(sql_stmt))
        except SQLAlchemyError as e:
            print(f"Error executing SQL: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        return True

    def upload_dataframe(self, dataframe, table_name, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None):
        """
        Upload a DataFrame to the database. By default, this function converts the dataframe column types to sqlalchmeny column types when uploading.
        A user can override this auto-conversion by passing their own dict of column typing where the key is the column_name and the value
        is the sqlalchemy_column_type.  

        Args:
            dataframe (pandas.DataFrame): The DataFrame to upload.
            table_name (str): The name of the table to upload the DataFrame to.
            schema (str): The schema name where you want to upload the DataFrame
            if_exists (str, optional): How to behave if the table already exists. Defaults to fail ('replace', 'append', 'fail')
            index (bool, optional): Whether to include the DataFrame index as a column. Defaults to False.
            index_label (str): What name to give the index
            chuncksize (int): If provided will execute the sql statement in chuncks of records specified
            dtype (dict, optional): Overrides the auto type detection with user-defined type mapping that is applied to the columns. Defaults to None.
            method (str): (None, 'multi', callable) Controls the SQL insertion clause used - Defaults to None (one per row) See pandas to_sql for details

        Example:
            oracle = SqlManagerFactory.create_sql_manager('oracle', 'u0062202')

            oracle.upload_df(dataframe=your_dataframe, table_name='my_table', schema='my_schema_name', if_exists='replace, index=False)

            Example without auto_dtype:
                import sqlalchemy as sa

                my_dtypes = {'int_col': sa.types.INTEGER(),
                            'str_col': sa.types.VARCHAR(length=30),
                            'bool_col': sa.types.BOOLEAN(),
                            'dt': sa.types.DATE()}

                oracle.upload_df(dataframe=your_dataframe, table_name='my_table', schema='my_schema_name', if_exists='replace, index=False, dtype=my_dtypes)

        Notes:
            For full list of acceptable types see https://docs.sqlalchemy.org/en/20/core/type_basics.html#types-sqlstandard 
            under the SQL Standard and Multiple Vendor “UPPERCASE” Types section

            The automatic conversion is based on the dataframe's datatypes. Hence, if a date field is listed as an object datatype 
            in the dataframe the auto-conversion will set it as a VARCHAR.  To rectify this, please cast your dataframe columns to 
            the desired data types prior to using this function or override the auto-conversion using the dtype argument.  
            In the example given if the auto-conversion is overridden and a date (which is an object datatype in the df) is set to 
            a sqlalchemy date then it will upload as a date.
        """
        dtypes = dtype or generate_sqlalchemy_dtypes(dataframe)
        try:
            with self.engine.begin() as connection:  
                dataframe.to_sql(name=table_name, con=connection, schema=schema, if_exists=if_exists, index=index, index_label=index_label, chunksize=chunksize, dtype=dtypes, method=method)
        except (SQLAlchemyError, ValueError) as e: 
            print(f"Error uploading DataFrame: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        return True
    
    def query(self, sql_query, sql_success_msg: bool = False):
        """Executes a SQL query and returns the result as a Pandas DataFrame.

        This method connects to the database, executes the provided SQL query,
        and returns the result as a Pandas DataFrame. It also provides an option
        to print a success message along with the query execution time.

        Args:
            sql_query (str): The SQL query to execute.
            sql_success_msg (bool, optional): If True, prints a success message
                including the query execution time. Defaults to False.

        Returns:
            pandas.DataFrame or None: A Pandas DataFrame containing the query
                results if the query was successful. Returns None if an error
                occurred during query execution or connection.

        Raises:
            Exception: If any error occurs during database interaction or 
                       time calculation.

        Example:
            >>> db_manager = DatabaseManager(engine)
            >>> df = db_manager.query("SELECT * FROM my_table")
            >>> if df is not None:
            ...     print(df.head())
            ... else:
            ...     print("Query failed")
            >>> df_with_message = db_manager.query("SELECT * FROM another_table", sql_success_msg=True)
            Query executed without error in 0d:0h:0m:0.12s. #Example output
        """
        try:
            with self.engine.connect() as connection:
                tic = time.perf_counter()
                result_df = pd.read_sql(sa.text(sql_query), con=connection)
                toc = time.perf_counter()
                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except Exception as e:
                        print(f"Problem getting elapsed time: {e}")
                return result_df
        except Exception as e:
            print(f"Error executing query: {e}") #Simplified the message
            return None
# %%
