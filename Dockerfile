FROM python

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "chainlit","run","app.py" ]

