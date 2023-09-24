import socket
import struct
import sys

# Constants from the specification
MAX_TCP_PACKET_SIZE = 424

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
    sock.send(packet)

# Parse command-line arguments
if len(sys.argv) != 2:
    sys.stderr.write("ERROR: Invalid number of arguments\n")
    sys.exit(1)

server_port = int(sys.argv[1])

try:
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(1)  # Listen for incoming connections

    print(f"Server is listening on port {server_port}")

    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        data = client_socket.recv(MAX_TCP_PACKET_SIZE)
        if not data:
            break

        # Process received data and send response packets
        # You can use your existing packet handling logic here

    # Close the client and server sockets when done
    client_socket.close()
    server_socket.close()

except Exception as e:
    sys.stderr.write(f"An error occurred: {e}\n")
    sys.exit(1)

