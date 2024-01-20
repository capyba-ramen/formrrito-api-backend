FROM python:3.8.16

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev

RUN mkdir /code

ADD requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

ENV PYTHONPATH=/code

# Make /app as a working directory in the container
WORKDIR /code

# Copy requirements from host, to docker container in /app
COPY . .

ENV PORT=8000

# Expose the port 8000 in which our application runs
EXPOSE 8000

# Run the application in the port 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["./startupg.sh"]