import os
import cloudinary.api
import cloudinary.uploader
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import requests

from io import BytesIO



import cloudinary

import engine
from PIL import Image

cloudinary.config(
    cloud_name="prappo",
    api_key="744967435881411",
    api_secret="_ZchlXAL7egeenAb_XPv52-a4p8",
)

# Check if ckpt/u2net.pth exists otherwise download it

app = Flask(__name__, static_url_path='/out', )
cors = CORS(app)
app.config['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,true'
app.config['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'

@app.route('/',  methods=['GET', 'POST'])

def hello():
    imageUrl = ''
    if request.method == 'POST':

        imageUrl = request.form.get('url')
        fileName = request.form.get('fileName')

        try:
           
            response = requests.get(imageUrl)
            input_image = Image.open(BytesIO(response.content))
            img_pil = engine.remove_bg(input_image)
            img_byte_arr = BytesIO()
            img_pil.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            output_file = cloudinary.uploader.upload(img_byte_arr)

            return {
                "source": imageUrl,
                "output": output_file
            }
        except Exception as e:
            return {
                "error": "Something went bad",
                "message" : str(e)
            }

    return {
        "msg": "something went wrong",
    }

port = int(os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=port)