#!/bin/bash

mkdir upload

cp -R skill/* upload/

poetry export -f requirements.txt > upload/requirements.txt

