# PythonHostIDS
PythonHostIDS is a simple host based IDS which detects any accesses or modification to the contents of the given folder, then saves those change events into log and csv reports and sends an email using SendGrid API to given email addresses using SENDGRID_API_KEY set in the environment.   

**Make sure that You have set up a free SendGrid account and have a SENDGRID_API_KEY set into the environment**

`export SENDGRID_API_KEY = "API_key_from_sendgrid"`

## Usage

```
usage: pythonIDS.py [-h] -w WATCH -c REPORTS -s SENDER -r RECVR

PythonHostIDS is a simple host based Intrusion Detection System which detects any accesses or
modification to the contents of the given folder, then saves those change
events into log and csv reports and sends an email using SendGrid API to given
email addresses using SENDGRID_API_KEY set in the environment.

optional arguments:
  -h, --help            show this help message and exit
  -w WATCH, --watch WATCH
                        The file or folder to monitor of intrusion detection
  -c REPORTS, --reports REPORTS
                        Folder in which the csv reports should be saved
  -s SENDER, --sender SENDER
                        Email address of the sender
  -r RECVR, --recvr RECVR
                        Email address of the receiver or a .txt file name,
                        which contains the email addresses of receivers (each
                        on new line)

```
