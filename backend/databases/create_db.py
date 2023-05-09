import database as db
import models as m

def create_db() -> None:
    m.Base.metadata.create_all(bind=db.engine)
    
if __name__ == "__main__":
    create_db()