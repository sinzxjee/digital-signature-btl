import tempfile, unittest
from pathlib import Path
from signature_core import *
class Tests(unittest.TestCase):
    def check(self,a):
        with tempfile.TemporaryDirectory() as x:
            d=Path(x); f=d/"a.txt"; f.write_text("Dữ liệu",encoding="utf-8")
            generate_key_pair(a,d/"pr.pem",d/"pu.pem","123456"); sign_file(f,d/"pr.pem","123456",a,d/"a.sig.json")
            self.assertTrue(verify_file(f,d/"pu.pem",d/"a.sig.json")[0])
            f.write_text("Đã sửa",encoding="utf-8"); self.assertFalse(verify_file(f,d/"pu.pem",d/"a.sig.json")[0])
    def test_rsa(self): self.check(RSA_PSS)
    def test_ecdsa(self): self.check(ECDSA)
if __name__=="__main__": unittest.main()
