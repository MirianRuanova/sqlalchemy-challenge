# Import the dependencies.
from sqlalchemy import create_engine
#from sqlalchemy import Column, Integer, String, Float

#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()

# Path to sqlite

database_path = "../Resources/hawaii.sqlite"

# Create an engine that can talk to the database
engine = create_engine(f"sqlite:///{database_path}")
# Query All Records in the the Database
data = engine.execute("SELECT * FROM hawaii")

for record in data:
    print(record)

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
