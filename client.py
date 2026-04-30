import socket

# supported queries
SUPPORTED_QUERIES = [
    "Quit"
    "What is the average moisture inside our kitchen fridges in the past hours, week and month?",
    "What is the average water consumption per cycle across our smart dishwashers in the past hour, week and month?",
    "Which house consumed more electricity in the past 24 hours, and by how much?"
]

# enter server IP and port
serverIP = input("Enter server IP: ")
serverPort = int(input("Enter server port: "))

maxBytesToReceive = 1024  

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.connect((serverIP, serverPort))

someCondition = True

while someCondition:
    # show queries to user
    print("\nSupported queries:")
    for i, query in enumerate(SUPPORTED_QUERIES):
        print(f"{i}. {query}")
    print("Enter 'q' to quit.\n")
    
    # user input
    userInput = int(input("Enter your query: "))
    
    # user quit condition
    if userInput == 0:
        someCondition = False
        break
    
    # if valid query
    if userInput >= 0 and userInput <= 3:
        myTCPSocket.send(bytearray(str(userInput), encoding='utf-8'))
        
        # receive and display server response
        serverResponse = myTCPSocket.recv(maxBytesToReceive)
        decode = serverResponse.decode('utf-8')
        print(f"\nServer response: {decode}\n")
    else:
        # reject invalid queries with user-friendly message
        print("\nSorry, this query cannot be processed. Please try one of the supported queries.\n")

myTCPSocket.close()  # close the socket when done