FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./ /app
EXPOSE 4150

RUN pip install -r ./backend/requirements.txt

CMD uvicorn backend.clubhouse.api:app --host 0.0.0.0 --port 4150