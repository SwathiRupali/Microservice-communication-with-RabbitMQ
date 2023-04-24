FROM python
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY producer.py .
CMD ["python3", "producer.py"]
