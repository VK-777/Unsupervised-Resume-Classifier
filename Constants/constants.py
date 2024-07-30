LOG_FILE_PATH = "C:/#KIIT/RC2.1/Logging"
DATABASE_URL = "postgresql://postgres:1410@localhost:5432/postgres"
JOB_SKILLS_FILEPATH = "C:/#KIIT/RC2.1/job_skills.json"
JOB_TITLES_FILEPATH = "C:/#KIIT/RC2.1/job_titles.json"
API_KEYS_FILEPATH = "C:/#KIIT/RC2.1/keys.txt"
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


