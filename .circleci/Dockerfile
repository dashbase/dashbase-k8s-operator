FROM circleci/python:3.6.2
LABEL maintainer="Pure White"
LABEL email="daniel48@126.com"
LABEL company="Dashbase"
LABEL website="www.dashbase.io"

USER root
RUN apt-get update --fix-missing && apt-get upgrade -y && apt-get clean
RUN pip install awscli
USER circleci
RUN mkdir /home/circleci/.ssh
COPY circleci.pem /home/circleci/.ssh/circleci.pem
RUN sudo curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && sudo chmod 777 ./kubectl && sudo mv ./kubectl /usr/local/bin/kubectl
RUN sudo curl -LO https://github.com/kubernetes/kops/releases/download/1.7.0/kops-linux-amd64 && sudo chmod 777 ./kops-linux-amd64 && sudo mv ./kops-linux-amd64 /usr/local/bin/kops
