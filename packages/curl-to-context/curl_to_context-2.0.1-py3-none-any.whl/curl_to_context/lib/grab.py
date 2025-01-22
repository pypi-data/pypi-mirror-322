from typing import Dict, Any
import json
from collections import OrderedDict

class GrabCodeWriter:
    """Generates Grab framework code from parsed curl commands."""
    
    COMMON_HEADERS = [
        'accept-encoding',
        'accept-language',
        'accept',
        'connection',
        'user-agent'
    ]

    def __init__(self, parsed_command: Dict[str, Any]):
        self.parsed = parsed_command
        
    def generate_code(self) -> str:
        """Generate Grab framework code from parsed curl command."""
        code_parts = [
            self._generate_headers(),
            self._generate_cookies(),
            self._generate_params(),
            self._generate_request()
        ]
        
        return '\n\n'.join([p for p in code_parts if p])

    def _generate_headers(self) -> str:
        """Generate code for headers setup."""
        if not self.parsed.get('headers'):
            return ''
            
        headers_dict = self._dict_to_python(
            self.parsed['headers'],
            'headers',
            mark_common=True
        )
        return f'self.g.setup({headers_dict})'

    def _generate_cookies(self) -> str:
        """Generate code for cookies setup."""
        if not self.parsed.get('cookies'):
            return ''
            
        cookies_dict = self._dict_to_python(
            self.parsed['cookies'],
            'cookies'
        )
        return f'self.g.setup({cookies_dict})'

    def _generate_params(self) -> str:
        """Generate code for request parameters."""
        if not self.parsed.get('data'):
            return ''
            
        params_name = f"{self.parsed['method']}_params"
        return self._dict_to_python(
            self.parsed['data'],
            params_name
        )

    def _generate_request(self) -> str:
        """Generate the actual request code."""
        url = self.parsed['url']
        method = self.parsed['method']
        
        if not self.parsed.get('data'):
            return f"self.g.go('{url}')"
            
        params_name = f"{method}_params"
        param_type = 'json' if self.parsed['data_as_json'] else 'post'
        
        if method == 'get':
            return f"self.g.go('{url}', params={params_name})"
        else:
            return f"self.g.go('{url}', {param_type}={params_name})"

    def _dict_to_python(self, data: Dict, var_name: str, mark_common: bool = False) -> str:
        """Convert dictionary to Python code string."""
        dict_str = json.dumps(data, indent=4)
        
        if mark_common:
            lines = []
            for line in dict_str.split('\n'):
                if any(h in line.lower() for h in self.COMMON_HEADERS):
                    line += ' # should not be necessary'
                lines.append(line)
            dict_str = '\n'.join(lines)
            
        return f"{var_name}={dict_str}"