#!/bin/bash

mkdir -p .ask

rsync -av --exclude '*__pycache__*' lambda .ask/

poetry export --without-hashes -f requirements.txt > .ask/lambda/requirements.txt

cd .ask && zip -r lambda_code.zip lambda
