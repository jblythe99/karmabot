FROM python:3.6

RUN mkdir /opt/jblythe
WORKDIR /opt/jblythe

#Pull Code
RUN git clone https://github.com/jblythe99/karmabot.git

ENV SLACK_KARMA_BOTUSER=${SLACK_KARMA_BOTUSER}
ENV SLACK_KARMA_TOKEN=${SLACK_KARMA_TOKEN}

RUN pip install pymongo slackclient feedparser

ENTRYPOINT cd karmabot && pip install -r requirements.txt && sh run.sh
