FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
