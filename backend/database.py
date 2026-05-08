import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

# Database URL is loaded from the environment for deployment stability.
# For MySQL, use: mysql+pymysql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is required.\n"
        "Example: mysql+pymysql://user:password@localhost:3306/ramnagari_tourism"
    )

engine = create_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "false").lower() == "true", pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
