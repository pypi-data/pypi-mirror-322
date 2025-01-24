import pytest
from click.testing import CliRunner
from dabih.main import main
from dabih.config import get_client
import dabih.config

@pytest.fixture
def runner():
    return CliRunner()

# def test_token_invalid(runner, monkeypatch):
#     original_get_client = get_client
#     def mock_get_client():
#         client, pem_files = original_get_client()
#         client.token = 'kjhbdfkahs'
#         return client, pem_files
#     monkeypatch.setattr('dabih.config.get_client', mock_get_client)

#     result = runner.invoke(main, ['token-val'])
#     print(result.output)
#     assert 'Token is not valid' in result.output

# def test_invalid_base_url(runner, monkeypatch):
#     original_get_client = get_client
#     def mock_get_client():
#         client, pem_files = original_get_client()
#         client.base_url = 'http://invalid-url'
#         return client, pem_files
#     monkeypatch.setattr('dabih.config.get_client', mock_get_client)

#     result = runner.invoke(main, ['check'])
#     print(result.output)
#     assert 'Connection error: Please check the URL in config file or whether the server is running' in result.output


def test_upload_with_invalid_file(runner):
    result = runner.invoke(main, ['upload', 'non_existent_file.txt'])
    print(result.output)
    assert 'File at path: non_existent_file.txt not found. Please check the path.' in result.output

def test_upload_with_invalid_folder(runner):
    result = runner.invoke(main, ['upload', 'test.txt', 'invalid_folder_mnemonic'])
    print(result.output)
    assert 'Requested dabih file/folder not found: Inode invalid_folder_mnemonic not found.' in result.output

def test_download_with_invalid_mnemonic(runner):
    result = runner.invoke(main, ['download', 'invalid_mnemonic'])
    print(result.output)
    assert 'Requested dabih file/folder not found: No file found for mnemonic invalid_mnemonic.' in result.output
