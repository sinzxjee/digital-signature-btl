import base64, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
RSA_PSS="RSA-PSS-SHA256"; ECDSA="ECDSA-P256-SHA256"
def generate_key_pair(a,pr,pu,pw):
    if not pw: raise ValueError("Mật khẩu không được để trống.")
    if a==RSA_PSS: k=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    elif a==ECDSA: k=ec.generate_private_key(ec.SECP256R1())
    else: raise ValueError("Thuật toán không hỗ trợ.")
    Path(pr).write_bytes(k.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.BestAvailableEncryption(pw.encode())))
    Path(pu).write_bytes(k.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
def sign_file(f,pr,pw,a,out):
    d=Path(f).read_bytes(); k=serialization.load_pem_private_key(Path(pr).read_bytes(),password=pw.encode())
    if a==RSA_PSS: s=k.sign(d,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=32),hashes.SHA256())
    elif a==ECDSA: s=k.sign(d,ec.ECDSA(hashes.SHA256()))
    else: raise ValueError("Thuật toán không hỗ trợ.")
    p={"format":"BTL-DIGITAL-SIGNATURE-1","algorithm":a,"hash":"SHA-256","file_name":Path(f).name,"file_size":len(d),"file_sha256":hashlib.sha256(d).hexdigest(),"signed_at_utc":datetime.now(timezone.utc).isoformat(),"signature_base64":base64.b64encode(s).decode()}
    Path(out).write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8"); return p
def verify_file(f,pu,sf):
    d=Path(f).read_bytes(); p=json.loads(Path(sf).read_text(encoding="utf-8"))
    if hashlib.sha256(d).hexdigest()!=p.get("file_sha256"): return False,"Tệp đã thay đổi: SHA-256 không khớp.",p
    try:
        s=base64.b64decode(p["signature_base64"],validate=True); k=serialization.load_pem_public_key(Path(pu).read_bytes())
        if p["algorithm"]==RSA_PSS: k.verify(s,d,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=32),hashes.SHA256())
        elif p["algorithm"]==ECDSA: k.verify(s,d,ec.ECDSA(hashes.SHA256()))
        else: return False,"Thuật toán không hỗ trợ.",p
    except (InvalidSignature,ValueError,KeyError,TypeError): return False,"Chữ ký sai hoặc khóa không tương ứng.",p
    return True,"Chữ ký hợp lệ; tệp còn nguyên vẹn.",p
