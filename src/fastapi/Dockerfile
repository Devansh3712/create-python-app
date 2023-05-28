FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0:0:0:0", "--port", "8000"]
