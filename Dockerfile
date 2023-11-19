FROM python:3.11

RUN apt-get install -y libmagic1

WORKDIR /backend

COPY ./backend .

RUN pip install -r requirements.txt

COPY ./frontend/dist ./ui

CMD exec uvicorn main:app --host 0.0.0.0 --port 8001