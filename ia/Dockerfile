FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat &&\
    apt-get install ffmpeg libsm6 libxext6 build-essential libpq-dev -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html
RUN pip install psycopg2-binary --no-binary psycopg2-binary

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python", "main.py"]

