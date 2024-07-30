LOG_FILE_PATH = "Logging"
DATABASE_URL = "postgresql_database_link_here"
JOB_SKILLS_FILEPATH = "job_skills.json/file/path"
JOB_TITLES_FILEPATH = "job_titles.json/file/path"
API_KEYS_FILEPATH = "keys.txt/file/path"
CHUNK_SIZE = 100
GET_BY_ID = "SELECT * FROM public.candidate_details WHERE id = :cid"
GET_ALL = "SELECT * FROM public.candidate_details ORDER BY id LIMIT :limit OFFSET :offset"
UPDATE = "UPDATE public.candidate_details SET classification = :new_value WHERE id = :candidate_id"
REGEX_PATTERNS = [
            r'\b(?:[a-z]+\s){0,2}(?:engineer|developer|lead|manager|administrator|consultant|technician|scientist'
            r'|analyst|coordinator|director|specialist|officer|architect|strategist|executive|advisor|designer'
            r'|programmer|supervisor|trainer|planner|controller|assistant|operator|agent|representative|clerk'
            r'|inspector|instructor|apps developer|attendant)\b',
        ]


