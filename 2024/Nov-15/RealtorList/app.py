from flask import Flask, request, jsonify, send_file
from pathlib import Path
from datetime import datetime, UTC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Default route for the root URL."""
    return jsonify({
        "message": "Welcome to the Realtor Search API!",
        "available_endpoints": [
            "/health - Check API health",
            "/run_search - Search for agents (POST)",
            "/scrape - Scrape agent data (POST)"
        ],
        "timestamp": datetime.now(UTC).isoformat()
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint for Make.com."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": "realtor-search-api"
    })

@app.route('/run_search', methods=['POST'])
def run_search():
    """Return stored agent data for requested city and state."""
    try:
        # Get search parameters from request
        search_params = request.get_json()
        if not search_params or 'city' not in search_params or 'state' not in search_params:
            return jsonify({
                "error": "City and state parameters required",
                "status": "error",
                "timestamp": datetime.now(UTC).isoformat()
            }), 400

        # Construct path to JSON file
        file_path = Path(__file__).parent / "output" / f"agents_{search_params['city'].lower()}_{search_params['state'].lower()}.json"
        
        if not file_path.exists():
            return jsonify({
                "error": f"No data found for {search_params['city']}, {search_params['state']}",
                "status": "error",
                "timestamp": datetime.now(UTC).isoformat()
            }), 404

        # Return the JSON file
        return send_file(file_path, mimetype='application/json')

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": datetime.now(UTC).isoformat()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 