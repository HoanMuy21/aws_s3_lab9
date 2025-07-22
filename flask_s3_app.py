from flask import Flask, request, jsonify
import boto3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

S3_BUCKET = os.getenv('S3_BUCKET')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=AWS_REGION
)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return '''
        <h2>Upload file lên S3</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <button type="submit">Upload</button>
        </form>
        '''

    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'error': 'Chưa chọn tệp'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    try:
        s3_client.upload_fileobj(file, S3_BUCKET, filename)
        file_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return f'''
        <h3>Upload thành công!</h3>
        <p>Link tải: <a href="{file_url}" target="_blank">{file_url}</a></p>
        <a href="/upload">⬅ Quay lại</a>
        '''
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'khỏe mạnh'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
