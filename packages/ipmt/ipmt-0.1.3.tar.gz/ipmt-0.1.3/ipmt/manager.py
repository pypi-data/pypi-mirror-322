import threading
from flask import request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import ipaddress
import logging
from typing import Dict, List, Optional, Union

class IPMT:
    def __init__(self, app_bp,
                 error: bool = True, 
                 request_limit: int = 60,
                 time_window: int = 60,
                 graylist_duration: int = 24,
                 blacklist_duration: int = 30):
        """
        Initialize IP Management Tool with configurable parameters.
        
        Args:
            app_bp: Flask blueprint
            request_limit: Max requests allowed per time_window
            time_window: Time window in seconds for rate limiting
            graylist_duration: Hours to keep IPs in graylist
            blacklist_duration: Days to keep IPs in blacklist
        """
        self.error = error
        self.app = app_bp
        self.request_limit = request_limit
        self.time_window = time_window
        
        # Use defaultdict for automatic initialization
        self.ip_requests: Dict[str, List[datetime]] = defaultdict(list)
        self.gray_list: Dict[str, datetime] = {}
        self.black_list: Dict[str, datetime] = {}
        self.gray_list_violations: Dict[str, int] = defaultdict(int)
        
        # Duration settings
        self.graylist_duration = timedelta(hours=graylist_duration)
        self.blacklist_duration = timedelta(days=blacklist_duration)
        
        # Whitelist for trusted IPs
        self.whitelist: List[Union[ipaddress.IPv4Network, ipaddress.IPv4Address]] = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Register the before_request method
        self.app.before_request(self.before_request)
        
        # Start the cleaner function
        self.start_cleaner()

    def setup_logging(self):
        """Configure logging for the IPMT module."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def add_to_whitelist(self, ip_or_network: str):
        """Add an IP or network to the whitelist."""
        try:
            # Try parsing as network first
            network = ipaddress.IPv4Network(ip_or_network)
            self.whitelist.append(network)
            self.logger.info(f"Added network {ip_or_network} to whitelist")
        except ValueError:
            # If not a network, try as single IP
            ip = ipaddress.IPv4Address(ip_or_network)
            self.whitelist.append(ip)
            self.logger.info(f"Added IP {ip_or_network} to whitelist")
    
    def is_whitelisted(self, ip: str) -> bool:
        """Check if an IP is whitelisted."""
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            return any(
                (isinstance(entry, ipaddress.IPv4Network) and ip_obj in entry) or
                (isinstance(entry, ipaddress.IPv4Address) and ip_obj == entry)
                for entry in self.whitelist
            )
        except ValueError:
            self.logger.warning(f"Invalid IP address format: {ip}")
            return False
    
    def before_request(self):
        """Process each incoming request for IP management."""
        try:
            ip = request.remote_addr
            if not ip:
                self.logger.warning("No IP address found in request")
                return None
                
            current_time = datetime.now()
            
            # Skip checks for whitelisted IPs
            if self.is_whitelisted(ip):
                return None
            
            # Check blacklist
            if ip in self.black_list:
                if self.black_list[ip] > current_time:
                    self.logger.warning(f"Blocked blacklisted IP: {ip}")
                    return jsonify(self.create_error_response("blacklisted", self.black_list[ip])), 403
                self.black_list.pop(ip)
            
            # Check graylist
            if ip in self.gray_list:
                if self.gray_list[ip] > current_time:
                    # Increment violations counter using defaultdict
                    self.gray_list_violations[ip] += 1
                    
                    # Check for maximum violations
                    if self.gray_list_violations[ip] >= 15:
                        self.add_to_blacklist(ip)
                        self.logger.warning(f"IP {ip} moved to blacklist due to repeated violations")
                        return jsonify(self.create_error_response("blacklisted", self.black_list[ip])), 403
                    
                    return jsonify(self.create_error_response("graylisted", self.gray_list[ip])), 403
                
                # Clear expired graylist entry and its violations
                self.gray_list.pop(ip)
                self.gray_list_violations.pop(ip, None)
            
            # Update request history and check rate limits
            self.clean_old_requests(ip, current_time)
            self.ip_requests[ip].append(current_time)
            
            if len(self.ip_requests[ip]) > self.request_limit:
                self.add_to_graylist(ip)
                self.logger.warning(f"IP {ip} added to graylist due to rate limiting")
                return jsonify(self.create_error_response("graylisted", self.gray_list[ip])), 403
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in before_request: {str(e)}")
            return None
    
    def add_to_graylist(self, ip: str):
        """Add an IP to the graylist."""
        self.gray_list[ip] = datetime.now() + self.graylist_duration
        # Initialize violations counter
        self.gray_list_violations[ip] = 0
    
    def add_to_blacklist(self, ip: str):
        """Add an IP to the blacklist."""
        self.black_list[ip] = datetime.now() + self.blacklist_duration
        # Clean up graylist entries
        self.gray_list.pop(ip, None)
        self.gray_list_violations.pop(ip, None)
    
    def clean_old_requests(self, ip: str, current_time: datetime):
        """Clean old requests outside the time window."""
        cutoff_time = current_time - timedelta(seconds=self.time_window)
        self.ip_requests[ip] = [
            req_time for req_time in self.ip_requests[ip]
            if req_time > cutoff_time
        ]
    
    def create_error_response(self, list_type: str, expiry: datetime) -> dict:
        """Create a standardized error response."""
        if self.error == True:
            return {
                "error": "Access denied",
                "reason": f"IP {list_type}",
                "expires": expiry.isoformat(),
                "retry_after": int((expiry - datetime.now()).total_seconds())
            }
        else:
            return {"error": "Forbidden"}  # Reject with 403 status code
    
    def start_cleaner(self):
        """Start the periodic cleaning process."""
        def cleaner():
            try:
                current_time = datetime.now()
                
                # Clean expired entries
                self.gray_list = {
                    ip: expiry for ip, expiry in self.gray_list.items()
                    if expiry > current_time
                }
                self.black_list = {
                    ip: expiry for ip, expiry in self.black_list.items()
                    if expiry > current_time
                }
                
                # Clean old requests for all IPs
                for ip in list(self.ip_requests.keys()):
                    self.clean_old_requests(ip, current_time)
                    if not self.ip_requests[ip]:  # Remove empty lists
                        del self.ip_requests[ip]
                
                # Clean violation counters for removed graylisted IPs
                self.gray_list_violations = defaultdict(int, {
                    ip: count for ip, count in self.gray_list_violations.items()
                    if ip in self.gray_list
                })
                
                self.logger.debug("Cleanup completed")
                
            except Exception as e:
                self.logger.error(f"Error in cleaner: {str(e)}")
            
            finally:
                threading.Timer(60, cleaner).start()
        
        cleaner()
    
    def get_status(self, ip: Optional[str] = None) -> dict:
        """Get current status of IP management system or specific IP."""
        status = {
            "total_tracked_ips": len(self.ip_requests),
            "graylisted_ips": len(self.gray_list),
            "blacklisted_ips": len(self.black_list),
            "whitelisted_entries": len(self.whitelist)
        }
        
        if ip:
            status["ip_details"] = {
                "requests_in_window": len(self.ip_requests.get(ip, [])),
                "is_graylisted": ip in self.gray_list,
                "is_blacklisted": ip in self.black_list,
                "is_whitelisted": self.is_whitelisted(ip),
                "graylist_violations": self.gray_list_violations.get(ip, 0)
            }
        
        return status