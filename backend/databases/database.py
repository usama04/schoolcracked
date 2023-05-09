import sys
import sqlalchemy as sa
import sqlalchemy.orm as orm

sys.path.append("..")
import settings

db_url = settings.DATABASE_URL

engine = sa.create_engine(db_url)

SessionLocal = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)


