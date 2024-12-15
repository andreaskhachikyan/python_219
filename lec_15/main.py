from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "cars_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        car_list = json.load(file)
else:
    car_list = []

def save_to_file():
    with open(DATA_FILE, "w") as file:
        json.dump(car_list, file, indent=4)

@app.route("/cars", methods=["GET"])
def get_all_cars():
    return jsonify(car_list)

@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car_by_id(car_id):
    car = next((c for c in car_list if c["id"] == car_id), None)
    if car:
        return jsonify(car)
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars", methods=["POST"])
def add_car():
    new_car = request.json
    if not new_car.get("id") or any(c["id"] == new_car["id"] for c in car_list):
        return jsonify({"error": "Car ID must be unique and provided"}), 400
    car_list.append(new_car)
    save_to_file()
    return jsonify(new_car), 201

@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = next((c for c in car_list if c["id"] == car_id), None)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    updated_data = request.json
    car.update(updated_data)
    save_to_file()
    return jsonify(car)

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    global car_list
    updated_list = [c for c in car_list if c["id"] != car_id]
    if len(updated_list) == len(car_list):
        return jsonify({"error": "Car not found"}), 404
    car_list = updated_list
    save_to_file()
    return jsonify({"message": "Car deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)