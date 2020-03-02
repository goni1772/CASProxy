FROM ubuntu:18.04
MAINTAINER goni1772
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y openjdk-8-jre-headless
WORKDIR /CASProxy
RUN git clone https://github.com/goni1772/CASProxy.git
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["CasProxy.py"]
