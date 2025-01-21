
# IPMT - Flask IP Management Tool

**IPMT** is a Flask-based IP management library designed to help you manage IP addresses, monitor visitor activity, and protect your website from malicious traffic (e.g., DDoS attacks).

## Features
- Request rate limiting (customizable thresholds).
- Whitelist, graylist, and blacklist IPs or networks.
- Monitor and log visitor activity.
- Protect your website from DDoS attacks with customizable policies.
- Automatic cleanup of expired graylist and blacklist entries.

## Installation

You can install **IPMT** using pip:

```bash
pip install ipmt
```

## Simple Usage

Here’s a minimal example of how to use **IPMT** in your Flask application:

```python
from flask import Flask
from ipmt.manager import IPMT

app = Flask(__name__)

# Initialize IPMT with customized configurations
ip_manager = IPMT(app, 
    request_limit=60,  # Max 60 requests
    time_window=60,    # Per 60 seconds
    graylist_duration=24,  # Graylist duration in hours
    blacklist_duration=30  # Blacklist duration in days
)

# Add trusted IPs/networks to the whitelist
ip_manager.add_to_whitelist("10.0.0.0/24")
ip_manager.add_to_whitelist("192.168.1.100")

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the home page!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

### How It Works:
1. **Rate Limiting**: The library tracks requests from each IP address and enforces a limit based on the configured `request_limit` and `time_window`.
2. **Whitelisting**: Trusted IPs or networks are exempt from rate limiting and blacklisting/graylisting.
3. **Graylisting & Blacklisting**: If an IP exceeds the request limit, it is temporarily added to the graylist. After a certain number of violations, the IP is moved to the blacklist.

## Customization

You can customize the following settings in the `IPMT` initialization:
- `request_limit`: Maximum number of requests allowed per IP within the `time_window` (default is 60).
- `time_window`: Time window in seconds (default is 60).
- `graylist_duration`: Duration (in hours) an IP remains in the graylist (default is 24 hours).
- `blacklist_duration`: Duration (in days) an IP remains in the blacklist (default is 30 days).

### Adding IPs to Whitelist

You can add single IPs or networks to the whitelist:

```python
ip_manager.add_to_whitelist("10.0.0.0/24")  # Add network to whitelist
ip_manager.add_to_whitelist("192.168.1.100")  # Add single IP to whitelist
```

### Getting the Status

You can check the current status of IP management, including the number of tracked IPs, graylisted/blacklisted IPs, and the whitelist:

```python
status = ip_manager.get_status()
print(status)

# Get specific details for an IP address
ip_status = ip_manager.get_status("192.168.1.100")
print(ip_status)
```

## Logging

**IPMT** automatically logs activities like adding IPs to the whitelist, graylist, and blacklist, as well as any violations and errors.

You can customize the logging format or change the logging level if needed. Logs are output to the console by default.

## Example Error Responses

When an IP is rate-limited, the system returns a response like this:

```json
{
  "error": "Access denied",
  "reason": "IP graylisted",
  "expires": "2025-01-01T12:00:00",
  "retry_after": 3600
}
```

This response tells the client that their IP is graylisted and includes the time when they can retry after the lock expires.
