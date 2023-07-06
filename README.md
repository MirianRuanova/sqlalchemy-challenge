# sqlalchemy-challenge

#### Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

## Reflect Tables into SQLAlchemy ORM

1. Create our `engine` to connect with the database file `hawaii.sqlite`. The engine is a component that povides the interface to a database. It is reponsible fot establishing and managing the connections to the database and executing SQL queries.
2. Define a Base class that will serve as the base for the generated classes representing database tables. Create an instance of it 

    ```python
    Base = automap_base()
    ```
3. Use `prepare()` method of `Base` class to reflect the schema of the existing database. Provide `engine` object as an argument. 
    ```python
    Base.prepare(engine, reflect=True)
     ```
4. To display all the classes that automap found, access the `classes` atribute of `Base` object.
    ```python
    classes = Base.classes
    classes_name = Base.classes.keys()
    print(classes_name)
     ```
    The `Base.classes` provides an dictionary-like interface that contains all the classes taht were automatically mapped. The `keys()` method is used to retrieve the names of the classes.
5. To save references to each table after reflecting the database schema using automap_base in SQLAlchemy, you can store the generated classes in variables.
    ```python
    measurement = Base.classes.measurement
    station = Base.classes.station
     ```
    The variables can be used to query and manipulate data from the respective tables.
6. To create a session in SQLAlchemy and establish a connection between Python and the database use the `Session()` class from `sqlalchemy.orm`, passing the engine as an argument. The `Session` object will serve as the entry point for all database operations.

## Exploratory Precipitation Analysis

### Find the most recent date in the data set

#### In the code below, ``func.max(measurement.date)`` is used within the ``query()`` method to find the maximum (most recent) date in the ``"date" `` column of the ``"measurement"`` table. The ``scalar()`` method is then called to retrieve the result as a single value.

### Design a query to retrieve the last 12 months of precipitation data.

## Part 2: Design Your Climate App

#### After completing the initial analysis, we will design a Flask API based on the queries that we just developed. To do so, we will use Flask to create our routes as follows:

Flask is a webframework for building web applications in Python. It provides a simple