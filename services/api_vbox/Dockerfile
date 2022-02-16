FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY main.py /app/

CMD ["python","-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
