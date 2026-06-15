import redis
import json
import time
import os
import signal

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

running = True

def signal_handler(sig, frame):
    global running
    print("\nShutting down worker gracefully...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("Worker started. Waiting for hooks...")

while running:
    try:
        # Ждём задачу из очереди (5 секунд таймаут)
        task = r.brpop('hooks:queue', timeout=5)
        
        if task:
            data = json.loads(task[1])
            hook_id = data['id']
            
            print(f"Processing hook {hook_id}...")
            time.sleep(2)  # имитация полезной работы
            
            # Обновляем статус
            data['status'] = 'processed'
            data['processed_at'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            r.hset('hooks:processed', hook_id, json.dumps(data))
            
            print(f"Hook {hook_id} processed successfully")
            
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

print("Worker stopped.")