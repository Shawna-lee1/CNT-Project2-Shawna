#!/usr/bin/env python3
import socket
import struct
import sys

# Constants from the specification
MAX_UDP_PACKET_SIZE = 424
MTU_SIZE = 412

# Function to create the Confundo header
def create_header(seq_num, ack_num, conn_id, ack_flag=False, syn_flag=False, fin_flag=False):
    flags = 0
    if ack_flag:
        flags |= 0x10
    if syn_flag:
        flags |= 0x02
    if fin_flag:
        flags |= 0x01
    header = struct.pack('!IIBB', seq_num, ack_num, conn_id, flags)
    return header

# Function to send a packet
def send_packet(sock, data, seq_num, ack_num, conn_id, ack_flag=False, syn_flag=False, fin_flag=False):
    header = create_header(seq_num, ack_num, conn_id, ack_flag, syn_flag, fin_flag)
    packet = header + data.encode('utf-8')
    sock.sendto(packet, client_address)

# Parse command-line arguments
if len(sys.argv) != 2:
    sys.stderr.write("ERROR: Invalid number of arguments\n")
    sys.exit(1)

server_port = int(sys.argv[1])


try:
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', server_port))

except Exception as e:
    print(f"An error occurred: {e}")

server_socket.listen(1)  # Listen for one incoming connection
client_socket, client_address = server_socket.accept()



# Listen for incoming connections and respond
while True:
    data, client_address = server_socket.recvfrom(MAX_UDP_PACKET_SIZE)
    header = struct.unpack('!IIBB', data[:12])
    seq_num, ack_num, conn_id, flags = header
    print(f"RECV {seq_num} {ack_num} {conn_id} {'ACK' if flags & 0x10 else ''} {'SYN' if flags & 0x02 else ''} {'FIN' if flags & 0x01 else ''}")

    if flags & 0x02:  # If SYN flag is set, respond with SYN-ACK
        conn_id += 1
        ack_num = seq_num + 1
        seq_num = INITIAL_SEQUENCE_NUMBER
        send_packet(server_socket, '', seq_num, ack_num, conn_id, ack_flag=True, syn_flag=True)

    # Handle other packet types (ACK, FIN) as needed

    # Send data or ACK packets as needed

# Close the server socket (this code may never be reached)
server_socket.close()
