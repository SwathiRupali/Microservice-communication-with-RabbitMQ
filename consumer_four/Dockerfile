FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY read.py .
CMD [ "python", "read.py" ]
