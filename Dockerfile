FROM python

ADD ./ .

RUN pip install streamlink requests

EXPOSE 30014

CMD [ "bash", "autorun.sh" ]