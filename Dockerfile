FROM python:3.6

RUN mkdir /opt/jblythe
WORKDIR /opt/jblythe

#Pull Code
RUN git clone https://github.com/jblythe99/karmabot.git

ENV SLACK_KARMA_BOTUSER=UH2R4CQEQ
ENV SLACK_KARMA_TOKEN=xoxp-455015788833-455451203892-594652601923-624a8a73796a6fc1fad32813af4ea638

RUN pip install pymongo slackclient feedparser

ENTRYPOINT cd karmabot && pip install -r requirements.txt && sh run.sh
