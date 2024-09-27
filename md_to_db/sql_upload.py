import pandas as pd
from sqlalchemy import (
    create_engine, Table, Column, Integer, String, Boolean, Text,
    MetaData, ForeignKey, select
)
from sqlalchemy.dialects.postgresql import insert  # PostgreSQL-specific insert
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
import sys
from dotenv import load_dotenv
import logging
import traceback

# =======================
# 1. Configure Logging
# =======================

logging.basicConfig(
    filename='import_log.log',  
    level=logging.INFO,          
    format='%(asctime)s %(levelname)s:%(message)s') 

# =======================
# 2. Load Environment Variables
# =======================

load_dotenv()

# =======================
# 3. Configuration
# =======================

CSV_FILE_PATH = 'techniques_data.csv'  
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
POSTGRES_HOST = os.getenv('DB_HOST', 'localhost')  
POSTGRES_PORT = os.getenv('DB_PORT', '5432')
POSTGRES_DB = os.getenv('DB_NAME')

# =======================
# 4. Database Engine
# =======================

def get_postgres_engine():
    """Create a SQLAlchemy engine for PostgreSQL."""
    connection_string = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    engine = create_engine(connection_string, echo=False)  # Set echo=True for detailed SQL logs
    return engine

def create_tables(engine, metadata):
    """Create tables in PostgreSQL based on the normalized schema."""
    categories = Table('categories', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(255), unique=True, nullable=False)
    )

    sub_categories = Table('sub_categories', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(255), unique=True, nullable=False)
    )

    tags = Table('tags', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(255), unique=True, nullable=False)
    )

    techniques = Table('techniques', metadata,
        Column('id', Integer, primary_key=True),
        Column('technique', String(255), unique=True, nullable=False),  
        Column('description', Text),
        Column('scope_global', Boolean),
        Column('scope_local', Boolean),
        Column('model_dependency', String(50)),
        Column('example_use_case', Text)
    )

    technique_categories = Table('technique_categories', metadata,
        Column('technique_id', Integer, ForeignKey('techniques.id', ondelete='CASCADE'), primary_key=True),
        Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
    )

    technique_tags = Table('technique_tags', metadata,
        Column('technique_id', Integer, ForeignKey('techniques.id', ondelete='CASCADE'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    )

    sub_techniques = Table('sub_techniques', metadata,
        Column('technique_id', Integer, ForeignKey('techniques.id', ondelete='CASCADE'), primary_key=True),
        Column('sub_category_id', Integer, ForeignKey('sub_categories.id', ondelete='CASCADE'), primary_key=True)
    )

    metadata.create_all(engine)
    logging.info("All tables created successfully.")
    print("All tables created successfully.")

def insert_unique_entry(session, table, name):
    """
    Insert a unique entry into a table.
    If the entry exists, return its ID.
    Otherwise, insert it and return the new ID.
    """
    # Construct a select statement
    stmt = select(table.c.id).where(table.c.name == name)
    result = session.execute(stmt).scalar_one_or_none()
    
    if result:
        return result
    else:
        # Use upsert to prevent duplicates by specifying index_elements as a tuple
        stmt = insert(table).values(name=name).on_conflict_do_nothing(
            index_elements=(table.c.name,)
        ).returning(table.c.id)
        result = session.execute(stmt)
        inserted_id = result.scalar_one_or_none()
        session.commit()
        if inserted_id:
            return inserted_id
        else:
            # If the insert did nothing because of a conflict, fetch the existing id
            stmt = select(table.c.id).where(table.c.name == name)
            result = session.execute(stmt).scalar_one()
            return result

def import_csv_to_postgres(csv_path: str, engine, metadata):
    """Import CSV data into PostgreSQL with normalized tables."""
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read CSV
    try:
        df = pd.read_csv(csv_path)
        logging.info(f"CSV file '{csv_path}' read successfully. Shape: {df.shape}")
        print(f"CSV file '{csv_path}' read successfully. Shape: {df.shape}")
    except Exception as e:
        logging.error(f"Error reading CSV file '{csv_path}': {e}")
        logging.error(traceback.format_exc())  # Log the full stack trace
        print(f"Error reading CSV file '{csv_path}': {e}")
        sys.exit(1)  # Exit since the CSV couldn't be read

    # Reflect tables
    metadata.reflect(bind=engine)

    # Access tables from metadata
    categories_table = metadata.tables.get('categories')
    sub_categories_table = metadata.tables.get('sub_categories')
    tags_table = metadata.tables.get('tags')
    techniques_table = metadata.tables.get('techniques')
    technique_categories_table = metadata.tables.get('technique_categories')
    technique_tags_table = metadata.tables.get('technique_tags')
    sub_techniques_table = metadata.tables.get('sub_techniques')

    # Explicitly check for missing tables
    required_tables = {
        'categories': categories_table,
        'sub_categories': sub_categories_table,
        'tags': tags_table,
        'techniques': techniques_table,
        'technique_categories': technique_categories_table,
        'technique_tags': technique_tags_table,
        'sub_techniques': sub_techniques_table
    }

    missing_tables = [name for name, table in required_tables.items() if table is None]

    if missing_tables:
        logging.error(f"Missing tables after reflection: {missing_tables}")
        print(f"Error: Missing tables after reflection: {missing_tables}")
        session.close()
        sys.exit(1)

    # Optional: Log successful reflections
    for name, table in required_tables.items():
        logging.info(f"Table '{name}' successfully reflected.")

    for index, row in df.iterrows():
        logging.info(f"Processing row {index + 1}: {row['Technique']}")
        try:
            # Insert into techniques
            technique_data = {
                'technique': row['Technique'],
                'description': row['Description'],
                'scope_global': True if str(row['Scope Global']).strip().lower() == 'yes' else False,
                'scope_local': True if str(row['Scope Local']).strip().lower() == 'yes' else False,
                'model_dependency': row['Model-Dependency'],
                'example_use_case': row['Example Use-Case']
            }
            
            # Corrected insert technique with tuple in index_elements
            stmt = insert(techniques_table).values(**technique_data)\
                .on_conflict_do_nothing(index_elements=(techniques_table.c.technique,))\
                .returning(techniques_table.c.id)
            result = session.execute(stmt)
            technique_id = result.scalar_one_or_none()
            
            if technique_id is None:
                # Technique already exists, fetch its id
                stmt = select(techniques_table.c.id).where(techniques_table.c.technique == row['Technique'])
                technique_id = session.execute(stmt).scalar_one()
            else:
                session.commit()
            
            # Handle Categories
            categories = str(row['Categories']).split(';')
            for category in categories:
                category = category.strip()
                if category:
                    category_id = insert_unique_entry(session, categories_table, category)
                    # Insert into technique_categories with tuple in index_elements
                    stmt = insert(technique_categories_table).values(technique_id=technique_id, category_id=category_id)\
                        .on_conflict_do_nothing(index_elements=(technique_categories_table.c.technique_id, technique_categories_table.c.category_id))
                    session.execute(stmt)
            session.commit()

            # Handle Sub-Categories
            sub_categories = str(row['Sub-Categories']).split(';')
            for sub_category in sub_categories:
                sub_category = sub_category.strip()
                if sub_category:
                    sub_category_id = insert_unique_entry(session, sub_categories_table, sub_category)
                    # Insert into sub_techniques with tuple in index_elements
                    stmt = insert(sub_techniques_table).values(technique_id=technique_id, sub_category_id=sub_category_id)\
                        .on_conflict_do_nothing(index_elements=(sub_techniques_table.c.technique_id, sub_techniques_table.c.sub_category_id))
                    session.execute(stmt)
            session.commit()

            # Handle Tags
            tags = str(row['Tags']).split(';')
            for tag in tags:
                tag = tag.strip()
                if tag:
                    tag_id = insert_unique_entry(session, tags_table, tag)
                    # Insert into technique_tags with tuple in index_elements
                    stmt = insert(technique_tags_table).values(technique_id=technique_id, tag_id=tag_id)\
                        .on_conflict_do_nothing(index_elements=(technique_tags_table.c.technique_id, technique_tags_table.c.tag_id))
                    session.execute(stmt)
            session.commit()

        except Exception as e:
            logging.error(f"Error processing row {index + 1}: {e}")
            logging.error(traceback.format_exc())  # Log the full stack trace
            print(f"Error processing row {index + 1}: {e}")
            session.rollback()

    session.close()
    logging.info("Data imported successfully.")
    print("Data imported successfully.")

def main():
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE_PATH):
        logging.error(f"CSV file '{CSV_FILE_PATH}' does not exist.")
        print(f"Error: CSV file '{CSV_FILE_PATH}' does not exist.")
        sys.exit(1)

    # Create database engine
    engine = get_postgres_engine()

    # Create a single MetaData instance
    metadata = MetaData()

    # Create tables
    create_tables(engine, metadata)

    # Import data
    try:
        import_csv_to_postgres(CSV_FILE_PATH, engine, metadata)
    except Exception as e:
        logging.error(f"An error occurred during import: {e}")
        logging.error(traceback.format_exc())  # Log the full stack trace
        print(f"An error occurred during import: {e}")
    finally:
        engine.dispose()

if __name__ == '__main__':
    main()
