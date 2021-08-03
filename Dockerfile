FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=US/Eastern
ENV IN_CONTAINER=1
LABEL AUTHOR="david.williware@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get update --fix-missing && apt-get install -y python3-opencv
RUN apt-get -y install tesseract-ocr
COPY . /app
WORKDIR /app
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pillow
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pytesseract
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org opencv-python
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org opencv-contrib-python
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org flask-uploads
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
