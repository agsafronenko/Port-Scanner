import socket
from common_ports import ports_and_services


def is_ip_address(host):
    try:
        socket.inet_aton(host)
        return True
    except socket.error:
        return False


def handle_host_error(host):
    return "Error: Invalid IP address" if not host[0].isalpha() else "Error: Invalid hostname"


def get_host_data(host):
    host_name, host_ip = None, None
    if is_ip_address(host):
        host_ip = host
        try:
            host_name = socket.gethostbyaddr(host_ip)[0]
        except:
            host_name = None
    else:
        host_name = host
        host_ip = socket.gethostbyname(host_name)
    return host_name, host_ip


def gerenate_verbose_string(host, open_ports):
    host_name, host_ip = get_host_data(host)
    host_str = f"{host_name} ({host_ip})" if host_name else f"{host_ip}"
    header_str = f"Open ports for {host_str}\nPORT     SERVICE\n"
    data_str = "\n".join(f"{port_number:<9}{ports_and_services[port_number]}" for port_number in open_ports)
    return header_str + data_str


def get_open_ports(host, port_range, verbose=False):
    print("host -->", host)
    open_ports = []

    for port_number in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_socket:
            socket.setdefaulttimeout(1)
            try:
                connection_result = connection_socket.connect_ex((host, port_number))
                if connection_result == 0:
                    open_ports.append(port_number)
            except socket.gaierror:
                return handle_host_error(host)

    return open_ports if not verbose else gerenate_verbose_string(host, open_ports)
