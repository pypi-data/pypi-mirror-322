from dabih.dabih_client.dabih_api_client.api.download import download_chunk
from .filesystem import get_file_info
from .crypto import b64, decrypt, hash
from ..logger import dbg, warn, log, error
from .util import check_status
from cryptography.hazmat.primitives import serialization
import sys

__all__ = ["find_key", "download_func"]


def find_key(key_list, pem_files):
    dbg("Finding private key...")
    dbg(f"key_list: {key_list}")
    for key in key_list:
        dbg(f"pem_list: {pem_files}")
        for pem_file in pem_files:
            try:
                with open(pem_file, "rb") as pem_file:
                    private_key = serialization.load_pem_private_key(
                        pem_file.read(),
                        password=None 
                    )
                    pem_hash = hash.get_key_hash(private_key)
            except (ValueError, TypeError) as e:
                warn(f"Error loading this PEM file {pem_file}. Using another key if available...")
                continue
                
            if key["hash"] == pem_hash:
                log("Found valid key")
                return private_key, key
            else:
                dbg(f"pem_hash: {pem_hash}")
                dbg(f"key_hash: {key['hash']}")

    warn("No valid key found")
    return None


def download_func(mnemonic, client, pem_files):
    log(f"Starting download for mnemonic: {mnemonic}")
    file, uid, key_list, size = get_file_info(mnemonic, client)
    if not pem_files:
        error("No valid key files found. You need your private key to download files. \nDownload aborted.")
        sys.exit(0)
    private_key, public_key = find_key(key_list, pem_files)
    
    if not private_key:
        error("No private key  found for requested file. Please check your key files.")
        sys.exit(0)

    encrypted_aes_key = public_key["key"]
    aes_key = decrypt.decrypt_aes_key(encrypted_aes_key, private_key)

    start = 0
    size = float(size)

    with open(file["fileName"], "wb") as f:
        log("Downloading... 0%")
        for chunk in file["chunks"]:

            chunk_hash = chunk["hash"]
            chunk_response = download_chunk.sync_detailed(uid=uid, hash_=chunk_hash, client=client)
            check_status(chunk_response)
            encrypted_chunk = chunk_response.content
            n = len(encrypted_chunk)

            iv = b64.decode(chunk["iv"])
            decrypted_chunk = decrypt.decrypt_file_chunk(encrypted_chunk, aes_key, iv)
        
            f.write(decrypted_chunk)

            last_percent = (start * 100) // size
            start += n
            percent = (start * 100) // size
            if percent != last_percent:
                print(f"{percent}%", end=" \n")
                sys.stdout.flush()

    log("Download finished.")