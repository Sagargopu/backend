import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# Use GCP Cloud SQL
from google.cloud.sql.connector import Connector
import pg8000

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL based on environment"""
    
    # Use Cloud SQL for all environments
    return get_cloud_sql_url()

# TODO: Uncomment when ready to connect to GCP
def get_cloud_sql_url():
    """Configure Cloud SQL connection with Application Default Credentials"""
    
    # GCP Cloud SQL configuration
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "construction-management-475118:us-east4:databasecm")  # project:region:instance
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME", "construction_management")
    
    if not INSTANCE_CONNECTION_NAME or not DB_PASS:
        raise ValueError("Missing required GCP Cloud SQL environment variables")
    
    # Create connector instance with Application Default Credentials
    # This will use the compute engine's service account automatically
    connector = Connector()
    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            enable_iam_auth=False  # Use password auth instead of IAM
        )
        return conn
    # Create SQLAlchemy engine with Cloud SQL connector
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=-1,
        pool_pre_ping=True,
    )
    return engine

DATABASE_URL = get_database_url()
if isinstance(DATABASE_URL, str):
    # SQLite fallback (should not be used)
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Cloud SQL engine (already configured)
    engine = DATABASE_URL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
