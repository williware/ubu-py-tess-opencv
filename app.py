from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2
import time

__author__ = 'david.williware@gmail.com>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      # create a secure filename
      filename = secure_filename(f.filename)

      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
      
      tmImgBeg = time.time()
      # load the example image and convert it to grayscale
      image = cv2.imread(filepath)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      
      # apply thresholding to preprocess the image
      gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

      # apply median blurring to remove any blurring
      gray = cv2.medianBlur(gray, 3)

      # save the processed image in the /static/uploads directory
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
      cv2.imwrite(ofilename, gray)
      tmImgEnd = time.time()
      
      tmOcrTxtBeg = time.time()
      # perform OCR on the processed image
      text = pytesseract.image_to_string(Image.open(ofilename))
      tmOcrTxtEnd = time.time()
      
      tmHocrTxtBeg = time.time()
      # perform OCR on the processed image
      hocrXml = pytesseract.image_to_pdf_or_hocr(ofilename, extension='hocr')
      tmHocrTxtEnd = time.time()

      # remove the processed image
      os.remove(ofilename)
      totTxt = 'imgTm:'+(tmImgEnd-tmImgBeg) + ' ocrTm:'+ (tmOcrTxtEnd-tmOcrTxtBeg) +  ' hocrTm:'+ (tmHocrTxtEnd-tmHocrTxtBeg) + '\n'+text+'\n\n'+hocrXml
      return render_template("uploaded.html", displaytext=totTxt, fname=filename)

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')