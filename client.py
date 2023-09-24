import socket
import struct
import time
import sys

# Constants from the specification
MAX_UDP_PACKET_SIZE = 424
MTU_SIZE = 412
INITIAL_CWND = 412
INITIAL_SS_THRESH = 12000
INITIAL_SEQUENCE_NUMBER = 50000

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
    sock.sendto(packet, (server_address, server_port))
    print(f"SEND {seq_num} {ack_num} {conn_id} {cwnd} {ss_thresh} {'ACK' if ack_flag else ''} {'SYN' if syn_flag else ''} {'FIN' if fin_flag else ''}")

# Function to receive a packet
def receive_packet(sock):
    packet, addr = sock.recvfrom(MAX_UDP_PACKET_SIZE)
    header = struct.unpack('!IIBB', packet[:12])
    data = packet[12:].decode('utf-8')
    seq_num, ack_num, conn_id, flags = header
    print(f"RECV {seq_num} {ack_num} {conn_id} {cwnd} {ss_thresh} {'ACK' if flags & 0x10 else ''} {'SYN' if flags & 0x02 else ''} {'FIN' if flags & 0x01 else ''}")
    return seq_num, ack_num, conn_id, flags, data

# Parse command-line arguments
if len(sys.argv) != 4:
    sys.stderr.write("ERROR: Invalid number of arguments\n")
    sys.exit(1)

server_address = sys.argv[1]
server_port = int(sys.argv[2])
file_name = sys.argv[3]

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Perform the 3-way handshake
conn_id = 0  # You may need to manage connection IDs
seq_num = INITIAL_SEQUENCE_NUMBER
ack_num = 0
cwnd = INITIAL_CWND
ss_thresh = INITIAL_SS_THRESH

# Step 1: Send SYN packet
send_packet(client_socket, '', seq_num, ack_num, conn_id, syn_flag=True)

# Step 2: Receive SYN-ACK packet
seq_num, ack_num, conn_id, flags, _ = receive_packet(client_socket)
if flags & 0x02 and flags & 0x10:
    ack_num = seq_num + 1
    seq_num += 1
else:
    sys.stderr.write("ERROR: Handshake failed\n")
    sys.exit(1)

# Step 3: Send ACK packet
send_packet(client_socket, '', seq_num, ack_num, conn_id, ack_flag=True)

# File transfer
try:
    with open(file_name, 'rb') as file:
        while True:
            data = file.read(MTU_SIZE)
            if not data:
                break
            send_packet(client_socket, data, seq_num, ack_num, conn_id, ack_flag=True)
            # Implement congestion control logic here
            # Update cwnd, ss_thresh, timers, etc.

    # Send FIN packet to close the connection
    send_packet(client_socket, '', seq_num, ack_num, conn_id, fin_flag=True)

    # Wait for incoming FIN packets for 2 seconds
    start_time = time.time()
    while time.time() - start_time < 2:
        seq_num, ack_num, conn_id, flags, _ = receive_packet(client_socket)
        if flags & 0x01:
            send_packet(client_socket, '', seq_num, ack_num, conn_id, ack_flag=True)

    # Close the socket and exit
    client_socket.close()
    sys.exit(0)

except FileNotFoundError:
    sys.stderr.write("ERROR: File not found\n")
    sys.exit(1)

except Exception as e:
    sys.stderr.write(f"ERROR: {str(e)}\n")
    sys.exit(1)
