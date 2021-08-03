from flask import Flask, render_template, request, jsonify 
from flask.wrappers import Response
from numpy.core.fromnumeric import trace
from werkzeug.utils import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2
import time
import traceback

__author__ = 'david.williware@gmail.com>'
__source__ = ''

# based on https://github.com/ricktorzynski/ocr-tesseract-docker
inContainer = os.environ.get('IN_CONTAINER', False)
if not inContainer:
  pytesseract.pytesseract.tesseract_cmd = r'c:\program files\tesseract-ocr\tesseract'
  print(pytesseract.get_languages(config=''))

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
    try:
      fmt = 'XML'; ux = False
      if 'fmt' in request.form: fmt=request.form['fmt']
      if fmt != 'TEXT': fmt = 'XML'
      if 'ux' in request.form:
         ux = request.form['ux']=='1'
      
      f = request.files['file']

      # create a secure filename
      filename = secure_filename(f.filename)

      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
      
      tmOcrTxtBeg = time.time()
      if fmt == 'TEXT':
        # perform OCR on the processed image
        text = pytesseract.image_to_string(filepath)
      else:
        hocrXml = pytesseract.image_to_pdf_or_hocr(filepath, extension='hocr')
        text= hocrXml.decode('utf-8')
      tmOcrTxtEnd = time.time()
      
      if ux:
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
        os.remove(filepath)
        tmImgEnd = time.time()
        
        totTxt = 'imgTm:'+str(tmImgEnd-tmImgBeg) + ' ocrTm:'+ str(tmOcrTxtEnd-tmOcrTxtBeg) + '\n'+text
        return render_template("uploaded.html", displaytext=totTxt, fname=ofilename)
      else:
        # remove the processed image
        os.remove(filepath)
        return jsonify({'elapsed':(tmOcrTxtEnd-tmOcrTxtBeg), 'data': text, 'error':''})
    except Exception as e:
        track = traceback.format_exc()
        return jsonify({'elapsed':0, 'data': '', 'error':repr(e), 'file':filepath, 'trace': track})

if __name__ == '__main__':
  app.run(debug=True, port=8081, host='0.0.0.0')
