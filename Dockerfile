FROM python:3.11.1

WORKDIR /stident_bot

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]