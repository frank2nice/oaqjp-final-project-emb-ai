"""
Flask Web Server for the Emotion Detection Application
"""

from flask import Flask, render_template, request, jsonify
from EmotionDetection import emotion_detector
import json


app = Flask("Emotion Detector")

@app.route("/")
def render_index_page():
    """
    Render the main HTML template
    """
    return render_template('index.html'), 200

@app.route("/emotionDetector")
def emotion_analyzer():
    """
    Analyze the emotion from the text in the request
    """
    try:
        # Get the text from the GET request
        text_to_analyze = request.args.get('textToAnalyze')
        
        # Check if text is provided - 400 Bad Request
        if not text_to_analyze:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Please provide text to analyze.',
                'code': 400
            }), 400
        
        # Calling the emotion_detector function
        result = emotion_detector(text_to_analyze)
        
        # Checking for errors from the emotion_detector
        if 'error' in result:
            return jsonify({
                'error': 'Emotion Detection Error',
                'message': result['error'],
                'code': 500
            }), 500
        
        # Extract emotion scores values
        anger = result.get('anger', 0)
        disgust = result.get('disgust', 0)
        fear = result.get('fear', 0)
        joy = result.get('joy', 0)
        sadness = result.get('sadness', 0)
        dominant = result.get('dominant_emotion', 'Unknown')
        
        # Format the response as specified
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {anger}, 'disgust': {disgust}, "
            f"'fear': {fear}, 'joy': {joy} and "
            f"'sadness': {sadness}. The dominant emotion is {dominant}."
        )
        
        # 200 OK - Success with the formatted response
        return jsonify({
            'status': 'success',
            'data': result,
            'message': response_text,
            'code': 200
        }), 200
        
    except requests.exceptions.ConnectionError:
        # 503 Service Unavailable - API connection error
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'Unable to connect to the emotion detection service. Please try again later.',
            'code': 503
        }), 503
        
    except requests.exceptions.Timeout:
        # 504 Gateway Timeout - API timeout
        return jsonify({
            'error': 'Gateway Timeout',
            'message': 'The emotion detection service timed out. Please try again.',
            'code': 504
        }), 504
        
    except json.JSONDecodeError:
        # 500 Internal Server Error - Invalid JSON response
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Invalid response received from the emotion detection service.',
            'code': 500
        }), 500
        
    except Exception as e:
        # 500 Internal Server Error - Unexpected error
        return jsonify({
            'error': 'Internal Server Error',
            'message': f'An unexpected error occurred: {str(e)}',
            'code': 500
        }), 500

# Error handlers for most common HTTP errors
@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors
    """
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found on the server.',
        'code': 404
    }), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    """
    Handle 405 Method Not Allowed errors
    """
    return jsonify({
        'error': 'Method Not Allowed',
        'message': 'The method is not allowed for the requested URL.',
        'code': 405
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle 500 Internal Server errors
    """
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred on the server.',
        'code': 500
    }), 500

@app.errorhandler(400)
def bad_request_error(error):
    """
    Handle 400 Bad Request errors
    """
    return jsonify({
        'error': 'Bad Request',
        'message': 'The server could not understand the request due to invalid syntax.',
        'code': 400
    }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)