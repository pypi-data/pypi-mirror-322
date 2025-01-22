# proxyrequest/utils.py
import requests
from typing import Optional, Dict

def proxy_verifier(proxy: Dict[str, str], test_url: str = "http://httpbin.org/ip", timeout: int = 5, headers: Optional[Dict[str, str]] = None, verify: bool = True) -> bool:
    """
    Checks whether the given proxy is working by making a simple HTTP request to a test URL.
    
    Args:
        proxy (dict): The proxy configuration (e.g., {"http": "http://proxy_ip:port", "https": "https://proxy_ip:port"}).
        test_url (str): The URL to test the proxy against. Default is http://httpbin.org/ip.
        timeout (int): The timeout value for the request in seconds. Default is 5 seconds.
        headers (dict, optional): Custom headers to be sent with the request. Default is None, which sends a standard User-Agent.
        verify (bool, optional): Whether to verify SSL certificates. Default is True. Set to False if you want to skip SSL verification.

    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    # If no custom headers are provided, use a default User-Agent header
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    try:
        # Sending a GET request to the test URL using the proxy, custom headers, timeout, and SSL verification
        response = requests.get(test_url, proxies=proxy, headers=headers, timeout=timeout, verify=verify)
        
        # If the status code is 200, the proxy is working
        if response.status_code == 200:
            print(f"Proxy {proxy} is working!")
            return True
        else:
            print(f"Proxy {proxy} failed with status code {response.status_code}")
            return False
    except requests.RequestException as e:
        # If there is any exception (e.g., timeout, connection error, etc.), the proxy is not working
        print(f"Error testing proxy {proxy}: {e}")
        return False