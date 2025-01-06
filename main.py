import os
from flask import Flask, redirect, request, Response, session
from google.cloud import storage
import io
from imagecaption import GenerateImageComponents


storage = storage.Client()
bucket_name = os.environ.get("CLOUD_BUCKET")

app = Flask(__name__)


@app.route('/')
def index():
    
    indexhtml = """
    <body>
    <br/>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <table align = 'center'>
            <tr>
                <td>Select a image</td>
                <td><input type="file" name="image" accept="image/**" required></td>
            </tr>
            <tr>
                <td colspan = 2 align = 'center'> <input type='submit' value='upload'</td>
            </tr>
        </table>
        <h2 align='center'>Avaiable Items </h2>
    </form>
    <ul align='center'>
    """
    image_files = all_image_files()
    for image in image_files:
        indexhtml += f'<li><a href="/files/{image}">{image}</a></li>'
    indexhtml += '''</ul>
    </body>'''
    return indexhtml

@app.route('/upload', methods=["POST"])
def upload_image():
    image = request.files['image']

    genAi = GenerateImageComponents()
    l = genAi.getCaptionAndDescription(image)
    text = l[0] + '|THE NEXT PART IS CAPTION|' + l[1]

    bucket = storage.bucket(bucket_name)
    blob_image = bucket.blob(image.filename)
    blob_image.upload_from_file(file_obj=image, rewind=True)

    blob_text = bucket.blob(image.filename.split('.')[0] + '.txt')
    blob_text.upload_from_string(text)
    
    
    return redirect("/")

@app.get('/images')
def all_image_files():
    images = []
    all_bucket_files = storage.list_blobs(bucket_name)
    for file in all_bucket_files:
        if file.name.lower().endswith(".jpeg") or file.name.lower().endswith(".jpg") or  file.name.lower().endswith(".png"):
            images.append(file.name)
    return images

@app.get('/files/<filename>')
def source_image_files(filename):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(filename.split(".")[0] + ".txt")
    file_content = None

    with blob.open('r') as file_obj:
        file_content = file_obj.read()
    
    description = file_content.split("|THE NEXT PART IS CAPTION|")[0]
    caption = file_content.split("|THE NEXT PART IS CAPTION|")[1]

    html_file = f'''
    <br/>
    <body>
    <div style="background: radial-gradient(black, transparent); padding: 50px; 
                                border-radius: 120px; margin-left: 100px; margin-right: 100px;">
        <a href="/" style="padding: 50px;">Back to Home Page</a>
    <br/>
        <center >
            <h2>{filename}</h2>
            <img src="/images/{filename}" width='25%'>
        
        <br/><br/>

        <div style="padding: 15px;margin-left: 125px;margin-right: 125px;border-radius: 30px;background: #eef1ee;">
            <h2> Caption </h2>
            <p>{caption}</p>

            <h2> Description </h2>
            <p>{description}</p>
        </div>
        </center>
    </div>
    </body>
    '''

    return html_file


@app.get('/images/<imagename>')
def getfile(imagename):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(imagename)
    file_data = blob.download_as_bytes()
    return Response(io.BytesIO(file_data), mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="localhost",port=5060, debug=True)
