# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /usr/src/app

# install python dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

# install poppler for pdf2img
# RUN apt-get install python-poppler

# RUN apt-get install c++
# RUN which cmake
# RUN /usr/bin/c++

# RUN apt-get update && apt-get -y install cmake
# RUN apt-get update
# RUN apt-get -y install gcc
# RUN which gcc
# RUN export CMAKE_CXX_COMPILER=/usr/bin/gcc
# RUN export CXX=/usr/bin/gcc
# RUN pip install python-poppler

# RUN apt-get install g++
# add app
COPY . .
