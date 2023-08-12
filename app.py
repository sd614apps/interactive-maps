from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Route to serve the HTML
@app.route('/')
def index():
    return render_template('index.html')

# Replace with your geocoding service endpoint and API key if required
GEOCODING_API_ENDPOINT = "https://nominatim.openstreetmap.org/search?format=json&q="

@app.route('/get-coordinates', methods=['POST'])
def get_coordinates():
    place_name = request.json.get('place_name')
    
    if not place_name:
        return jsonify({"error": "Invalid place name."}), 400

    response = requests.get(GEOCODING_API_ENDPOINT + place_name)
    
    if response.status_code != 200:
        return jsonify({"error": "Error fetching coordinates."}), 500

    coordinates_data = response.json()

    # For simplicity, pick the first result
    if coordinates_data:
        return jsonify({
            "lat": float(coordinates_data[0]["lat"]),
            "lon": float(coordinates_data[0]["lon"])
        })
    else:
        return jsonify({"error": "No coordinates found for given place name."}), 404

if __name__ == "__main__":
    app.run(debug=True)
