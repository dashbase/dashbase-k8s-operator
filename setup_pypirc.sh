#!/bin/bash

# build package and upload to private pypi index
echo "[distutils]" >> ~/.pypirc
echo "index-servers = pypi" >> ~/.pypirc
echo "[pypi]" >> ~/.pypirc
echo "repository=https://$PYPI_HOST" >> ~/.pypirc
echo "username=$PYPI_USERNAME" >> ~/.pypirc
echo "password=$PYPI_PASSWORD" >> ~/.pypirc
