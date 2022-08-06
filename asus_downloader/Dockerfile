FROM python:3.9.7
WORKDIR /asus
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
CMD ["python3", "downloader.py"]
