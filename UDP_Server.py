# Import libraries which will be used later in the code
import binascii
import socket
import struct
import sys
import hashlib
import random
import time

# Will use the loopback address for communication between the client and the server later in the code
UDP_IP = '127.0.0.1'
# Will use the port for communication between the client and the server later in the code
UDP_PORT = 5005
# Defined an unpacker for ease readability later in the code, it will unpack the response from the server
unpacker = struct.Struct('I 8s 32s')

# main method
def main():

    print('\nServer is set and listening at : ', UDP_IP ,' port: ', UDP_PORT)

    #Create the socket and listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    # Set the defaul ack and seq to be 0
    ack = 0
    seq = 0
 
    # Wait for message from the client 
    while True:

        # Receive the message from the client and unpack the data using the unpacker
        (data, adr) = sock.recvfrom(4096)
        UDP_Packet = unpacker.unpack(data)
        print("\nreceived from:", adr)
        print("received message:", UDP_Packet)

        # Use the helper function getchecksum to create the checksum to compare the packets to
        checksum = getchecksum(UDP_Packet[0], UDP_Packet[1])

        #If the packet is not lost and the checksums match
        if Network_Loss() == 1 and (UDP_Packet[2] == checksum):

            # Set the ack to 1 because the packet has been acknowledged 
            ack = 1
            
            # if the check sum is correct and the seq number matches
            if ((UDP_Packet[2] == checksum) and  seq == UDP_Packet[0]):

                # If the packet is not delayed
                if (Network_Delay() == 1):

                    print('CheckSums Match, Packet OK')
                    print('Packet data: ', data.decode("utf-8"))

                    # Call the helper function make_pkt to create the response packet to send to the client
                    UDP_Packet = make_pkt(ack, seq)

                    # Reverse the seq numbers for the next packet
                    if seq == 1:
                        seq = 0
                    else:
                        seq = 1

                    # Send the packet to the client
                    sock.sendto(UDP_Packet,adr)

            # If the check sums dont match
            else:
                
                print('CheckSums do not Match, Packet FAIL')

                # Reverse seq numbers
                if seq == 1:
                    seq1 = 0
                else:
                    seq1= 1

                # Make packet using helper function and send to client
                UDP_Packet = make_pkt(ack, seq1)
                sock.sendto(UDP_Packet,adr)

    # Close the socket
    sock.close() 

# Helper function to create and return the checksum for the response packet
def getchecksum(seq, data):
    # Check sum corruptor implemented to corrupt the packet data
    values = (seq, Packet_Checksum_Corrupter(data))
    UDP_Data = struct.Struct('I 8s')
    packed_data = UDP_Data.pack(*values)
    checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    return checksum

# Helper function to make the packet and return the response packet for sending
def make_pkt(ack, seq):
    response = (ack, seq)
    UDP_Data = struct.Struct('I I')
    resp_data = UDP_Data.pack(*response)
    checksum =  bytes(hashlib.md5(resp_data).hexdigest(), encoding='UTF-8')

    response = (ack,seq,checksum)
    print("Response sent: ", response)
    UDP_Data = struct.Struct('I I 32s')
    UDP_Packet = UDP_Data.pack(*response)
    return UDP_Packet

# Network delay function which will delay the packet being sent to the client and thus cause a socket timeout
def Network_Delay():
    if True and random.choice([0,0,1]) == 1: # Set to False to disable Network Delay. Default is 33% packets are delayed
        time.sleep(0.1)
        print("---Packet Delayed---")
        return 0
    else:
        print("---Packet Sent---")
        return 1

# The network loss function is lose the packet during tranmission when being sent to the client
def Network_Loss():
    if True and random.choice([0,0,1,1]) == 1: # Set to False to disable Network Loss. Default is 50% packets are lost
        print("---Packet Lost---")
        return 0 
    else:
        print("---Packet Not Lost---")
        return 1

# The packet corruptor is used to randomly corrput the packet data being sent over to the client
def Packet_Checksum_Corrupter(packetdata):
     if True and random.choice([1,0,0,1]) == 1: # Set to False to disable Packet Corruption. Default is 50% packets are corrupt
        print("---Packet Corrupted---")
        return(b'Corrupt!')
     else:
        print("---Packet Not Corrupted---")
        return(packetdata)

# Calls the main method to start the program
if __name__ == '__main__':
    main()
