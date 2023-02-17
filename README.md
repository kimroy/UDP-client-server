# UDP-client-server
This is a Python program that simulates a UDP client-server communication. This program sends a list of data from the client to the server and waits for an acknowledgement response from the server. The data sent from the client is a string type with the following data "NCC-1701", "NCC-1422", "NCC-1017". The program is designed to send and receive UDP packets that have a custom header which includes a 32-bit checksum, 32-bit sequence number, and 8-byte message.

Prerequisites
Python 3.6 or higher.
How to Run the Program
Clone the repository or download the client.py and server.py files.
Open two terminal windows and navigate to the folder containing the downloaded files.
In one terminal window, run the command python server.py to start the server.
In the other terminal window, run the command python client.py to start the client.
Program Overview
The client.py file contains the following methods:

getchecksum(seq, data_item_as_bytes) - Helper function that creates and returns the checksum that will be sent over to the server.
make_pkt(seq, data_item_as_bytes, checksum) - Helper function that creates and returns the packet that will be sent over to the server.
main() - The main function that sends the list of data from the client to the server and waits for the acknowledgement response.
The server.py file contains the following methods:

getchecksum(seq, data_item_as_bytes) - Helper function that creates and returns the checksum that will be sent over to the client.
make_pkt(seq, data_item_as_bytes, checksum) - Helper function that creates and returns the packet that will be sent over to the client.
main() - The main function that listens to the client requests, checks the integrity of the received packet and sends back an acknowledgement.
