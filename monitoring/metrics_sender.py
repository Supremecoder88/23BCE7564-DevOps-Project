import socket
import time
import psutil

GRAPHITE_HOST = 'localhost'
GRAPHITE_PORT = 2003

def send_metric(name, value):
    try:
        message = f"techsymp.devops.{name} {value} {int(time.time())}\n"
        sock = socket.socket()
        sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
        sock.sendall(message.encode())
        sock.close()
        print(f"Sent: {name} -> {value}")
    except Exception as e:
        print(f"Error sending metric: {e}")

if __name__ == "__main__":
    print(f"Starting metrics collection (to {GRAPHITE_HOST}:{GRAPHITE_PORT})...")
    while True:
        send_metric('cpu_usage', psutil.cpu_percent())
        send_metric('mem_usage', psutil.virtual_memory().percent)
        time.sleep(10)
