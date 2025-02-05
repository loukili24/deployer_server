from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Placeholder for the bme_prediction function
def bme_prediction(temperature, humidity, pressure, gas_resistance):
    p = temperature + humidity + pressure + gas_resistance
    return p

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        print(f"Received data: {data}")

        # Extract gateway_data
        gateway_data = data.get('data', {})

        # Process gateway_data
        processed_gateway_data = process_data(gateway_data)

        response = {
            "message": "Data received and processed",
            "gateway_data": processed_gateway_data
        }

        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
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

    return processed_data

if __name__ == '__main__':
    app.run(debug=True)
