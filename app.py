from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from tiktok_downloader import download_tiktok_video_temp
import os

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    # Cek apakah request dari fetch (JSON) atau dari form (form-data)
    if request.is_json:
        data = request.get_json()
        url = data.get('url')
    else:
        url = request.form.get('url')
    if not url:
        return jsonify(success=False, error="URL tidak boleh kosong."), 400
    try:
        temp_path, filename = download_tiktok_video_temp(url)
        if not temp_path:
            return jsonify(success=False, error="Gagal mengunduh video."), 500
        # Kirim file langsung ke browser
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=filename,
            mimetype="video/mp4"
        )
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)