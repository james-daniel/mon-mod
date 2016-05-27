#!/usr/bin/python3

# Monitor modifications to FS and email logs for diagnosis.
# For legal purposes only!

try:
    import smtplib
    import os.path
    import sys
    import time
    import logging
    import subprocess
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Caught ImportError")

# def lock_sysctlConf():
#     if os.path.isfile("/etc/sysctl.conf"):
#         subprocess.call(['chmod'],['000'],['/etc/sysctl.conf'])
#         subprocess.call(['chattr'],['-i'],['/etc/sysctl.conf'])
#     else:
#         raise StandardError
#
# def lock_sysctlD():
#     if os.path.isfile("/etc/sysctl.d"):
#         subprocess.call(['chmod'],['-R'],['000'],['/etc/sysctl.d'])
#         subprocess.call(['chattr'],['-R'], ['i'],['/etc/sysctl.d'])
#     else:
#         raise StandardError
#
# def modprobeConf():
#     if os.path.isfile("/bin/kmod"):
#         subprocess.call(['mv'],['/bin/kmod'],['/bin/paramiko'])
#     else:
#         raise StandardError

class jd_fs_evt_handler(FileSystemEventHandler):
    def __init__(self, observer, fileName):
        self.observer = observer
        self.filename = fileName
    # Overriding on_created
    def on_created(self, event):
        sendMail()
        # self.observer.stop()

def pollSys():
    path = '<PATH>'
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    # evt_handler = LoggingEventHandler()
    obs = Observer()
    fs_evt_handler = jd_fs_evt_handler(obs, path)
    obs.schedule(fs_evt_handler, path, recursive=True)
    obs.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     obs.stop()
    obs.join()

def sendMail():
    receiver_email = '<EMAIL>'
    sender_email = '<EMAIL>'
    sender_password = '<PASS>'
    smtp_srv = smtplib.SMTP("<SMTP_SERVER_FQDN>", 587)
    smtp_srv.ehlo()
    smtp_srv.starttls()
    smtp_srv.ehlo()
    smtp_srv.login(sender_email,sender_password)
    # Send files
    p = subprocess.Popen(['<BASH>'])
    p2 = subprocess.Popen(['<BASH>'])
    p3 = subprocess.Popen(['<BASH>'])
    output = p.stdout.read()
    output2 = p2.stdout.read()
    output3 = p3.stdout.read()
    header = 'To: ' + receiver_email + '\n' + 'From: ' + sender_email + '\n'
    + 'Subject: <SUBJECT>\n'
    message = header + '\n ' + output + '\n\n' + output2 + '\n\n' + output3
    smtp_srv.sendmail(sender_email, receiver_email, message)
    smtp_srv.close()

if __name__=='__main__':
    pollSys()