import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ftplib import FTP_TLS

# Konfiguration des Loggings
logging.basicConfig(filename='ftp_upload_log.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        logging.info(f"Neue Datei erkannt: {file_path}")
        
        upload_file(file_path)
        move_file(file_path)

def upload_file(file_path):
    ftp_host = 'serverhost'
    ftp_user = 'username'
    ftp_password = 'password'
    
    with FTP_TLS() as ftp:
        ftp.connect(ftp_host)
        ftp.login(ftp_user, ftp_password)
        
        logging.info(f"Hochladen von Datei: {file_path}")
        
        with open(file_path, 'rb') as file:
            ftp.prot_p()
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)

def move_file(file_path):
    destination_folder = 'C:\monitoreddone'
    destination_path = os.path.join(destination_folder, os.path.basename(file_path))
    
    logging.info(f"Verschieben von Datei nach: {destination_path}")
    
    os.rename(file_path, destination_path)

def monitor_folder(folder_path):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitored_folder = 'C:\monitoredfolder'
    logging.info(f"Überwachung von Ordner gestartet: {monitored_folder}")
    monitor_folder(monitored_folder)