FROM python:3.9-slim

RUN pip install --upgrade pip setuptools

WORKDIR /src

COPY . /src

RUN ls /src

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
