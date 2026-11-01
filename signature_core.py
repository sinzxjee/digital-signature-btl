

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

RSA_PSS = "RSA-PSS-SHA256"
ECDSA = "ECDSA-P256-SHA256"
SIGNATURE_FORMAT = "BTL-DIGITAL-SIGNATURE-1"


def _require_existing_file(path: str | Path, description: str) -> Path:
    resolved = Path(path)
    if not resolved.is_file():
        raise ValueError(f"Không tìm thấy {description}: {resolved}")
    return resolved


def generate_key_pair(algorithm, private_key_path, public_key_path, password):
    """Sinh cặp khóa và lưu khóa bí mật được mã hóa bằng mật khẩu."""
    if not password:
        raise ValueError("Mật khẩu bảo vệ khóa bí mật không được để trống.")
    if algorithm == RSA_PSS:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    elif algorithm == ECDSA:
        private_key = ec.generate_private_key(ec.SECP256R1())
    else:
        raise ValueError("Thuật toán không được hỗ trợ.")

    private_path, public_path = Path(private_key_path), Path(public_key_path)
    private_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.parent.mkdir(parents=True, exist_ok=True)
    private_path.write_bytes(private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(password.encode("utf-8")),
    ))
    public_path.write_bytes(private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ))


def sign_file(file_path, private_key_path, password, algorithm, signature_path):
    """Ký một tệp và lưu chữ ký rời ở định dạng JSON."""
    source = _require_existing_file(file_path, "tệp cần ký")
    private_path = _require_existing_file(private_key_path, "khóa bí mật")
    if not password:
        raise ValueError("Mật khẩu khóa bí mật không được để trống.")
    data = source.read_bytes()
    private_key = serialization.load_pem_private_key(
        private_path.read_bytes(), password=password.encode("utf-8")
    )

    if algorithm == RSA_PSS:
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise ValueError("Khóa bí mật đã chọn không phải khóa RSA.")
        signature = private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32),
            hashes.SHA256(),
        )
    elif algorithm == ECDSA:
        if not isinstance(private_key, ec.EllipticCurvePrivateKey):
            raise ValueError("Khóa bí mật đã chọn không phải khóa ECDSA.")
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
    else:
        raise ValueError("Thuật toán không được hỗ trợ.")

    package = {
        "format": SIGNATURE_FORMAT,
        "algorithm": algorithm,
        "hash": "SHA-256",
        "file_name": source.name,
        "file_size": len(data),
        "file_sha256": hashlib.sha256(data).hexdigest(),
        "signed_at_utc": datetime.now(timezone.utc).isoformat(),
        "signature_base64": base64.b64encode(signature).decode("ascii"),
    }
    output = Path(signature_path)
    if not output.name:
        raise ValueError("Chưa chọn nơi lưu tệp chữ ký.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    return package


def verify_file(file_path, public_key_path, signature_path):
    """Xác minh chữ ký và tính toàn vẹn của tệp."""
    source = _require_existing_file(file_path, "tệp cần xác minh")
    public_path = _require_existing_file(public_key_path, "khóa công khai")
    signature_file = _require_existing_file(signature_path, "tệp chữ ký")
    try:
        package = json.loads(signature_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Tệp chữ ký không phải JSON hợp lệ.") from exc

    required = {"format", "algorithm", "hash", "file_sha256", "signature_base64"}
    if not isinstance(package, dict) or not required.issubset(package):
        return False, "Tệp chữ ký thiếu trường dữ liệu bắt buộc.", package
    if package["format"] != SIGNATURE_FORMAT:
        return False, "Phiên bản định dạng chữ ký không được hỗ trợ.", package
    if package["hash"] != "SHA-256":
        return False, "Hàm băm trong tệp chữ ký không được hỗ trợ.", package

    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != package["file_sha256"]:
        return False, "Tệp đã thay đổi: SHA-256 không khớp.", package

    try:
        signature = base64.b64decode(package["signature_base64"], validate=True)
        public_key = serialization.load_pem_public_key(public_path.read_bytes())
        if package["algorithm"] == RSA_PSS:
            if not isinstance(public_key, rsa.RSAPublicKey):
                return False, "Khóa công khai không phải khóa RSA.", package
            public_key.verify(
                signature, data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32),
                hashes.SHA256(),
            )
        elif package["algorithm"] == ECDSA:
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                return False, "Khóa công khai không phải khóa ECDSA.", package
            public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        else:
            return False, "Thuật toán trong tệp chữ ký không được hỗ trợ.", package
    except (InvalidSignature, ValueError, TypeError, binascii.Error):
        return False, "Chữ ký sai hoặc khóa công khai không tương ứng.", package
    return True, "Chữ ký hợp lệ; tệp còn nguyên vẹn.", package
