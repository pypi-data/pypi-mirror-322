import ftplib
import paramiko
from io import BytesIO
from ftplib import FTP
from dateutil import parser
from os.path import basename
from datetime import datetime
from .file_folder import make_directory, folder_path_of_file, remove_file


def content(server: str, port: str, username: str, password: str, file_path: str, timeout: int = 20):
    file_content = ''
    if str(port) == '22':
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password, port=int(port), timeout=timeout)
        with ssh.open_sftp() as ftp:
            ftp.get_channel().settimeout(timeout)
            remote_file = ftp.open(file_path)
            try:
                for line in remote_file:
                    file_content += line
            finally:
                remote_file.close()

            utime = ftp.stat(file_path).st_mtime
            last_modified = datetime.fromtimestamp(utime)
    else:
        with FTP() as ftp, BytesIO() as r:
            ftp.connect(host=server, port=int(port))
            ftp.login(user=username, passwd=password)
            ftp.retrbinary(f'RETR {file_path}', r.write)
            file_content = r.getvalue().decode('utf-8')
            timestamp = ftp.voidcmd(f"MDTM {file_path}")[4:].strip()
            last_modified = parser.parse(timestamp)

    return {
        'name': basename(file_path),
        'last_modified': last_modified,
        'content': file_content,
    }


def get_last_modified(server: str, port: str, username: str, password: str, file_path: str, timeout: int = 20):
    if str(port) == '22':
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password, port=int(port), timeout=timeout)
        with ssh.open_sftp() as ftp:
            ftp.get_channel().settimeout(timeout)
            utime = ftp.stat(file_path).st_mtime
            last_modified = datetime.fromtimestamp(utime)
    else:
        with FTP() as ftp:
            ftp.connect(host=server, port=int(port))
            ftp.login(user=username, passwd=password)
            timestamp = ftp.voidcmd(f"MDTM {file_path}")[4:].strip()
            last_modified = parser.parse(timestamp)

    return {
        'name': basename(file_path),
        'last_modified': last_modified,
    }


def get_folder_list(server: str, port: str, username: str, password: str, folder_path: str = '', timeout: int = 20):
    if str(port) == '22':
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password, port=int(port), timeout=timeout)
        with ssh.open_sftp() as ftp:
            ftp.get_channel().settimeout(timeout)
            file_list = ftp.listdir(path=folder_path)

    else:
        with FTP() as ftp:
            ftp.connect(host=server, port=int(port))
            ftp.login(user=username, passwd=password)
            if folder_path is not None:
                ftp.cwd(folder_path)
            try:
                file_list = ftp.nlst()
            except ftplib.error_perm:
                file_list = []

    return file_list


def upload_file(local_path: str, server: str, port: str, username: str, password: str, file_path: str, confirm: bool = True, is_sftp: bool = False, timeout: int = 20):
    if is_sftp:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password, port=int(port), timeout=timeout)
        with ssh.open_sftp() as ftp:
            ftp.get_channel().settimeout(timeout)
            ftp.put(remotepath=file_path, localpath=local_path, confirm=confirm)
    else:
        with FTP() as ftp, open(local_path, 'rb') as file:
            ftp.connect(host=server, port=int(port))
            ftp.login(user=username, passwd=password)
            ftp.storbinary(f'STOR {file_path}', file)
    return True


def download_file(local_path: str, server: str, port: str, username: str, password: str, file_path: str, is_sftp: bool = False, timeout: int = 20):
    make_directory(folder_path_of_file(local_path))
    remove_file(local_path)
    if is_sftp:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password, port=int(port), timeout=timeout)
        with ssh.open_sftp() as ftp:
            ftp.get_channel().settimeout(timeout)
            ftp.get(remotepath=file_path, localpath=local_path)
    else:
        with FTP() as ftp, open(local_path, 'wb') as file:
            ftp.connect(host=server, port=int(port))
            ftp.login(user=username, passwd=password)
            ftp.retrbinary(f'RETR {file_path}', file.write)

    return True
