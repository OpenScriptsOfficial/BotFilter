import paramiko


def block_ip_via_ssh(ip_address, server_ip, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server_ip, username=username, password=password)

    command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
    ssh_client.exec_command(command)

    ssh_client.close()
    print(f"IP-адрес {ip_address} заблокирован на сервере {server_ip}.")


block_ip_via_ssh("192.168.1.100", "server_ip", "username", "password")  # Замените на реальные данные
