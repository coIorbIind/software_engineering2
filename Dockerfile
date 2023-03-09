FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code
RUN python setup.py develop
RUM seed_db

CMD ["uvicorn", "main:get_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--factory"]