from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from Constants.constants import DATABASE_URL, CHUNK_SIZE,GET_BY_ID, GET_ALL, UPDATE
import pandas as pd

# Create the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get a database session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_candidate_by_id(db: Session, candidate_id: int):
    q = text(GET_BY_ID)
    with engine.connect() as connection:
        df = pd.read_sql(q, connection, params={"cid": candidate_id})
        return df


def query(db: Session = Depends(get_db)):
    chunk_size = CHUNK_SIZE
    # SQL query to fetch all rows from the table
    offset = 0
    with engine.connect() as connection:
        while True:
            # Execute the query
            q = text(GET_ALL)
            df = pd.read_sql(q, connection, params={"limit": chunk_size, "offset": offset})

            if df.empty:
                break
            df = df.reset_index(drop=True)

            yield df
            offset += CHUNK_SIZE


def update(session: Session, df):
    for _, row in df.iterrows():
        q = text(UPDATE)
        session.execute(q, {'new_value': row['classification'], 'candidate_id': row['id']})
    session.commit()  # Commit changes
