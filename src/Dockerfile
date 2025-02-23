FROM python:3

WORKDIR /usr/src/app

ENV TZ="America/New_York"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./update.py" ]
