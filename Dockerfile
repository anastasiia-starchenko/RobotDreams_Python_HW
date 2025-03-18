FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=myapp.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]