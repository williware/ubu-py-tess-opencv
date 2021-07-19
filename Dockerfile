FROM ubuntu:latest
LABEL AUTHOR="david.williware@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get update --fix-missing && apt-get install -y python3-opencv
RUN apt-get -y install tesseract-ocr
COPY . /app
WORKDIR /app
RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-python
RUN pip install opencv-contrib-python
RUN pip install flask-uploads
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]