# Unsupervised Resume Classifier

## Overview
The Unsupervised Resume Classifier is a project that classifies and extracts job titles from candidate resumes. It processes skill sets to match candidates with job roles effectively. The project utilizes machine learning, natural language processing, and clustering techniques to enhance resume classification and job matching.

## Features
- Resume Classification: Classifies resumes based on job titles and skill sets.
- Regex Identification: Identifies certain patterns to extract job roles. 
- Skill Matching: Matches candidate skills with predefined job roles.
- LLM Application: Prompts gemini api to label unclassified candidates.
- Customizable: Allows integration of new job roles and skills through configuration files.

## Project Structure
- Constants/ : Contains configuration constants and settings.
- Controller/ : Manages API endpoints and application logic.
- Daos/ : Handles database interactions and data access.
- Logging/ : Provides logging functionalities.
- Services/ : Implements core classification and filtering services.
- Utils/ : Contains utility functions for data and text processing.

## Installation

1. **Clone the Repository**:
  ```sh
  git clone https://github.com/VK-777/Unsupervised-Resume-Classifier.git
  cd Unsupervised-Resume-Classifier
  ```
2. **Set Up the Environment**:
  - Ensure you have Python 3.11 or higher installed.
  - Install required packages:
  ```sh
  pip install -r requirements.txt
  ```
3. **Configuration**:
  - Update configuration files in the Constants/ directory as needed.

## Usage

1. **Run the Application**:
  ```sh
  python main.py
  ```
2. **API Endpoints**:
  - GET/classify: Classify resumes and match with job roles.
  - GET/classify_candidate/{id}: Classifies particular candidate whose id is mentioned.
  - GET/shutdown: Shutdowns the server gracefully after all tasks have been successfully executed.

3. **Database**:
  - Ensure PostgreSQL is running and configured as specified in Constants/constants.py.
  - The application reads from and writes to the database.

## Example
To classify a resume, send a GET request to the /classify endpoint with the resume data. The API will update your database with the classification results based on the provided job roles and skills.

## Project Files
  - job_skills.json: Contains job titles and required skills.
  - job_titles.json: List of job titles for classification.
  - main.py: Main script to run the application.
  - requirements.txt: Lists required Python packages.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
  - Machine Learning Libraries: Utilized various libraries for machine learning and text processing.
  - Open Source Tools: Leveraged open-source tools and libraries for project development.

## Contact
For any questions or feedback, please contact kvedant6@gmail.com.








#### -- READ Configuration.md FOR FURTHER ASSISSTANCE TO RUN THE CODE --


