import sys
import paramiko
import pysftp as sftp
import subprocess
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import threading, time

while True:

    def main():
        FTP_HOST = "1.vps.com"
        FTP_USER = "user"
        FTP_PASS = "pass"
        FTP_PORT = int("0000")
        remote_conf = r'/home/.env'
        local_conf = r'./config/.env'
        remote_stat = r'/home/stat.csv'
        local_stat = r'./stat.csv'
        opnstat = 'stat.csv'
        log_file = "log.txt"

        folder = os.path.dirname(os.path.abspath(__file__))
        conf_folder = "config\.env"
        cf2 = os.path.join(folder, conf_folder)

        cnopts = sftp.CnOpts()
        cnopts.hostkeys = None

        open('log.txt', 'w').close()

        # -------------- ENV CONTROL------------------

        def upload():
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
                sftp = ssh.open_sftp()
                sftp.put(local_conf, remote_conf)
                with open(log_file, "a") as f:
                    print("Config file upload success<br>", file=f)
                print("config upload success")
            except:
                print("config upload failed")
                with open(log_file, "a") as f:
                    print("<b>Config file upload failed<br></b>", file=f)

        def download():
            try:
                with paramiko.SSHClient() as ssh:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
                    with ssh.open_sftp() as sftp:
                        sftp.get(remote_conf, local_conf)
                with open(log_file, "a") as f:
                    print("Config file download success<br>", file=f)
                print("config download success")
            except:
                print("config download failed")
                with open(log_file, "a") as f:
                    print("<b>Config file download failed<br></b>", file=f)

        def open_folder():
            with open(log_file, "a") as f:
                print("<br>Config folder opening...<br>Use any available text editor for file configuration<br>"
                      "<b>Check out: the .ENV is an extension<br></b><br>", file=f)
            subprocess.Popen(f'explorer /select, "{cf2}"')

        # -------------- STAT CONTROL------------------

        def download_stat():
            try:
                with paramiko.SSHClient() as ssh:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
                    with ssh.open_sftp() as sftp:
                        sftp.get(remote_stat, local_stat)
                print("stat download success")
                with open(log_file, "a") as f:
                    print("Stat file updated <br>", file=f)
            except:
                print("stat download failed")
                with open(log_file, "a") as f:
                    print("<b>Stat file update failed<br></b>", file=f)

        def open_stat():
            print("\n\nCurrent server file: \n\n")
            print(open(local_conf, mode='r', buffering=-1,
                       encoding='utf-8', errors=None, newline=None, closefd=True, opener=None).read())
            print(local_stat)
            subprocess.Popen(f'{opnstat}', shell=True)

        # -------------- BOT CONTROL------------------

        def restart_bot():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
            ssh.exec_command("systemctl restart ")
            print("Restarting bot")
            with open(log_file, "a") as f:
                print("Bot Reloading...<br>", file=f)

        def stop_bot():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
            ssh.exec_command("systemctl stop ")
            print("Stop bot")
            with open(log_file, "a") as f:
                print("Bot Stopped<br>", file=f)

        def start_bot():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=FTP_HOST, username=FTP_USER, password=FTP_PASS, port=FTP_PORT)
            ssh.exec_command("systemctl start")
            print("Start bot")
            with open(log_file, "a") as f:
                print("Start Bot<br>", file=f)

        # -------------- APPLICATION------------------

        Form, Window = uic.loadUiType("bot-control.ui")
        app = QApplication([])
        window, form = Window(), Form()
        form.setupUi(window)
        window.show()

        form.dwnld.clicked.connect(download)
        form.upld.clicked.connect(upload)
        form.opnfldr.clicked.connect(open_folder)

        form.updtstat.clicked.connect(download_stat)
        form.vwstat.clicked.connect(open_stat)

        form.strtbt.clicked.connect(start_bot)
        form.stpbt.clicked.connect(stop_bot)
        form.rstrtbt.clicked.connect(restart_bot)

        form.extui.clicked.connect(sys.exit)

        def updtxt(n=2):
            while True:
                form.reload.clicked.emit()
                time.sleep(n)

        thread = threading.Thread(target=updtxt, daemon=True)
        thread.start()

        app.exec()


    if __name__ == "__main__":
        main()
