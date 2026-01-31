from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "a88b9a3d4987f27a9dce837977c77949"

@app.route('/upload', methods=['GET'])
def upload_image():
    image_input = request.args.get('img')
    if not image_input:
        return jsonify({"error": "Paramètre 'img' manquant"}), 400

    try:
        # L'URL d'upload ImgBB avec la clé API
        imgbb_url = f"https://api.imgbb.com/1/upload?key={API_KEY}"
        
        # Si c'est du Base64 (data:image/...)
        if image_input.startswith('data:image'):
            # On retire le préfixe 'data:image/...;base64,' pour ne garder que la donnée
            if ',' in image_input:
                image_input = image_input.split(',', 1)[1]
        
        # Envoi à ImgBB (ImgBB accepte soit une URL, soit du base64 dans le champ 'image')
        response = requests.post(imgbb_url, data={'image': image_input})
        
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
