# proxyrequest/utils.py
import requests
from typing import Optional, Dict

def proxy_verifier(proxy: Optional[Dict[str, str]] = None, test_url: str = "http://httpbin.org/ip", timeout: int = 5, headers: Optional[Dict[str, str]] = None, verify: bool = True) -> bool:
    """
    Checks whether the given proxy is working by making a simple HTTP request to a test URL.
    If no proxy is provided, it fetches the public IP directly.

    Args:
        proxy (dict, optional): The proxy configuration (e.g., {"http": "http://proxy_ip:port", "https": "https://proxy_ip:port"}). Default is None.
        test_url (str): The URL to test the proxy against. Default is http://httpbin.org/ip.
        timeout (int): The timeout value for the request in seconds. Default is 5 seconds.
        headers (dict, optional): Custom headers to be sent with the request. Default is None, which sends a standard User-Agent.
        verify (bool, optional): Whether to verify SSL certificates. Default is True. Set to False if you want to skip SSL verification.

    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    # If no proxy is provided, default to an empty dictionary
    if proxy is None:
        proxy = {}

    # If no custom headers are provided, use a default User-Agent header
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    try:
        # If no proxy is given, get the public IP directly
        if not proxy:
            response = requests.get(test_url, headers=headers, timeout=timeout, verify=verify)
        else:
            # Sending a GET request to the test URL using the proxy, custom headers, timeout, and SSL verification
            response = requests.get(test_url, proxies=proxy, headers=headers, timeout=timeout, verify=verify)
        
        # If the status code is 200, the proxy is working or we got the IP
        if response.status_code == 200:
            if not proxy:
                # If no proxy, just print and return the public IP
                public_ip = response.json().get("origin", "Unknown")
                print(f"Public IP is used: {public_ip}")
                return True
            else:
                # If proxy was used, print success
                print(f"Proxy {proxy} is working!")
                return True
        else:
            print(f"Failed with status code {response.status_code}")
            return False    

    except requests.exceptions.ConnectTimeout:
        print(f"Error: timeout")
        return False

    except requests.exceptions.ConnectionError:
        print(f"Error: check net connections")
        return False

    except requests.exceptions.SSLError:
        print(f"Error: certificate verify failed (SSL)")
        return False

    except Exception as error:
        print(error.__class__)
        return False 
   