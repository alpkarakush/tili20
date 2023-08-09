FROM python:3.8

WORKDIR /app
COPY . /app
# How you install your python packages may differ
RUN python -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Ensure the path here is correct
ENV FLASK_APP /app/app.py
ENV TEMPLATES_AUTO_RELOAD True

RUN apt-get update && apt-get install -y iputils-ping

EXPOSE 8080
EXPOSE 5000

RUN export FLASK_ENV=development

# CMD [ "flask", "run", "--host=0.0.0.0" ]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]