# sqbooster

A lightweight Python library providing a simple key-value store using SQLite.

## Description

`sqbooster` offers an easy way to store and retrieve key-value pairs using an SQLite database as the backend.  This is ideal for small projects or situations where you need a persistent key-value store without the complexity of larger database solutions.

## Features

- **Simple API:** Easily read, write, and manage key-value pairs.
- **JSON Serialization:** Values are automatically serialized and deserialized to/from JSON, allowing you to store complex data structures.
- **SQLite Backend:** Leverages the reliability and portability of SQLite.
- **Lightweight:** Minimal dependencies, perfect for single-file projects.

## Getting Started
```python
import sqbooster

database = sqbooster.db("database.db")
# creates an object from your database (if not in path, creates one)

database.write_key("salam",2)
# creates a table in your database and commits that

database.read_key("salam","default-value")
# returns table's value

database.write_database()
# gets a dictionary , puts it in the database as table (keys) and values

database.read_database()
# returns a dictionary of all the tables in your database

database.keys()
# returns a list of all the keys in your database
```

## Installation

```bash
pip install sqbooster