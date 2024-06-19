import base64
import json

# Global variable to keep track of processed proxies
proxy_counter = 0

def rename_vmess_address(proxy, new_address):
    global proxy_counter
    base64_str = proxy.split('://')[1]
    missing_padding = len(base64_str) % 4
    if missing_padding:
        base64_str += '=' * (4 - missing_padding)
    try:
        decoded_str = base64.b64decode(base64_str).decode('utf-8')
        print("Decoded VMess proxy JSON:", decoded_str)  # Debugging
        proxy_json = json.loads(decoded_str)
        proxy_json['add'] = new_address
        proxy_counter += 1
        encoded_str = base64.b64encode(json.dumps(proxy_json).encode('utf-8')).decode('utf-8')
        renamed_proxy = 'vmess://' + encoded_str
        print("Renamed VMess proxy:", renamed_proxy)  # Debugging
        return renamed_proxy
    except Exception as e:
        print("Error processing vmess proxy: ", e)
        return None

def rename_vless_address(proxy, new_address):
    global proxy_counter
    try:
        parts = proxy.split('@')
        userinfo = parts[0]
        hostinfo = parts[1]
        hostinfo_parts = hostinfo.split(':')
        hostinfo_parts[0] = new_address
        hostinfo = ':'.join(hostinfo_parts)
        renamed_proxy = userinfo + '@' + hostinfo
        proxy_counter += 1
        print("Renamed VLess proxy:", renamed_proxy)  # Debugging
        return renamed_proxy
    except Exception as e:
        print("Error processing vless proxy: ", e)
        return None

def process_proxies(input_file, ips_file, output_file_prefix):
    # Read the single proxy configuration
    with open(input_file, 'r') as f:
        proxy = f.readline().strip()

    # Read the list of IP addresses
    with open(ips_file, 'r') as ip_f:
        ips = [line.strip() for line in ip_f.readlines()]

    # Process each IP address and create a new configuration
    for i, ip in enumerate(ips):
        if proxy.startswith('vmess://'):
            proxy = rename_vmess_address(proxy, ip)
        elif proxy.startswith('vless://'):
            proxy = rename_vless_address(proxy, ip)

        if proxy is not None:
            output_file = f'{output_file_prefix}_{i+1}.txt'
            with open(output_file, 'w') as out_f:
                out_f.write(proxy + '\n')

# Example usage
input_file = 'IPTest/config.txt'
ips_file = 'IPTest/ips.txt'
output_file_prefix = 'IPTest/output'

process_proxies(input_file, ips_file, output_file_prefix)
