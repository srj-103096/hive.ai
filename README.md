# Fixes
Fixed nginx02 filename typo in the original entrypoint.
Corrected nginx ports to 8000, 8001 and 8002.
 Added separate nginx PID files.
Changed HAProxy backend addresses to 127.0.0.1.
Added HAProxy backend health checks.
Changed the application response to:
"it works! solved by suraj"
Added /solution.txt.
Added a metrics scraper container.
Routed /metrics through HAProxy.
# Run
```bash
docker compose build
docker compose up -d
