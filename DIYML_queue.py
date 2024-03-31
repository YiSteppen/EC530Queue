from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from uuid import uuid4
from queue import Queue

# Create queues
DIYML = Flask(__name__)
inference_queue = Queue()
training_queue = Queue()
def process_inference_queue():
    while True:
        # Get a task from the queue
        task = inference_queue.get()
        print(f"Processing inference request: {task}")
        inference_queue.task_done()

def process_training_queue():
    while True:
        task = training_queue.get()
        print(f"Processing training request: {task}")
        training_queue.task_done()


@DIYML.route('/submit_inference', methods=['POST'])
def submit_inference():
    data = request.json
    inference_queue.put(data)
    return jsonify({'message': 'Inference request submitted successfully.'}), 200

@DIYML.route('/submit_training', methods=['POST'])
def submit_training():
    data = request.json
    training_queue.put(data)
    return jsonify({'message': 'Training request submitted successfully.'}), 200

if __name__ == '__main__':
    DIYML.run(debug=True, port=5000)