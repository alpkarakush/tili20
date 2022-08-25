FROM python:3.8

WORKDIR /app
COPY . /app
# How you install your python packages may differ
RUN pip3 install -r /app/requirements.txt

# Ensure the path here is correct
ENV FLASK_APP /app/app.py

RUN apt-get update && apt-get install -y iputils-ping

EXPOSE 8080
EXPOSE 5000

# CMD [ "flask", "run", "--host=0.0.0.0" ]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]