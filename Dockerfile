FROM python:3.12

WORKDIR /usr

COPY requirements.txt /usr

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/api

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]