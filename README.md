# dashbase-operator

This tool is currently a wrapper of [kops](https://github.com/kubernetes/kops), which allows user to create multiple kubernetes clusters in one vpc even in one subnet.

It's aim is to make user able to create a cluster like [stackpoint](https://stackpoint.io/). User only needs to do some simple selections and then can get a running cluster.

## Install

`pip install dashops`

## Preparation

First, you need to install [aws-cli](https://github.com/aws/aws-cli)

```
pip install awscli

# on mac
brew install mawscli
```

Second, you need to install [kops](https://github.com/kubernetes/kops), and configure your aws credientials, set up your aim and export key and secret to env according to the [kops document](https://github.com/kubernetes/kops/blob/master/docs/aws.md):

```
aws configure
export AWS_ACCESS_KEY_ID=<access key>
export AWS_SECRET_ACCESS_KEY=<secret key>
```

Thirdly, you need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in order to control your cluster.

## Usage

To be done...