from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from tkinter import messagebox as mbox
import ntpath
import os
import pickle
import time;
import tkinter as tk
import zipfile



os.system("cls")
tk=tk.Tk()
tk.withdraw()
a=mbox.askquestion("Backup","Are you sure you wan't to create backup",icon="warning",default="no")
if (a=="no"):
	quit()



print(">ZIPPING<".center(60,"="))
st=time.time()
zf=zipfile.ZipFile("backup.zip","w",zipfile.ZIP_DEFLATED)
for r,d,fl in os.walk("C:\\K"):
	for f in fl:
		if ("__pycache__" in os.path.join(r,f)):
			print(f"SKIPPING CACHE:\t{os.path.join(r,f)}")
			continue
		s=str(os.stat(os.path.join(r,f)).st_size)
		c=0
		for i in range(len(s)-1,0,-1):
			c+=1
			if (c==3):
				c=0
				s=s[:i]+" "+s[i:]
		lpad=" "*(len(f"Zipping:    (s={s} B, t={int((time.time()-st)*100)/100})    ")+4)
		log=f"Zipping:    (s={s} B, t={int((time.time()-st)*100)/100})    {os.path.join(r,f)}"
		i=0
		sz=0
		while (i<len(log)):
			sz+=1
			if (sz==100):
				sz=0
				log=log[:i]+"\n"+lpad+log[i:]
				i+=1+len(lpad)
			i+=1
		print(log)
		zf.write(os.path.join(r,f))
zf.close()
s=str(os.stat("./backup.zip").st_size)
c=0
for i in range(len(s)-1,0,-1):
	c+=1
	if (c==3):
		c=0
		s=s[:i]+" "+s[i:]
print("Zipping finished in %.2f%%s (zip_size=%i B)"%(time.time()-st,s))



cdata=None
if (ntpath.exists("token.pickle")):
	with open("token.pickle","rb") as t:
		cdata=pickle.load(t)
if (not cdata or not cdata.valid):
	if (cdata and cdata.expired and cdata.refresh_token):
		cdata.refresh(Request())
	else:
		flw=InstalledAppFlow.from_client_secrets_file("creds.json",["https://www.googleapis.com/auth/drive"])
		cdata=flw.run_local_server(port=0)
	with open("token.pickle","wb") as t:
		pickle.dump(cdata,t)
req=build("drive","v2",credentials=cdata).files().insert(body={"title":"Backup.zip","description":"Backup","mimetype":"application/octet-stream"},media_body=MediaFileUpload("backup.zip",mimetype="application/octet-stream",chunksize=524288,resumable=True))
resp=None
st=time.time()
print(">UPLOADING<".center(60,"="))
while (resp is None):
	s,resp=req.next_chunk()
	if s:
		print("%.2f%% complete...\t(t=%.2f)"%(s.progress()*100,time.time()-st))
