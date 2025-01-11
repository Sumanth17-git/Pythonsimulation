from flask import Flask, jsonify
import multiprocessing
import time

app = Flask(__name__)

# Function to simulate high CPU usage
def high_cpu_task(duration):
    """
    Perform a CPU-intensive task for the specified duration (in seconds).
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        # Perform a computationally expensive operation
        for _ in range(50_000_000):
            pass  # Busy loop for CPU load

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the High CPU Usage Simulator!"})

@app.route("/high_cpu", methods=["GET"])
def trigger_high_cpu():
    """
    Trigger high CPU usage across all cores for 30 seconds.
    """
    duration = 30  # Duration in seconds
    num_cores = multiprocessing.cpu_count()  # Get the number of CPU cores
    processes = []

    # Start a CPU-intensive task on each core
    for _ in range(num_cores):
        process = multiprocessing.Process(target=high_cpu_task, args=(duration,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    return jsonify({"status": "High CPU task started", "duration": duration, "cores_used": num_cores}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
