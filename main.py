import ftplib
import sys
import os
from pathlib import Path
from gi.repository import GLib
from termcolor import colored
import shutil
downloads = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
localfile = None
pbar = None
def grabFile(filename):
  global localfile, pbar
  widgets = ['Downloading: ', Percentage(),Bar(marker='#',left='[',right=']'),' ' , ETA(), ' ', FileTransferSpeed()]
  pbar = ProgressBar(widgets=widgets, maxval=ftp.size(filename))
  pbar.start() 
  localfile = open(f"{downloads}/{filename}", 'wb')
  def file_write(data):
    global localfile, pbar
    localfile.write(data)
    pbar += len(data)
  try:
    ftp.retrbinary('RETR ' + filename, file_write, 1024)
  except:
    print("Download FAILED")
  localfile.close()


host = sys.argv[1]
pwd = "/"
if len(sys.argv) < 2:
  print("FTP needs (1) argument, the URL to connect to!")
  exit()
if  len(sys.argv) ==  4:
  uname = sys.argv[2]
  passwd = sys.argv[3]
else:
  uname = "anonymous"
  passwd = ""
print(f"Connecting to {host} as {uname}...")
ftp = ftplib.FTP_TLS(host)
ftp.sendcmd(f"USER {uname}")
ftp.sendcmd(f"PASS {passwd}")
print(ftp.getwelcome())
while True:
  try:
    command = input(f"{uname}@{host}[{pwd}] ")
  except EOFError or KeyboardInterrupt:
    ftp.quit()
    print()
    break
  command = command.split(' ')
  if command[0] == "exit":
    ftp.quit()
    break
  elif command[0] == "ls":

    ftp.dir() 
  elif command[0] == "cd":
    try: 
      ftp.cwd(command[1])
    except ftplib.error_perm as err:
     e = str(err).split(' ')
     http = e[0]
     if http == '550':
      print(f"{command[1]}: no such file or directory")
    pwd = ftp.pwd()
  elif command[0] == 'grab':
    if len(command) < 2:
      continue
    try:
      grabFile(command[1])
    except ftplib.error_perm as err:
      e = str(err)
      print(e)
      if e.startswith('550'):
        print(f"Could not grab \"{command[1]}\" from server: No such file or directory (* does not work)")
        continue
  elif command[0] == 'help':
    print('exit: Close the FTP session\nls: list files in the present working directory\ncd: change to the specified directory\ngrab: download the specified file to the Downloads folder')
  elif command[0] == 'find':
    files = []
    found = []
    ftp.dir(files.append)
    search = []
    for item in files:
      search.append(item)
      if command[1] in item:
        found.append(item)
    if len(found) < 1:
      print(f"{command[1]}: no such file or directory")
      continue
    for item in found:
      item = item.split(command[1])
      print(item[0] + colored(command[1],'red') + item[1])
  else:
    print(f"{command[0]}: command not found")
