#!python
#
#	import
#
import sys
import os
import time
import re
import getopt
#
#	main function
#
def deleteFile(fname, eflag):
	if os.path.isdir(fname) == True: 
		sumn = 0
		sumsz = 0
		try:
			files = os.listdir(fname)
		except PermissionError as err:
			if eflag and not sflag:
				print("Permission Error: ",err)
			files = []
		for file in files:
			(n, sz) = deleteFile(os.path.join(fname, file), eflag)
			sumn += n
			sumsz += sz
		try:
			os.rmdir(fname)
			if not sflag:
				print("rmdir: {0}".format(os.path.basename(fname)))
		except OSError as err:
			if eflag and not sflag:
				print("OSError: ",err)
		return (sumn, sumsz)
	elif os.path.isfile(fname) == True:
		n = 1
		sz = os.path.getsize(fname)
		try:
			os.remove(fname)
			if not sflag:
				print("remove: {0} ({1:,d} bytes)".format(os.path.basename(fname), sz))
		except PermissionError as err:
			if eflag and not sflag:
				print("Permission Error: ",err)
			n = 0
			sz = 0
		return (n, sz)
	else:
		if eflag and not sflag:
			print("not exist: {0}".format(os.path.basename(fname)))
		return (0,0)
#
#	usage
#
def usage():
	print(
		"deltmp copyright (c)2016 made by mohmongar\n"
		"usage deltmp [option]\n"
		"-e or --err          ... error disp mode.\n"
		"-w num or --wait num ... wait num second after command.\n"
		"-s                   ... silent mode.\n"
	)
	sys.exit()
#
#	parameter
#
paths = [
	r"%windir%\temp", 
	r"%USERPROFILE%\AppData\Local\Microsoft\Windows\INetCache",
	r"%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Cache",
	r"%USERPROFILE%\AppData\Local\Temp"
	]
eflag = False
wait = 0.0
sflag = False
#
#	command line
#
try:
	opts,argv = getopt.getopt(sys.argv[1:], "ew:s",["err", "wait=","silent"])
except getopt.GetoptError:
	usage()
#
#	analyze option
#
for opt,para in opts:
	if opt in ('-e', '--err'):
		eflag = True
		if not sflag:
			print("error disp on")
	if opt in ('-w', '--wait'):
		wait = float(para)
		if not sflag:
			print("wait={0}".format(wait))
	if opt in ('-s', '--silent'):
		sflag = True;
#
#	main loop
#
sumn = 0
sumsz = 0
for path in paths:
	m = re.finditer('%(\w+)%', path)
	for env in m:
		nam = env.group(1)
		val = os.getenv(nam)
		if val != "":
			path = path.replace("%"+nam+"%", val)
		else:
			if eflag and not sflag:
				print("Not set enviroment var : {0}", nam)
	if not sflag:
		print("[{0}]".format(path))
	if os.path.isdir(path) == True:
		try:
			files = os.listdir(path)
		except PermissionError as err:
			files = []
			if eflag and not sflag:
				print("Permission Error: ",err)
		for file in files:
			(n, sz)= deleteFile(os.path.join(path, file), eflag)
			sumn += n
			sumsz +=sz 
if not sflag:
	print("Deleted {0} files ({1:,d} bytes)".format(sumn, sumsz))
if wait>0.0 :
	time.sleep(wait)
#
