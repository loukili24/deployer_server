from flask import Flask, request, jsonify
import ipinfo
from geopy.geocoders import Nominatim
import os
import logging

app = Flask(__name__)

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to predict BME (placeholder)
def bme_prediction(temperature, humidity, pressure, gas_resistance):
    p = temperature + humidity + pressure + gas_resistance
    return p

# Global variable to store the latest received data
latest_data = {}

# Function to calculate battery level and life (placeholders)
def calculate_battery_level(voltage):
    return voltage * 10

def calculate_battery_life(voltage):
    return voltage * 20

# Function to get IP information
def get_ip_info(ip_address):
    try:
        access_token = os.getenv('IPINFO_ACCESS_TOKEN')  # Use environment variable for ipinfo access token
        if not access_token:
            raise ValueError("IPINFO_ACCESS_TOKEN environment variable not set")

        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip_address)
        
        city = details.city
        region = details.region
        country = details.country
        
        # Use geopy to get more precise latitude and longitude
        location = geolocator.geocode(f"{city}, {region}, {country}")
        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            latitude, longitude = details.loc.split(',')

        return {
            "country": country,
            "region": region,
            "city": city,
            "postal": details.postal,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": details.timezone,
            "isp": details.org,
            "asn": details.org.split(' ')[0]  # Assuming the ASN is the first part of org
        }
    except Exception as e:
        logging.error(f"Error fetching IP info: {e}")
        return {"error": "Unable to fetch IP information"}

@app.route('/')
def home():
    # Display the latest received data
    return jsonify(latest_data)

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")
        
        # Further validation for required fields
        required_fields = ['Temperature', 'Humidity', 'Pressure', 'Gas_resistance']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        logging.info(f"Received data: {data}")

        # Extract gateway_data
        gateway_data = data.get('data', {})

        # Process gateway_data
        processed_gateway_data = process_data(gateway_data)

        latest_data = {
            "message": "Data received and processed",
            "gateway_data": processed_gateway_data
        }

        logging.info(f"Response data: {latest_data}")
        return jsonify(latest_data), 200
    except ValueError as ve:
        logging.error(f"Validation Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def process_data(data):
    temperature = float(data.get('Temperature', 0))
    humidity = float(data.get('Humidity', 0))
    pressure = float(data.get('Pressure', 0))
    gas_resistance = float(data.get('Gas_resistance', 0))
    prediction = bme_prediction(temperature, humidity, pressure, gas_resistance)

    processed_data = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "gas_resistance": gas_resistance,
        "prediction": prediction
    }

    return processed_data

if __name__ == '__main__':
    app.run(debug=True)
