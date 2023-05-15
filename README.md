# SchoolCracked - AI Teaching Assistant

SchoolCracked is an innovative AI teaching assistant designed to enhance the teaching and learning experience for both teachers and students. This project has been built with Django as AuthBackend, FastAPI Microservice as Chatbot backend, ReactJS frontend and uses PostgreSQL database. The logic of the chatbot has been developed using Langchain and ChatOpenAI LLM.

## Features

- Real-time information: SchoolCracked can provide real-time information, solve complex mathematical problems, write code, conduct research on the internet, and read and understand documents to provide relevant information.
- Course creation: SchoolCracked can assist in creating course outlines, assignments, quizzes, and even question papers.
- Answer questions: Students can ask any question and receive guidance towards the answer, rather than just receiving the answer directly.
- Critical thinking skills: This approach aligns with the principles of effective teaching, as it helps students develop critical thinking skills and problem-solving abilities.

## Requirements

- Python 3.7 or higher
- PostgreSQL 12 or higher

## Installation

1. Clone the repository
2. Install the requirements for AuthBackend by running `pip install -r requirements.txt`
3. Install the requirements for the backend by running `pip install -r backend/requirements.txt`
4. Create a PostgreSQL database
5. Set up the database by running `python manage.py migrate` from AuthBackend folder
6. Start the AuthBackend server by running `python manage.py runserver`
7. Start the backend server by running `uvicorn backend.main:app --reload` from backend folder
8. Start the frontend server by running `npm start` from frontend folder

Note: AuthBackend and backend need to run in different Python environments.

## Docker

Dockerized versions of the application will be coming soon.

## Contributors

- Usama Arshad - https://github.com/usama04