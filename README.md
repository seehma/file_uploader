# Python File Uploader
*file_uploader.py* observes a given directory if a file is created inside, uploads this newly created file to a ftp-server via a ftps connection and moves the file in charge (on the local machine) to another directory. It is also possible to filter the files which should be uploaded regarding their file-extension.

For the FTP connection the parameters *ftp_host*, *ftp_username* and *ftp_password* have to be filled accordingly. Also the directory which should be observed has to be given (on windows machines make a double \ to avoid python errors (e.g. C:\\temp\\mydirectory)). On the FTP server side it is also possible to give a directory, where the file should be stored.

*file_downloader.py* connects via an ftps connection to a ftp serve and downloads one file after another from it and saves it to a given directory on the machine where the script has been called. After a successful download and save operation, the file will be deleted on the remote server.

These scripts automatically create a logfile, located in the same directory as the script itself to have a history of all processed files.