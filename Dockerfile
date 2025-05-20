FROM python:3
LABEL authors="pinheadtf2"

CMD [ "python", "-m pip install --upgrade pip" ]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]