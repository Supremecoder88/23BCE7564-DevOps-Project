# Monitoring Configuration Details

## 1. Nagios Configuration
To monitor the website availability, add the following to your Nagios configuration file (e.g., `/usr/local/nagios/etc/objects/website.cfg`):

```nagios
define host {
    use                     linux-server
    host_name               techsymp-website
    alias                   College Event Website
    address                 localhost  # Or K8s Service IP
    check_command           check-host-alive
}

define service {
    use                     generic-service
    host_name               techsymp-website
    service_description     HTTP Availability
    check_command           check_http!-p 30001
}
```

## 2. Graphite Metrics Collection
To send metrics to Graphite, you can use a simple script or a sidecar container. Here is a sample Python snippet to send CPU usage:

```python
import socket
import time
import psutil

GRAPHITE_HOST = 'localhost'
GRAPHITE_PORT = 2003

def send_metric(name, value):
    message = f"techsymp.devops.{name} {value} {int(time.time())}\n"
    sock = socket.socket()
    sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
    sock.sendall(message.encode())
    sock.close()

while True:
    send_metric('cpu_usage', psutil.cpu_percent())
    send_metric('mem_usage', psutil.virtual_memory().percent)
    time.sleep(10)
```

## 3. Grafana Dashboard JSON
Import this JSON into Grafana to visualize the metrics:
- **Datasource**: Graphite
- **Metrics**: 
    - `techsymp.devops.cpu_usage`
    - `techsymp.devops.mem_usage`
- **Dashboards**: Create panels for CPU, Memory, and Uptime.

### Required Metrics for Grafana:
- **CPU Usage**: `aliasByNode(techsymp.devops.cpu_usage, 2)`
- **Memory Usage**: `aliasByNode(techsymp.devops.mem_usage, 2)`
- **HTTP Status**: Using Nagios datasource or simple Ping.
