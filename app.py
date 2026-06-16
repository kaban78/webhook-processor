from flask import Flask, request, jsonify, render_template
import redis
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/hook', methods=['POST'])
def receive_hook():
    hook_id = str(uuid.uuid4())[:8]
    
    data = {
        "id": hook_id,
        "timestamp": datetime.now().isoformat(),
        "headers": dict(request.headers),
        "body": request.get_json(silent=True) or {},
        "status": "received"
    }
    
    r.lpush('hooks:queue', json.dumps(data))
    r.hset('hooks:processed', hook_id, json.dumps(data))
    
    return jsonify({
        "hook_id": hook_id,
        "status": "queued",
        "message": "Webhook received and queued for processing"
    }), 202

@app.route('/hooks', methods=['GET'])
def list_hooks():
    hooks = r.hgetall('hooks:processed')
    result = []
    for key, value in hooks.items():
        result.append(json.loads(value))
    result.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(result)
@app.route('/')
def index():
    hooks = r.hgetall('hooks:processed')
    result = []
    for key, value in hooks.items():
        hook_data = json.loads(value)
        result.append({
            'id': key,
            'data': hook_data
        })
    result.sort(key=lambda x: x['data']['timestamp'], reverse=True)
    return render_template('index.html', hooks=result, total=len(result))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)