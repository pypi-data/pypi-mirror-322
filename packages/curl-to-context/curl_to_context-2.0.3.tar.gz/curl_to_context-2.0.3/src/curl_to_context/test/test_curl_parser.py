import pytest
from ..lib.curl_parser import CurlParser

def test_parse_simple_get():
    curl = """curl 'https://api.example.com/data'"""
    result = CurlParser.parse_curl(curl)
    
    assert result['method'] == 'get'
    assert result['url'] == 'https://api.example.com/data'
    assert not result['data']
    assert not result['headers']
    assert not result['cookies']

def test_parse_with_headers():
    curl = """curl 'https://api.example.com/data' -H 'accept: application/json' -H 'user-agent: Mozilla/5.0'"""
    result = CurlParser.parse_curl(curl)
    
    assert result['headers'] == {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0'
    }

def test_parse_with_cookies():
    curl = """curl 'https://api.example.com/data' -H 'cookie: session=abc123; user=john'"""
    result = CurlParser.parse_curl(curl)
    
    assert result['cookies'] == {
        'session': 'abc123',
        'user': 'john'
    }

def test_parse_post_data():
    curl = """curl 'https://api.example.com/data' -d '{"key":"value"}'"""
    result = CurlParser.parse_curl(curl)
    
    assert result['method'] == 'post'
    assert result['data'] == {'key': 'value'}
    assert result['data_as_json'] == True

def test_invalid_curl():
    with pytest.raises(ValueError):
        CurlParser.parse_curl("not a curl command")
