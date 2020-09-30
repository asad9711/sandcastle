FROM python:2.7-alpine
WORKDIR /root
RUN apk add --no-cache --virtual .depends git
RUN git clone https://github.com/0xSearches/sandcastle.git
RUN apk del .depends
RUN pip install requests
WORKDIR /root/sandcastle
ENTRYPOINT ["./sandcastle.py"]
CMD ["--help"]
