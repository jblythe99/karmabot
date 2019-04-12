FROM python:3.6

RUN mkdir /opt/jblythe
WORKDIR /opt/jblythe

#Pull Code
RUN git clone https://github.com/jblythe99/karmabot.git

ENV SLACK_KARMA_BOTUSER=UH2R4CQEQ
ENV SLACK_KARMA_TOKEN=xoxb-455015788833-580854432500-R0uVjzKxfwuWHg7c7T7GyGxM

RUN pip install pymongo slackclient feedparser

RUN cd karmabot && pip install -r requirements.txt && sh run.sh
