# Docker file for pfdcm_tagextract ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-pfdcm_tagextract .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-pfdcm_tagextract .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-pfdcm_tagextract
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-pfdcm_tagextract
#

FROM fnndsc/python:3.8.5-ubuntu20.04
LABEL maintainer="Mohit Chandarana <chandarana.m@northeastern.edu>"

RUN apt-get update

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["pfdcm_tagextract", "--help"]
