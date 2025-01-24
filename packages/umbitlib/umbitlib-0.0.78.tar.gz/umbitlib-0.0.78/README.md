# Umbitlib

This is a library containing commonly used functions and constants so that they can be centrally hosted, sourced, tested, and managed

Functions being added to the library should
- Include a clear description of the function's purpose 
- Include parameter definitions for easy access in the tooltip 
- Include descriptive comments and formatting to aid in reading the code
- Include specific unit tests for the function in the corresponding tests file
- Follow DRY (Don't Repeat Yourself) coding practices where possible
- Include input cleaning and/or explicit parameter-typing  to prevent end-users from entering incorrect values

For an example submission including tests see the 'add()' function in umbitlib/helpers.py and tests/test_helpers.py

# db_connections.py

This module provides classes and protocols for managing database connections, credential retrieval, TNS configuration loading, and SQL execution. It offers a streamlined way to interact with Oracle and PostgreSQL databases, including managing credentials and configurations.

## Table of Contents
- [Overview](#overview)
- [Classes and Protocols](#classes-and-protocols)
  - [Credential Management](#credential-management)
  - [TNS Configuration](#tns-configuration)
  - [Database Engine Factory](#database-engine-factory)
  - [SQL Management](#sql-management)
- [Examples](#examples)
  - [Create and Execute SQL](#create-and-execute-sql)
  - [Upload DataFrame to a Database](#upload-dataframe-to-a-database)

---

## Overview

The `db_connections.py` module is designed to:
- Retrieve credentials securely using keyring.
- Load TNS (Transparent Network Substrate) configurations from YAML files.
- Create SQLAlchemy engine instances for Oracle and PostgreSQL databases.
- Execute SQL queries and manage database interactions with ease.

---

## Classes and Protocols

### Credential Management

#### `CredentialProvider` (Protocol)
Defines the interface for retrieving credentials for a service and username.

- **Method**: `get_credentials(service_name: str, username: Optional[str]) -> Dict[str, str]`

#### `KeyringCredentialProvider`
Implements the `CredentialProvider` protocol using the `keyring` library to securely retrieve credentials.

- **Method**: 
  - `get_credentials(service_name: str, username: Optional[str] = None) -> Dict[str, str>`
- **Raises**: `ValueError` if credentials are not found.

---

### TNS Configuration

#### `TNSConfigLoader` (Protocol)
Defines the interface for retrieving TNS addresses from a configuration file.

- **Method**: `load_tns_address(config_file: str, entry_name: str, address_name: str) -> Dict`

#### `YamlTNSConfigLoader`
Loads TNS configurations from a YAML file. 

- **Method**:
  - `load_tns_address(config_file: str, entry_name: str, address_name: str) -> Dict`
- **Raises**: `TNSConfigError` for invalid configurations, missing entries, or addresses.

---

### Database Engine Factory

#### `DatabaseEngineFactory` (Protocol)
Defines the interface for creating SQLAlchemy engines for a database.

- **Method**: `create_engine(db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine`

#### `OracleEngineFactory`
Creates Oracle database engines.

- **Method**: 
  - `create_engine(db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine`

#### `PostgresEngineFactory`
Creates PostgreSQL database engines.

- **Method**:
  - `create_engine(db_name: str, tns: Dict, username: str, password: str) -> sa.engine.Engine`
- **Raises**: `KeyError` if required TNS information is missing.

---

### Database Engine Controller

#### `DatabaseEngineController`
Manages the retrieval of credentials, TNS configurations, and creation of database engines.

- **Constructor**: 
  - `DatabaseEngineController(config_file: str, credential_provider: CredentialProvider, tns_config_loader: TNSConfigLoader)`
- **Method**:
  - `get_engine(service_name: str, username: Optional[str] = None) -> sa.engine.Engine`

---

### SQL Management

#### `SqlManager`
Provides high-level methods for interacting with SQL databases.

- **Constructor**: 
  - `SqlManager(engine: sa.engine.Engine)`
- **Methods**:
  - `execute_sql(sql_stmt: str) -> bool`
  - `upload_dataframe(dataframe, table_name, schema=None, if_exists='fail', ...) -> bool`
  - `query(sql_query: str, sql_success_msg: bool = False) -> pd.DataFrame`

#### `SqlManagerFactory`
Factory for creating pre-configured `SqlManager` instances.

- **Method**:
  - `create_sql_manager(service_name: str, username: Optional[str] = None, ...) -> SqlManager`

---

## Examples

### Create and Execute SQL

```python
from db_connections import SqlManagerFactory

# Create an SqlManager instance
sql_manager = SqlManagerFactory.create_sql_manager(service_name='oracle', username='u0062202')

# Execute a SQL query
result = sql_manager.query("SELECT * FROM my_table")
if result is not None:
    print(result.head())

# Run raw sql
sql_manager.execute_sql("truncate table my_schema.my_table")