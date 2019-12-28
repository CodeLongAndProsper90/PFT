import ftplib
import sys
import os
try:
  os.mkdir('Downloads')
except FileExistsError:
  None
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
localfile = None
pbar = None
def grabFile(filename):
  global localfile, pbar
  widgets = ['Downloading: ', Percentage(), ' ',Bar(marker=">",left='[',right=']'),' ' , ETA(), ' ', FileTransferSpeed()]
  pbar = ProgressBar(widgets=widgets, maxval=ftp.size(filename))
  pbar.start() 
  localfile = open(f"Downloads/{filename}", 'wb')
  def file_write(data):
    global localfile, pbar
    localfile.write(data)
    pbar += len(data)


  ftp.retrbinary('RETR ' + filename, file_write, 1024)

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
print(f"Connecting to {host} as {uname}")
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
    print(f"Size of {command[1]} is {ftp.size(command[1])}")
    grabFile(command[1])
