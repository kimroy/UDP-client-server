# Import libraries which will be used later in the code
import binascii
import socket
import struct
import sys
import hashlib

# Will use the loopback address for communication between the client and the server later in the code
UDP_IP = '127.0.0.1'
# Will use the port for communication between the client and the server later in the code
UDP_PORT = 5005
# Set up a list of data that will be sent from the client
data_list = ['NCC-1701', 'NCC-1422', 'NCC-1017']
# Defined an unpacker for ease readability later in the code, it will unpack the response from the server
unpacker = struct.Struct('I I 32s')

# main method
def main():

    print('UDP target IP:', UDP_IP)
    print('UDP target port:', UDP_PORT)

    # Set the default ack and seq to 0
    seq = 0
    ack = 0

    # Loop throguh for each data item to send in the list
    for data_item in data_list:

        # convert the data item to byte by using the encode method to send across the port
        data_item_as_bytes = data_item.encode('utf-8')

        # Call a helper function getchecksum to create the check sum for the packet
        checksum = getchecksum(seq, data_item_as_bytes)

        # Call the helper function make_pkt to create the packet that will be sent over
        snd_pkt = make_pkt(seq, data_item_as_bytes, checksum)

        print("\n",snd_pkt.decode('utf-8'))

        #Send the UDP packet
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(snd_pkt, (UDP_IP, UDP_PORT))
        print('UDP Packet has been sent')

        # This will read the reponse of the server and act accordingly
        while True:

            # Set the socket time out to 9ms according to assignment specifications
            sock.settimeout(0.009)

            # Try to unpack the data that was sent from the server
            try:

                # Receive the information from the socket
                (data, adr) = sock.recvfrom(4096)

                # Unpack the data and store it in the UDP_Packet 
                UDP_Packet = unpacker.unpack(data)

                # This to check the checksum that is received from the server to ensure that they are the same
                values = (UDP_Packet[0], UDP_Packet[1])
                UDP_Data = struct.Struct('I I')
                packed_data = UDP_Data.pack(*values)
                checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

                # If the checksums are the same and the seq num has not changed between transmission
                if checksum == UDP_Packet[2] and UDP_Packet[1] == seq:
                    print('Packet data sent back from the receiver: ', UDP_Packet )

                    # Set the socket timeout to nothing because the data was received succesfully
                    sock.settimeout(None)

                    # Reverse the seq num for the next data item that will be sent to the server
                    if seq == 1:
                        seq = 0
                    else:
                        seq = 1

                    # Break because the loop should finish for that data item once the correct response has been received
                    break;

                # If the checksum do not match inform the user
                else:
                    print ("Check sums do not match, packet corrupt")

            # To catch the exception if there is a socket timeout then resend the same packet again
            except socket.timeout:
                print("Timed Out")
                sock.sendto(snd_pkt, (UDP_IP, UDP_PORT))
                print("UDP Packet has been sent again.")

    # Close the client socket once all of the information was passed
    sock.close()

# Helper function which will create and return the checksum that will be sent over to the server
def getchecksum(seq, data_item_as_bytes):
    #Create the checksum
    values = (seq, data_item_as_bytes)
    UDP_Data = struct.Struct('I 8s')
    packed_data = UDP_Data.pack(*values)
    checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    return checksum

# Helper function which will create and return the packet that will be sent over to the server
def make_pkt(seq, data_item_as_bytes, checksum):

    #Build the UDP packet to send
    values = (seq, data_item_as_bytes, checksum)
    UDP_Packet_Data = struct.Struct('I 8s 32s')
    return UDP_Packet_Data.pack(*values)

# Calls the main method to start the program
if __name__ == '__main__':
    main()
