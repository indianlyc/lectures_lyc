import socket
import struct
import textwrap

# ethernet frame
# mac address bit
# ip header
# ipv4 packet
# icmp packet
# tcp/ip packet
# tcp segment
# udp segment

TAB_1 = "\t - "
TAB_2 = "\t\t - "
TAB_3 = "\t\t\t - "
TAB_4 = "\t\t\t\t - "

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def ipv4(addr):
    return '.'.join(map(str, addr))

def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]

def tcp_segment(data):
    src_port, dest_port, sequence, acknowledgement, offset_reserved_flags = \
                                    struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    return (src_port, dest_port, sequence, acknowledgement,
            flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:])

def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H @x H', data[:8])
    return src_port, dest_port, size, data[8:]

def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])
def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print('\nEthernet Frame:')
        print(f'{TAB_1}Destination: {dest_mac}, Source: {src_mac}, Protocol: {eth_proto}')

        if eth_proto == 8:
            version, header_length, ttl, proto, src, target, data = ipv4_packet(data)
            print(TAB_1 + 'IPv4 Packet:')
            print(TAB_2 + f'Version: {version}, Header Length: {header_length}, TTL: {ttl}')
            print(TAB_3 + f'Protocol: {proto}, Source {src}, Target {target}')

            if proto == 1:
                icmp_type, code, checksum, data = icmp_packet(data)
                print(TAB_1 + "ICMP Packet:")
                print(TAB_2 + f"Type: {icmp_type}, Code: {code}, Checksum: {checksum}")
                print(TAB_2 + "Data:")
                print(format_multi_line(DATA_TAB_3, data))

            elif proto == 6:
                (src_port, dest_port, sequence, acknowledgement,
                 flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
                print(TAB_1 + "TCP Segment:")
                print(TAB_2 + f"Source Port: {src_port}, Destination Port: {dest_port}")
                print(TAB_2 + f"Sequence: {sequence}, Acknowledgment: {acknowledgement}")
                print(TAB_2 + f"Flags:")
                print(TAB_3 + f"URG: {flag_urg}, ACK: {flag_ack}, PSH: {flag_psh}, RST: {flag_rst}, SYN: {flag_syn}, FIN: {flag_fin}")
                print(TAB_2 + "Data:")
                print(format_multi_line(DATA_TAB_3, data))

            elif proto == 17:
                src_port, dest_port, length, data = udp_segment(data)
                print(TAB_1 + "UDP Segment:")
                print(TAB_2 + f"Source Port: {src_port}, Destination Port: {dest_port}, Length: {length}")
                print(format_multi_line(DATA_TAB_3, data))
            else:
                print(TAB_1 + "Data:")
                print(format_multi_line(DATA_TAB_2, data))
        else:
            print("Data:")
            print(format_multi_line(DATA_TAB_1, data))

if __name__ == "__main__":
    main()