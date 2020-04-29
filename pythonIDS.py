__author__ = "Devashish Gaikwad"
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Devashish Gaikwad"
__email__ = "ishay.gaikwad@gmail.com"
__status__ = "Production"

import os, subprocess
import pyinotify
import queue
import logging
import logging.config
import pandas as pd
from datetime import datetime
import argparse

import notify_me
import sendmail

logging.config.fileConfig('logging.conf')



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=
    """
        PythonHostIDS is a simple host based IDS which detects 
        any accesses or modification to the contents of the given folder,
        then saves those change events into log and csv reports and
        sends an email using SendGrid API to given email addresses
        using SENDGRID_API_KEY set in the environment.                        
    """
    )
    parser.add_argument("-w", "--watch", help="The file or folder to monitor of intrusion detection", required=True)
    parser.add_argument("-c", "--reports", help="Folder in which the csv reports should be saved", required=True)
    parser.add_argument("-s", "--sender", help="Email address of the sender", required=True)
    parser.add_argument("-r", "--recvr", help="Email address of the receiver or a .txt file name, which contains the email addresses of receivers (each on new line)", required=True)

    args = parser.parse_args()
    
    watch_this = args.watch
    reportDir = args.reports
    sender = args.sender

    if args.recvr[-4:] == ".txt":
        with open(args.recvr, "r") as f:
            recvrs = f.readlines()
            recvrs = [x.strip() for x in recvrs]
    else:
        recvrs = [args.recvr]

    sendgridapi = os.environ.get('SENDGRID_API_KEY') ##Make sure SENDGRID_API_KEY is set in the bash environment
    if sendgridapi is None:
        logging.error("SENDGRID_API_KEY is not set! Exiting")
        exit(1)


    subject = "Intruder Alert! {} has been accessed or modified! on {} at ".format(watch_this, os.uname()[1])

    reportDir = os.path.abspath(reportDir)
    watch_this = os.path.abspath(watch_this)


    q = queue.Queue()
    mail = sendmail.sendmail(sender, sendgridapi)
    watch_manager = pyinotify.WatchManager()
    event_processor = notify_me.EventProcessor(eventq=q)
    event_notifier = pyinotify.ThreadedNotifier(watch_manager, event_processor)
    watch_manager.add_watch(watch_this, pyinotify.ALL_EVENTS)
    event_notifier.start()
    logging.info("Watch Created")


    msgs = []
    while True:
        msgs = []
        if not q.empty():
            logging.info("Received Updates")
            try:
                while True:
                    msgs.append(q.get(True, 2))
            except Exception as E:
                df = pd.DataFrame(msgs)
                dateiso = datetime.now().isoformat("-")
                reportname0 = "report-" + dateiso + ".csv"
                reportname = os.path.join(reportDir, reportname0)
                df.to_csv(reportname)
                logging.info("{} saved".format(reportname))
                sub = subject + dateiso
                cont = sub
                try:
                    statuscode = mail.sendfile(to=recvrs, subject=sub, content=cont, filename=reportname)
                    if statuscode == 202:
                        logging.info("Email sent Succesfully")
                    else:
                        logging.error("Email Error code: {}".format(statuscode))
                except Exception as e:
                    logging.error("Email Error: {}".format(e))
    pass