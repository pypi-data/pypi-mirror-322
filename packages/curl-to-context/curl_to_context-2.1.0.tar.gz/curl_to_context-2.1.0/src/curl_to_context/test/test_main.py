import pytest
import pyperclip
from typer.testing import CliRunner
from ..main import app
from ..lib.curl_parser import CurlParser

runner = CliRunner()

def test_convert_grab():
    curl_cmd = """curl 'https://api.example.com/data'"""
    pyperclip.copy(curl_cmd)
    
    result = runner.invoke(app, ["--framework", "grab"])
    assert result.exit_code == 0
    assert "has been copied to clipboard" in result.stdout

def test_convert_context():
    curl_cmd = """curl 'https://api.example.com/data'"""
    pyperclip.copy(curl_cmd)
    
    result = runner.invoke(app, ["--framework", "context"])
    assert result.exit_code == 0
    assert "has been copied to clipboard" in result.stdout

def test_show_output():
    curl_cmd = """curl 'https://api.example.com/data'"""
    pyperclip.copy(curl_cmd)
    
    result = runner.invoke(app, ["--framework", "grab", "--show"])
    assert result.exit_code == 0
    assert "self.g.go" in result.stdout

def test_invalid_curl():
    pyperclip.copy("not a curl command")
    
    result = runner.invoke(app, ["--framework", "grab"])
    assert result.exit_code == 1
    assert "Invalid curl command" in result.stdout

def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "curl-to-context version:" in result.stdout 