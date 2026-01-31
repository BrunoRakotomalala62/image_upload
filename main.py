from flask import Flask, request, jsonify
import requests
import re
import base64

app = Flask(__name__)

API_KEY = "a88b9a3d4987f27a9dce837977c77949"

@app.route('/upload', methods=['GET'])
def upload_image():
    image_input = request.args.get('img')
    if not image_input:
        return jsonify({"error": "Paramètre 'img' manquant"}), 400

    try:
        imgbb_url = f"https://api.imgbb.com/1/upload?key={API_KEY}"
        
        # Vérifier si l'entrée est une chaîne Base64 (format data:image/...)
        if image_input.startswith('data:image'):
            # Extraire uniquement la partie base64
            # Format attendu : data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
            base64_data = re.sub(r'^data:image/.+;base64,', '', image_input)
            payload = {'image': base64_data}
        else:
            # Sinon, on considère que c'est une URL classique
            payload = {'image': image_input}

        response = requests.post(imgbb_url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            direct_url = data.get('data', {}).get('url')
            return jsonify({"image_direct": direct_url})
        else:
            return jsonify({
                "error": "Échec de l'upload sur ImgBB", 
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
