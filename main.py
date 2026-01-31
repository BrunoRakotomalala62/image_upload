import os
import time
import requests
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Note: Pour une utilisation réelle, l'utilisateur devrait fournir son propre CLIENT_ID.
# Nous utilisons ici un ID générique souvent trouvé dans les exemples publics pour le test.
IMGUR_CLIENT_ID = "546c25a59c58ad7" 

def delete_imgur_image(delete_hash):
    """Supprime une image d'Imgur en utilisant son deletehash."""
    url = f"https://api.imgur.com/3/image/{delete_hash}"
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"Image {delete_hash} supprimée avec succès.")
        else:
            print(f"Échec de la suppression de l'image {delete_hash}: {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")

# Initialisation du scheduler pour les tâches de suppression
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/upload', methods=['GET'])
def upload_image():
    image_url = request.args.get('imgur')
    
    if not image_url:
        return jsonify({"error": "Veuillez fournir une URL d'image via le paramètre 'imgur'."}), 400

    # Étape 1: Upload vers Imgur
    imgur_url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    payload = {
        "image": image_url,
        "type": "url"
    }

    try:
        response = requests.post(imgur_url, headers=headers, data=payload)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            image_data = data["data"]
            public_url = image_data["link"]
            delete_hash = image_data["deletehash"]

            # Étape 2: Programmer la suppression après 5 minutes (300 secondes)
            scheduler.add_job(
                func=delete_imgur_image,
                trigger='date',
                run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 300)),
                args=[delete_hash]
            )

            return jsonify({
                "status": "success",
                "image_url": public_url,
                "message": "L'image sera supprimée automatiquement dans 5 minutes pour protéger votre vie privée."
            })
        else:
            return jsonify({
                "status": "error",
                "message": data.get("data", {}).get("error", "Échec de l'upload vers Imgur.")
            }), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # L'API écoute sur le port 5000 par défaut
    app.run(host='0.0.0.0', port=5000)
