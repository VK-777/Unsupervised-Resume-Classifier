import pandas as pd
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from Services.classification_service import Classify
from Daos.database import query, updater, get_db, get_candidate_by_id
from Constants.constants import CHUNK_SIZE


class ApiService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def classify_all(self):
        counter = 0

        for candidates in query(self.db):
            if not isinstance(candidates, pd.DataFrame):
                raise ValueError("Expected a DataFrame from the query generator")

            # Classify the resume
            result = Classify.classify_resume(candidates)

            updater(result)

            print(f"Successfully updated Chunk {counter}")
            counter += 1

    def classify_by_id(self, candidate_id):
        # Fetch the candidate from the database
        candidate_df = get_candidate_by_id(self.db, candidate_id)

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
        return formatted_result
