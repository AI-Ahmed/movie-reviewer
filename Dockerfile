FROM nvidia/cuda:11.0-cudnn8-runtime-ubuntu18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /movie_reviewer
COPY . .

# Install software dependencies
RUN apt-get update && apt-get install software-properties-common -y

## Fix the proxy issue for new Ubuntu images
RUN apt-get install --reinstall ca-certificates

## Install python Ubuntu packages
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y \
    cmake \
    unzip \
    curl \
    git \
    libpoppler-cpp-dev \
    libtesseract-dev \
    pkg-config \
    poppler-utils \
    python3-pip \
    python3.7 \
    python3.7-dev \
    python3.7-distutils \
    default-libmysqlclient-dev \
    build-essential \
    swig \
    tesseract-ocr \
    wget && \
rm -rf /var/lib/apt/lists/*


# Set default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && \
    update-alternatives --set python3 /usr/bin/python3.7


# Install PyTorch for CUDA 11
RUN pip3 install torch==1.10.2+cu111 -f https://download.pytorch.org/whl/torch_stable.html

# Install package
RUN apt-get install -y poppler-utils
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m pip install cffi

# Run Required models to be cached --> Translator & Sentiment Analysis models
RUN python3 -c "from haystack.nodes import TransformersTranslator, TransformersDocumentClassifier;TransformersTranslator(model_name_or_path='Helsinki-NLP/opus-mt-de-en');TransformersTranslator(model_name_or_path='Helsinki-NLP/opus-mt-fr-en');TransformersDocumentClassifier(model_name_or_path='valhalla/distilbart-mnli-12-3', task ='zero-shot-classification', labels=['good', 'neutral', 'bad'])"


EXPOSE 80
ENV HAYSTACK_DOCKER_CONTAINER="HAYSTACK_GPU_CONTAINER"

ENTRYPOINT ["python3", "./main.py"]
