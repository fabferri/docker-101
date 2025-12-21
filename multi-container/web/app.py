from flask import Flask, jsonify
import redis
import os
import socket

app = Flask(__name__)

# Redis connection
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Container App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .counter {
                font-size: 48px;
                color: #667eea;
                font-weight: bold;
                margin: 20px 0;
            }
            .info {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }
            button {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px 5px;
            }
            button:hover {
                background-color: #764ba2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐳 Multi-Container Docker Application</h1>
            <p>This page demonstrates a Flask web app communicating with a Redis database.</p>
            
            <div class="counter">
                <p>Visit Count: <span id="count">Loading...</span></p>
            </div>
            
            <button onclick="incrementCounter()">Increment Counter</button>
            <button onclick="resetCounter()">Reset Counter</button>
            
            <div class="info">
                <h3>Architecture:</h3>
                <ul>
                    <li><strong>Web Service:</strong> Flask (Python) - This page</li>
                    <li><strong>Database:</strong> Redis - Stores the counter</li>
                    <li><strong>Network:</strong> Docker bridge network for inter-container communication</li>
                    <li><strong>Volume:</strong> Persistent storage for Redis data</li>
                </ul>
            </div>
        </div>
        
        <script>
            async function getCount() {
                const response = await fetch('/api/count');
                const data = await response.json();
                document.getElementById('count').textContent = data.count;
            }
            
            async function incrementCounter() {
                await fetch('/api/increment', { method: 'POST' });
                getCount();
            }
            
            async function resetCounter() {
                await fetch('/api/reset', { method: 'POST' });
                getCount();
            }
            
            // Load count on page load
            getCount();
        </script>
    </body>
    </html>
    '''

@app.route('/api/count')
def get_count():
    try:
        count = redis_client.get('visit_count')
        if count is None:
            redis_client.set('visit_count', 0)
            count = 0
        return jsonify({'count': int(count)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/increment', methods=['POST'])
def increment():
    try:
        count = redis_client.incr('visit_count')
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    try:
        redis_client.set('visit_count', 0)
        return jsonify({'count': 0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return jsonify({
            'status': 'healthy',
            'redis': 'connected',
            'hostname': socket.gethostname()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'redis': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
