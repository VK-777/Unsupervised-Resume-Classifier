from Services.api_service import ApiService
from fastapi import APIRouter, FastAPI
from Logging.logger import custom_logger
import asyncio

app = FastAPI()
router = APIRouter()
custom_logger = custom_logger.get_instance("custom_logfile.log", max_file_size=500000, backup_count=3)

# Event to signal when classification is done
classification_done_event = asyncio.Event()
classification_done_event.set()  # Initially set to True

# Global variable to manage server shutdown
shutdown_event = asyncio.Event()
api = ApiService()


@router.get("/classify")
def classify_endpoint():
    classification_done_event.clear()  # Clear the event at the start of classification

    api.classify_all()

    # Signal that classification is done
    classification_done_event.set()

    return {"message": "Job done"}


@router.get("/classify_candidate/{candidate_id}")
def classify_candidate(candidate_id: int):
    classification_done_event.clear()
    formatted_result = api.classify_by_id(candidate_id)
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
