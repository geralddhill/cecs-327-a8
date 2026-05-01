# CECS 327 Assignment 8
## Instructions for running the system:

One computer runs the server.py file, while the other runs the client.py file. The client enters the server's IP and port that is displayed on the server's screen. Then the client can input a number (1-3) to pick their desired query, or 0 to end the session.

## System Architecture:

The distributed smart-house design contains two smart houses that feed data into NeonDB, which then send information to the Server. Then, when the TCP Client prompts a query it is decoded by the Server, which returns the correct information. The Client uses an option based UI to filter out unwanted queries. 
