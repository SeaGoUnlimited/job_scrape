FROM python:3

ADD gov_job_basic_bs4.py /
COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

CMD [ “python”, "./gov_job_basic_bs4.py” ]

