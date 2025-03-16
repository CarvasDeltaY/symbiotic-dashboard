import sys
import os
from sqlalchemy import inspect

########### Setting working directory for acessing packages  ############
try:
    script_dir = os.path.abspath(os.path.dirname(__file__))
except NameError:
    script_dir = os.getcwd()  # Fallback for environments without __file__
    print("Warning: __file__ not found. Using current working directory instead.")

# Assuming your project root is the parent directory of the current script:
project_root = os.path.abspath(os.path.join(script_dir, "."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("Current sys.path:", sys.path)  # Debug: check if project_root is included

from external.aws_rds.db import Base, engine, SessionLocal
from external.aws_rds.database_models import StakingData  # Ensure models are imported before create_all



# Now SQLAlchemy knows about the User model
Base.metadata.create_all(engine)

# Drop all tables
#Base.metadata.drop_all(engine)

# Get all table names

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:", tables)