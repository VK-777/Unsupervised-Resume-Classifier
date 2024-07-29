import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from Daos.database import get_db, query, update, get_candidate_by_id
from Services.classification_service import Classify
from Logging.logger import custom_logger
from Constants.constants import CHUNK_SIZE
import asyncio

app = FastAPI()
router = APIRouter()
custom_logger = custom_logger.get_instance("custom_logfile.log", max_file_size=500000, backup_count=3)

# Event to signal when classification is done
classification_done_event = asyncio.Event()
classification_done_event.set()  # Initially set to True

# Global variable to manage server shutdown
shutdown_event = asyncio.Event()


@router.get("/classify")
def classify_endpoint(db: Session = Depends(get_db)):
    classification_done_event.clear()  # Clear the event at the start of classification
    counter = 0

    for candidates in query(db):
        if not isinstance(candidates, pd.DataFrame):
            raise ValueError("Expected a DataFrame from the query generator")

        # Classify the resume
        result = Classify.classify_resume(candidates)

        update(db, result)

        print(f"Successfully updated {counter}-{counter + CHUNK_SIZE}")
        counter += CHUNK_SIZE

    # Signal that classification is done
    classification_done_event.set()

    return {"message": "Job done"}


@router.get("/classify_candidate/{candidate_id}")
def classify_candidate(candidate_id: int, db: Session = Depends(get_db)):
    classification_done_event.clear()
    # Fetch the candidate from the database
    candidate_df = get_candidate_by_id(db, candidate_id)

    if candidate_df.empty:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Classify the candidate
    result_df = Classify.classify_resume(candidate_df)

    result_json = result_df[['id', 'candidate_name', 'classification']].to_dict(orient='records')

    # Format the result string
    formatted_result = {
        "id": result_json[0]['id'] if result_json else "N/A",
        "candidate_name": result_json[0]['candidate_name'] if result_json else "N/A",
        "classification": result_json[0]['classification'] if result_json else "N/A"
    }

    # print(f"Classification Result:\n{formatted_result}")

    classification_done_event.set()

    return {"message": "Classification completed", "result": formatted_result}


@router.get("/shutdown")
def shutdown_endpoint():
    # Set the shutdown event
    shutdown_event.set()
    return {"message": "Server is shutting down..."}


@app.on_event("startup")
async def startup():
    print("Server is starting...")


@app.on_event("shutdown")
async def on_shutdown():
    print("Shutting down gracefully...")
    # Perform any cleanup tasks here if needed

app.include_router(router)
