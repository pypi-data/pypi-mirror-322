### Dabih Python Package

A CLI Tool to interact with the dabih API

#### Installation

After cloning this library, you can install the dabih python package via: 

```bash
pip install -e .
```

#### Set Up Guide

Create a folder named dabih at either ~/.config (create ~/.config if necessary) or at your default XDG_CONFIG_HOME location. In the dabih folder, create a config.yaml file with the following format:

```yaml
base_url: "http://localhost:3000/api/v1"
token: "your token"
```

Save any dabih private keys (.pem files) in that dabih folder as well. The .pem files should have 'dabih' at some point in their file name or they won't be recognised as dabih private keys.

After completing the setup, run: 
```bash
dabih check
```
to test for URL, token and key-files being valid.

#### Example usage: 

To see all available commands and options:
```bash
dabih
```
Example for uploading or downloading a file:
```bash
dabih upload <filename> <target_folder_mnemonic>
dabih upload <filename>
dabih download <mnemonic>
```

For debugging, use -v:
```bash
dabih -v token-info
```