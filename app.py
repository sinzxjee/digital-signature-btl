import tkinter as tk
from pathlib import Path
from tkinter import filedialog,messagebox,ttk
from signature_core import *
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Ứng dụng chữ ký số – BTL"); self.geometry("800x540"); self.a=tk.StringVar(value=RSA_PSS)
        root=ttk.Frame(self,padding=16); root.pack(fill="both",expand=True)
        ttk.Label(root,text="ỨNG DỤNG CHỮ KÝ SỐ",font=("Segoe UI",18,"bold")).pack()
        ttk.Label(root,text="Minh họa học tập – không thay thế chữ ký số được CA chứng thực").pack()
        bar=ttk.Frame(root); bar.pack(pady=8)
        ttk.Radiobutton(bar,text="RSA-PSS 3072",variable=self.a,value=RSA_PSS).pack(side="left",padx=12)
        ttk.Radiobutton(bar,text="ECDSA P-256",variable=self.a,value=ECDSA).pack(side="left",padx=12)
        book=ttk.Notebook(root); book.pack(fill="both",expand=True)
        self.k=ttk.Frame(book,padding=15); self.s=ttk.Frame(book,padding=15); self.v=ttk.Frame(book,padding=15)
        book.add(self.k,text="Sinh khóa"); book.add(self.s,text="Ký tệp"); book.add(self.v,text="Xác minh")
        self.folder=tk.StringVar(); self.kpw=tk.StringVar(); self.row(self.k,0,"Thư mục:",self.folder,lambda:self.folder.set(filedialog.askdirectory())); self.password(self.k,1,self.kpw); ttk.Button(self.k,text="Sinh cặp khóa",command=self.gen).grid(row=2,column=1,pady=15)
        self.f=tk.StringVar(); self.pr=tk.StringVar(); self.out=tk.StringVar(); self.spw=tk.StringVar()
        self.row(self.s,0,"Tệp cần ký:",self.f,lambda:self.pick(self.f)); self.row(self.s,1,"Khóa bí mật:",self.pr,lambda:self.pick(self.pr)); self.row(self.s,2,"Tệp chữ ký:",self.out,self.save); self.password(self.s,3,self.spw); ttk.Button(self.s,text="Ký tệp",command=self.sign).grid(row=4,column=1,pady=15)
        self.vf=tk.StringVar(); self.pu=tk.StringVar(); self.sig=tk.StringVar()
        self.row(self.v,0,"Tệp gốc:",self.vf,lambda:self.pick(self.vf)); self.row(self.v,1,"Khóa công khai:",self.pu,lambda:self.pick(self.pu)); self.row(self.v,2,"Tệp chữ ký:",self.sig,lambda:self.pick(self.sig)); ttk.Button(self.v,text="Xác minh",command=self.verify).grid(row=3,column=1,pady=15)
    def row(self,p,i,t,v,c):
        ttk.Label(p,text=t).grid(row=i,column=0,sticky="w",pady=7); ttk.Entry(p,textvariable=v).grid(row=i,column=1,sticky="ew",padx=8); ttk.Button(p,text="Chọn…",command=c).grid(row=i,column=2); p.columnconfigure(1,weight=1)
    def password(self,p,i,v):
        ttk.Label(p,text="Mật khẩu:").grid(row=i,column=0); ttk.Entry(p,textvariable=v,show="•").grid(row=i,column=1,sticky="ew",padx=8)
    def pick(self,v):
        x=filedialog.askopenfilename(); v.set(x or v.get())
    def save(self):
        x=filedialog.asksaveasfilename(defaultextension=".sig.json"); self.out.set(x or self.out.get())
    def gen(self):
        try:
            d=Path(self.folder.get()); d.mkdir(parents=True,exist_ok=True); n="rsa" if self.a.get()==RSA_PSS else "ecdsa"; generate_key_pair(self.a.get(),d/f"{n}_private.pem",d/f"{n}_public.pem",self.kpw.get()); messagebox.showinfo("Thành công","Đã tạo cặp khóa.")
        except Exception as e: messagebox.showerror("Lỗi",str(e))
    def sign(self):
        try: sign_file(self.f.get(),self.pr.get(),self.spw.get(),self.a.get(),self.out.get()); messagebox.showinfo("Thành công","Đã lưu chữ ký rời.")
        except Exception as e: messagebox.showerror("Lỗi",str(e))
    def verify(self):
        try:
            ok,msg,_=verify_file(self.vf.get(),self.pu.get(),self.sig.get()); (messagebox.showinfo if ok else messagebox.showwarning)("Kết quả",msg)
        except Exception as e: messagebox.showerror("Lỗi",str(e))
if __name__=="__main__": App().mainloop()
