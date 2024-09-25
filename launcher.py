import subprocess
import threading
import time

# Function to launch the server
def launch_server():
    print("Starting server...")
    subprocess.Popen(["python", "server.py"])

# Function to launch a client
def launch_client(client_name):
    print(f"Starting {client_name}...")
    subprocess.Popen(["python", client_name])

def main():
    # Start the server
    server_thread = threading.Thread(target=launch_server)
    server_thread.start()

    # Give the server some time to start
    time.sleep(1)

    # Start the clients (modify the file names if needed)
    client1_thread = threading.Thread(target=launch_client, args=("client1/client1.py",))
    client2_thread = threading.Thread(target=launch_client, args=("client2/client2.py",))

    client1_thread.start()
    client2_thread.start()

    # Wait for all threads to finish (optional, depending on use case)
    server_thread.join()
    client1_thread.join()
    client2_thread.join()

if __name__ == "__main__":
    main()
