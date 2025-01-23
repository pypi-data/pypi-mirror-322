from typing import Dict, Any
import json

class ContextCodeWriter:
    """Generates Context framework code from parsed curl commands."""
    
    def __init__(self, parsed_command: Dict[str, Any]):
        self.parsed = parsed_command
        
    def generate_code(self) -> str:
        """Generate Context framework code from parsed curl command."""
        code_parts = [
            self._generate_headers(),
            self._generate_cookies(),
            self._generate_request()
        ]
        
        return '\n\n'.join([p for p in code_parts if p])

    def _generate_headers(self) -> str:
        """Generate code for headers setup."""
        if not self.parsed.get('headers'):
            return ''
            
        headers = json.dumps(self.parsed['headers'], indent=4)
        return f'self.context.headers.update({headers})'

    def _generate_cookies(self) -> str:
        """Generate code for cookies setup."""
        if not self.parsed.get('cookies'):
            return ''
            
        cookies = json.dumps(self.parsed['cookies'], indent=4)
        return f'self.context.cookies.update({cookies})'

    def _generate_request(self) -> str:
        """Generate the actual request code."""
        url = self.parsed['url']
        method = self.parsed['method'].upper()
        
        if not self.parsed.get('data'):
            return f'response = self.context.{method}("{url}")'
            
        data = json.dumps(self.parsed['data'], indent=4)
        data_type = 'json' if self.parsed['data_as_json'] else 'data'
        
        return f'response = self.context.{method}("{url}", {data_type}={data})'
