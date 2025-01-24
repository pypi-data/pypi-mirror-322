import requests
import rsp.common.console as console
import googledriver

class GoogleDrive():
    def download_file(url, save_filename):#, file_id = '1cMaGRmDjnx43fLHkYFif29BkXYZzmj23', destination = 'test.zip'):
        waitControl = console.WaitControl(f'Downloading file...')

        try:
            file_id = url.split('/')[5]

            # URL zum direkten Herunterladen
            url = f"https://drive.google.com/uc?export=download&id={file_id}"

            # HTTP-Session starten
            session = requests.Session()

            # Erste Anfrage senden, um Cookies zu setzen
            response = session.get(url, stream=True)
            # Überprüfen, ob eine Bestätigung erforderlich ist
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
                    response = session.get(url, stream=True)
                    break

            # Datei herunterladen und speichern
            with open(save_filename, "wb") as f:
                for chunk in response.iter_content(32768):  # In kleinen Blöcken schreiben
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            console.error(f'Download failed. Exception: {e}')
        waitControl.destroy()
        #print(f"Datei wurde gespeichert unter: {save_filename}")

    def download_folder(url, save_folder_name):
        googledriver.download_folder(url, save_folder_name)

if __name__ == '__main__':
    #GoogleDrive.download_file('https://drive.google.com/file/d/1cMaGRmDjnx43fLHkYFif29BkXYZzmj23/view?usp=sharing', 'test.zip')
    GoogleDrive.download_folder('https://drive.google.com/drive/folders/1fe_BnH4ro1AqhDjHFeebvhRwugwPAfU-?usp=sharing', 'test')
    pass