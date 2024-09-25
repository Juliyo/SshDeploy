# SshKeyDeploy/cli.py

import argparse
import paramiko
from scp import SCPClient
import getpass
import json
import os

KEY_PATH = os.path.expanduser("~/.ssh/id_rsa")  # Default SSH key path


def create_ssh_client(server, user, password):
    """Create an SSH client and connect to the server."""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=user, password=password)
    return ssh

def generate_ssh_key():
    """Generate a new SSH key pair."""
    key = paramiko.RSAKey.generate(2048)
    private_key_path = KEY_PATH
    public_key_path = f"{KEY_PATH}.pub"

    # Save private key
    key.write_private_key_file(private_key_path)

    # Save public key
    with open(public_key_path, 'w') as pubkey_file:
        pubkey_file.write(f"{key.get_name()} {key.get_base64()} Generated by SendDeploy\n")

    print(f"SSH key generated: {private_key_path} and {public_key_path}")

    return public_key_path

def copy_key_to_server(public_key_path, server, user, password):
    """Copy the public SSH key to the remote server's authorized_keys."""
    ssh_client = create_ssh_client(server, user, password)

    # Append the public key to authorized_keys
    with open(public_key_path, 'r') as pubkey_file:
        public_key = pubkey_file.read()

    try:
        # Check the OS type of the remote server
        stdin, stdout, stderr = ssh_client.exec_command("uname")
        os_type = stdout.read().decode().strip()

        if os_type in ["Linux", "Darwin"]:  # Linux or macOS
            # Ensure .ssh directory exists
            ssh_client.exec_command('mkdir -p ~/.ssh')
            ssh_client.exec_command('chmod 700 ~/.ssh')

            # Append the public key to authorized_keys
            stdin, stdout, stderr = ssh_client.exec_command('cat >> ~/.ssh/authorized_keys')
            stdin.write(public_key)
            stdin.close()

            # Set permissions for authorized_keys
            ssh_client.exec_command('chmod 600 ~/.ssh/authorized_keys')
            print(f"Public key copied to {server}:{user}'s authorized_keys.")

        else:  # Asume Windows
            # For Windows, use the SSHD server setup, which typically involves the .ssh folder as well
            # Ensure the .ssh directory exists
            ssh_client.exec_command('mkdir C:\\Users\\' + user + '\\.ssh')
            ssh_client.exec_command('icacls C:\\Users\\' + user + '\\.ssh /grant "' + user + ':(OI)(CI)F"')

            # Append the public key to authorized_keys (may be named differently)
            stdin, stdout, stderr = ssh_client.exec_command('echo ' + public_key + ' >> C:\\Users\\' + user + '\\.ssh\\authorized_keys')
            ssh_client.exec_command('icacls C:\\Users\\' + user + '\\.ssh\\authorized_keys /grant "' + user + ':(F)"')

            print(f"Public key copied to {server}:{user}'s authorized_keys on Windows.")

        
    except Exception as e:
        print(f"Failed to copy key: {e}")
    finally:
        ssh_client.close()


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="A CLI tool to manage SSH keys and upload files via SCP")
    args = parser.parse_args()

    # Handle the copy key functionality
    ssh_ip = input("Enter SSH server IP address: ")
    ssh_user = input("Enter SSH username: ")
    ssh_password = getpass.getpass("Enter SSH password: ")

    # Generate SSH key
    public_key_path = generate_ssh_key()

    # Copy the public key to the server
    copy_key_to_server(public_key_path, ssh_ip, ssh_user, ssh_password)

if __name__ == "__main__":
    main()