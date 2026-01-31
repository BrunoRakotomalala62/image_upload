from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "a88b9a3d4987f27a9dce837977c77949"

@app.route('/upload', methods=['GET'])
def upload_image():
    # Utilisation du paramètre 'img' comme demandé
    image_url = request.args.get('img')
    if not image_url:
        return jsonify({"error": "Paramètre 'img' manquant"}), 400

    try:
        # Préparation de la requête vers ImgBB
        imgbb_url = f"https://api.imgbb.com/1/upload?key={API_KEY}"
        response = requests.post(imgbb_url, data={'image': image_url})
        
        if response.status_code == 200:
            data = response.json()
            # Extraction du lien direct vers l'image
            direct_url = data.get('data', {}).get('url')
            return jsonify({"image_direct": direct_url})
        else:
            return jsonify({"error": "Échec de l'upload sur ImgBB", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Configuration pour le déploiement (port 5000 par défaut)
    app.run(host='0.0.0.0', port=5000)
