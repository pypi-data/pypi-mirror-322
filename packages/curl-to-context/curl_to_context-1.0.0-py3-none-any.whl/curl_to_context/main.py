import pyperclip
import re
import argparse
from typing import Optional

def validate_curl_command(command: str) -> bool:
    """Validate if the string is a curl command."""
    return command.strip().startswith('curl ')

def extract_cookies_from_curl(curl_command: str) -> Optional[dict]:
    """Extract cookies from curl command."""
    cookie_match = re.search(r"-H 'cookie: (.*?)'", curl_command)
    if not cookie_match:
        return None
    
    cookie_str = cookie_match.group(1)
    cookies = {}
    for cookie in cookie_str.split('; '):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key] = value
    return cookies

def extract_headers_from_curl(curl_command: str) -> dict:
    """Extract headers from curl command."""
    headers = {}
    header_pattern = r"-H '(.*?): (.*?)'"
    for match in re.finditer(header_pattern, curl_command):
        key, value = match.groups()
        if key.lower() != 'cookie':  # Skip cookie header as it's handled separately
            headers[key] = value
    return headers

def extract_url_from_curl(curl_command: str) -> str:
    """Extract URL from curl command."""
    url_match = re.search(r"curl '([^']*)'", curl_command)
    if url_match:
        return url_match.group(1)
    return ""

def extract_data_from_curl(curl_command: str) -> Optional[str]:
    """Extract data from curl command."""
    data_match = re.search(r"--data-raw '([^']*)'", curl_command)
    if data_match:
        return data_match.group(1)
    return None

def convert_curl_to_code(curl_command: str, framework: str = 'grab') -> str:
    """Convert curl command to Python code for specified framework."""
    cookies = extract_cookies_from_curl(curl_command)
    headers = extract_headers_from_curl(curl_command)
    url = extract_url_from_curl(curl_command)
    data = extract_data_from_curl(curl_command)
    
    code = []
    
    if framework == 'grab':
        code.append("def method_name(self):")
        if cookies:
            code.append("    self.g.setup(cookies={")
            for key, value in cookies.items():
                code.append(f"        '{key}': '{value}',")
            code.append("    })")
            code.append("")
        
        if headers:
            code.append("    self.g.setup(headers={")
            for key, value in headers.items():
                code.append(f"        '{key}': '{value}',")
            code.append("    })")
    else:  # context
        code.append("def method_name(self):")
        if cookies:
            code.append("    self.context.cookies.update({")
            for key, value in cookies.items():
                code.append(f"        '{key}': '{value}',")
            code.append("    })")
            code.append("")
        
        if headers:
            code.append("    self.context.headers.update({")
            for key, value in headers.items():
                code.append(f"        '{key}': '{value}',")
            code.append("    })")
    
    # Add URL and data if present
    if url:
        code.append(f"\n    # URL: {url}")
    if data:
        code.append(f"    # Data: {data}")
    
    return "\n".join(code)

def main():
    parser = argparse.ArgumentParser(description='Convert curl command to Python code')
    parser.add_argument('-f', '--framework', choices=['grab', 'context'],
                       help='Target framework (if not specified, will ask interactively)')
    args = parser.parse_args()
    
    # If framework not specified, ask user interactively
    framework = args.framework
    if not framework:
        while True:
            choice = input("Choose framework (g=Grab, c=Context): ").lower().strip()
            if choice == 'g':
                framework = 'grab'
                break
            elif choice == 'c':
                framework = 'context'
                break
            print("Invalid choice. Please enter 'g' for Grab or 'c' for Context.")
    
    print("Please copy your curl command to clipboard and press Enter...")
    input()
    
    # Get clipboard content
    curl_command = pyperclip.paste()
    
    # Validate curl command
    if not validate_curl_command(curl_command):
        print("Error: Invalid curl command. Please make sure you copied a valid curl command.")
        return
    
    # Convert to Python code
    python_code = convert_curl_to_code(curl_command, framework)
    
    # Copy result to clipboard
    pyperclip.copy(python_code)
    print(f"Converted code (for {framework}) has been copied to your clipboard!")

if __name__ == "__main__":
    main()