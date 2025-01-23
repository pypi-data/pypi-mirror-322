
import paramiko
from io import StringIO

class SFTPClient:
    def __init__(self, hostname, username, sftp_private_key, port):
        self.hostname = hostname
        self.username = username
        self.sftp_private_key = sftp_private_key
        self.port = port
        self.client = None

    def connect(self):
        private_key = StringIO(self.sftp_private_key)
        key = paramiko.RSAKey.from_private_key(private_key)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.hostname, 
            username=self.username, 
            port=self.port,
            pkey=key
        )
        self.client = client.open_sftp()

    def disconnect(self):
        if self.client:
            self.client.close()

    def get(self, remote_dir, local_dir, pattern="*"):
        for filename in self.client.listdir(remote_dir):
            if filename.endswith(pattern):
                remote_path = os.path.join(remote_dir, filename)
                local_path = os.path.join(local_dir, filename)
                self.client.get(remote_path, local_path)

    def upload(self, local_dir, filename, dest_remote_dir):
        local_path = os.path.join(local_dir, filename)
        dest_remote_path = os.path.join(dest_remote_dir, filename)
        self.client.put(local_path, dest_remote_path)
    