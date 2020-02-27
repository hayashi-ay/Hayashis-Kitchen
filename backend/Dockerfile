FROM python:3.8.2-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# for production
# CMD [ "gunicorn", "-b", ":8080", "app:app" ]

# for development
CMD [ "python", "app.py" ]
