import os
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
        """Connects to the SFTP server using an OpenSSH private key."""
        # Convert the key data string into a file-like object
        private_key = StringIO(self.sftp_private_key) 
        key = paramiko.RSAKey.from_private_key(private_key)  # Pass the file-like object

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.hostname, 
            username=self.username, 
            port=self.port,
            pkey=key, 
            disabled_algorithms={
                "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]
            }, 
            banner_timeout=200
        )
        
        self.client = client.open_sftp()

    def disconnect(self):
        """Disconnects from the SFTP server."""
        if self.client:
            self.client.close()
            print("Disconnected from SFTP server.")

    def get(self, remote_dir, local_dir, pattern="*"):
        """
        Downloads files matching the pattern from remote_dir to local_dir.

        Args:
            remote_dir: Path to the remote directory.
            local_dir: Path to the local directory.
            pattern: File pattern to match (default: '*').
        """
 
        for filename in self.client.listdir(remote_dir):
            if filename.endswith(pattern):
                remote_path = os.path.join(remote_dir, filename)
                local_path = os.path.join(local_dir, filename)
                self.client.get(remote_path, local_path)
                print(f"Downloaded {filename} to {local_dir}.")

    def remove_remote_file(self, remote_dir, filename):
        """
        Removes a file from the remote directory.

        Args:
            remote_dir: Path to the remote directory.
            filename: Name of the file to remove.
        """
        try:
            remote_path = os.path.join(remote_dir, filename)
            self.client.remove(remote_path)
            print(f"Removed {filename} from {remote_dir}.")
        except Exception as e:
            print(f"Error removing file {filename} from {remote_dir}: {e}")

    def upload(self, local_dir, filename, src_remote_dir, dest_remote_dir):
        """
        Moves a file from the source remote directory to the destination remote directory and uploads a file from the local directory to the destination remote directory.

        Args:
            local_dir: Path to the local directory.
            filename: Name of the file to upload.
            src_remote_dir: Path to the source remote directory.
            dest_remote_dir: Path to the destination remote directory.
        """
        try:
            local_dir = str(local_dir)
            filename = str(filename)
            src_remote_dir = str(src_remote_dir)
            dest_remote_dir = str(dest_remote_dir)
            
            local_path = os.path.join(local_dir, filename)
            if not os.path.exists(local_path):
                print(f"File {filename} does not exist in the local directory {local_dir}.")
                return
            dest_remote_path = os.path.join(dest_remote_dir, filename)
            self.client.put(local_path, dest_remote_path)
            print(f"Uploaded {filename} from {local_dir} to {dest_remote_dir}.")
        except Exception as e:
            print(f"Error in move_and_upload: {e}")

