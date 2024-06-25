from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from my_model_module import recommend_courses

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins on all routes

# Load your model
model = joblib.load('./model/recommend_courses.joblib')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.is_json:
        data = request.json
        print("Received data:", data)  # Check if data is being received
        try:
            # Assuming recommend_courses returns a DataFrame or a list of recommended courses
            recommendations = recommend_courses(data['course_title'])  # Adjust according to your function
            return jsonify(recommendations.to_dict(orient='records'))  # Convert DataFrame to JSON
        except KeyError as ke:
            return jsonify({"error": f"KeyError: {str(ke)}"}), 400  # Bad Request if key 'course_title' is missing
        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error for other exceptions
    else:
        return jsonify({"error": "Unsupported Media Type: Expected application/json"}), 415

if __name__ == '__main__':
    app.run(port=5000)
