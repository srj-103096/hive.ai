#!/usr/bin/env python3

import os
import time
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer


def cpu_usage():
    with open("/proc/stat", "r") as f:
        line = f.readline()

    values = line.split()[1:]
    values = [int(v) for v in values]

    idle = values[3]
    total = sum(values)

    return total, idle


def memory_metrics():
    memory = {}

    with open("/proc/meminfo", "r") as f:
        for line in f:
            key, value = line.split(":", 1)
            value = value.strip().split()[0]
            memory[key] = int(value) * 1024

    return memory


def load_average():
    with open("/proc/loadavg", "r") as f:
        return float(f.read().split()[0])


def metrics():
    cpu1, idle1 = cpu_usage()
    time.sleep(0.1)
    cpu2, idle2 = cpu_usage()

    total_delta = cpu2 - cpu1
    idle_delta = idle2 - idle1

    if total_delta > 0:
        cpu_percent = 100.0 * (1 - idle_delta / total_delta)
    else:
        cpu_percent = 0.0

    memory = memory_metrics()

    total_memory = memory.get("MemTotal", 0)
    available_memory = memory.get("MemAvailable", 0)
    used_memory = total_memory - available_memory

    disk = shutil.disk_usage("/")

    output = [
        "# HELP system_cpu_usage_percent CPU usage percentage",
        "# TYPE system_cpu_usage_percent gauge",
        f"system_cpu_usage_percent {cpu_percent:.2f}",

        "# HELP system_memory_total_bytes Total memory",
        "# TYPE system_memory_total_bytes gauge",
        f"system_memory_total_bytes {total_memory}",

        "# HELP system_memory_available_bytes Available memory",
        "# TYPE system_memory_available_bytes gauge",
        f"system_memory_available_bytes {available_memory}",

        "# HELP system_memory_used_bytes Used memory",
        "# TYPE system_memory_used_bytes gauge",
        f"system_memory_used_bytes {used_memory}",

        "# HELP system_load_average_1m One minute load average",
        "# TYPE system_load_average_1m gauge",
        f"system_load_average_1m {load_average():.2f}",

        "# HELP system_disk_total_bytes Total disk space",
        "# TYPE system_disk_total_bytes gauge",
        f"system_disk_total_bytes {disk.total}",

        "# HELP system_disk_used_bytes Used disk space",
        "# TYPE system_disk_used_bytes gauge",
        f"system_disk_used_bytes {disk.used}",

        "# HELP system_disk_free_bytes Free disk space",
        "# TYPE system_disk_free_bytes gauge",
        f"system_disk_free_bytes {disk.free}",
    ]

    return "\n".join(output) + "\n"


class MetricsHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/metrics":
            data = metrics().encode()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)

        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK\n")

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", 9100), MetricsHandler)

print("Metrics scraper listening on port 9100")

server.serve_forever()
