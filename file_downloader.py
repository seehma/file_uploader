from ftplib import FTP_TLS, error_perm
import os
import time
import logging

# Konfiguration des Loggings
logging.basicConfig(filename='ftp_download_log.txt', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

def download_and_delete_latest_file(ftp_host, ftp_user, ftp_password, remote_folder, local_folder, file_extension='.DDD'):
    try:
        while True:
            with FTP_TLS() as ftp:
                ftp.connect(ftp_host)
                ftp.login(ftp_user, ftp_password)
                ftp.prot_p()  # Aktiviere SSL/TLS für Datenkanal

                # Liste der Dateien im Verzeichnis abrufen
                file_list = ftp.nlst(remote_folder)

                # Filtere Dateien nach der gewünschten Endung
                filtered_files = [file for file in file_list if file.lower().endswith(file_extension.lower())]

                if not filtered_files:
                    logging.info(f"Keine Dateien mit der Endung '{file_extension}' mehr auf dem Server. Das Skript wird beendet.")
                    print(f"Keine Dateien mit der Endung '{file_extension}' mehr auf dem Server. Das Skript wird beendet.")
                    break

                # Neueste Datei auswählen (basierend auf dem letzten Änderungsdatum)
                latest_file = max(filtered_files, key=lambda file: ftp.voidcmd(f"MDTM {file}")[4:].strip())

                # Lokale und entfernte Pfade erstellen
                local_path = os.path.join(local_folder, os.path.basename(latest_file))
                remote_path = os.path.join(remote_folder, latest_file)

                # Datei herunterladen
                with open(local_path, 'wb') as file:
                    ftp.retrbinary(f'RETR {remote_path}', file.write)
                    logging.info(f"Datei von {remote_path} wurde erfolgreich heruntergeladen.")
                    print(f"Datei von {remote_path} wurde erfolgreich heruntergeladen.")

                # Lösche die Datei auf dem Server nur, wenn der Download erfolgreich war
                try:
                    ftp.delete(remote_path)
                    logging.info(f"Datei von {remote_path} wurde erfolgreich heruntergeladen und auf dem Server gelöscht.")
                    print(f"Datei von {remote_path} wurde erfolgreich heruntergeladen und auf dem Server gelöscht.")
                except error_perm as e:
                    logging.warning(f"Datei konnte nicht gelöscht werden: {str(e)}")
                    print(f"Datei konnte nicht gelöscht werden: {str(e)}")
                
            time.sleep(1)  # Wartezeit, um die Schleife nicht zu intensiv zu machen

    except Exception as e:
        logging.error(f"Fehler beim Herunterladen: {str(e)}")
        print(f"Fehler beim Herunterladen: {str(e)}")
    finally:
        logging.info("Das Skript wurde abgeschlossen.")
        print("Fertig. Das Skript wurde abgeschlossen.")

if __name__ == "__main__":
    ftp_host = 'serverhost'
    ftp_user = 'username'
    ftp_password = 'password'    
    remote_folder = ''
    local_folder = 'C:\downloadedfiles'

    download_and_delete_latest_file(ftp_host, ftp_user, ftp_password, remote_folder, local_folder, file_extension='.DDD')