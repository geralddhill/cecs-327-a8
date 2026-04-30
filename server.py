import socket

import psycopg2
import os

from dotenv import load_dotenv, dotenv_values 

# loading variables from .env file

load_dotenv() 


MAX_BYTES_TO_RECIEVE = 1024


def fetchMoisture():
    res = {}
    for time_range in ['24 hours', '1 week', '1 month']:
        avgs = []
        for id in ['A', 'B']:

            conn = None

            try:
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(

                    dbname=os.getenv(f"PGDATABASE{id}"),

                    user=os.getenv(f"PGUSER{id}"),

                    password=os.getenv(f"PGPASSWORD{id}"),

                    host=os.getenv(f"PGHOST{id}")
                )


                # create a cursor

                cur = conn.cursor()


                cur.execute(f'SELECT AVG(COALESCE(((payload->>\'Moisture Meter - Fridge-Moisture-Meter\')::numeric), ((payload->>\'Moisture Meter - Fridge-Moisture-Meter 2 8742d24f-4dbf-4e87-8b8d-bba528b92347\')::numeric), ((payload->>\'Moisture Meter - Fridge 1 Moisture Meter\')::numeric), ((payload->>\'Moisture Meter - Fridge 2 Moisture Meter\')::numeric))) FROM {'data_virtual' if id == 'A' else 'homedata_virtual'} WHERE time BETWEEN NOW() - INTERVAL \'{time_range}\' and NOW()')


                data = float(cur.fetchone()[0])
                avgs.append(data)


                # close the communication with the PostgreSQL
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

            finally:

                if conn is not None:
                    conn.close()

                    print('Database connection closed.')
        res[time_range] = sum(avgs)/len(avgs)
    return res



def fetchWaterConsumption():
    res = {}
    for time_range in ['24 hours', '1 week', '1 month']:
        avgs = []
        for id in ['A', 'B']:

            conn = None

            try:
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(

                    dbname=os.getenv(f"PGDATABASE{id}"),

                    user=os.getenv(f"PGUSER{id}"),

                    password=os.getenv(f"PGPASSWORD{id}"),

                    host=os.getenv(f"PGHOST{id}")
                )


                # create a cursor

                cur = conn.cursor()


                cur.execute(f'SELECT AVG(COALESCE(((payload->>\'YF-S201 - Dishwasher-Water-Consumption\')::numeric), ((payload->>\'Water Consumption\')::numeric))) FROM {'data_virtual' if id == 'A' else 'homedata_virtual'} WHERE time BETWEEN NOW() - INTERVAL \'{time_range}\' and NOW()')


                data = float(cur.fetchone()[0])
                avgs.append(data)


                # close the communication with the PostgreSQL
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

            finally:

                if conn is not None:
                    conn.close()

                    print('Database connection closed.')
        res[time_range] = sum(avgs)/len(avgs)
    return res



def fetchMoreElecConsumption():
    usage = {}
    for id in ['A', 'B']:

        conn = None

        try:
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(

                dbname=os.getenv(f"PGDATABASE{id}"),

                user=os.getenv(f"PGUSER{id}"),

                password=os.getenv(f"PGPASSWORD{id}"),

                host=os.getenv(f"PGHOST{id}")
            )


            # create a cursor

            cur = conn.cursor()


            cur.execute(f'SELECT {'COALESCE(SUM(COALESCE(((payload->>\'ACS712 - Fridge-Ammeter\')::numeric), 0)), 0), COALESCE(SUM(COALESCE(((payload->>\'ACS712 - Fridge-Ammeter 3 8742d24f-4dbf-4e87-8b8d-bba528b92347\')::numeric), 0)), 0), COALESCE(SUM(COALESCE(((payload->>\'ACS712 - Dishwasher-Ammeter\')::numeric), 0)), 0)' if id == 'A' else 'COALESCE(SUM(COALESCE(((payload->>\'Fridge 1 Ammeter\')::numeric), 0)), 0), COALESCE(SUM(COALESCE(((payload->>\'Fridge 2 Ammeter\')::numeric), 0)), 0), COALESCE(SUM(COALESCE(((payload->>\'Dishwasher Ammeter\')::numeric), 0)), 0)'} FROM {'data_virtual' if id == 'A' else 'homedata_virtual'} WHERE time BETWEEN NOW() - INTERVAL \'24 hours\' and NOW()')


            data = cur.fetchone()
            usage[id] = sum(map(float, data))


            # close the communication with the PostgreSQL
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:

            if conn is not None:
                conn.close()

                print('Database connection closed.')
    if usage['A'] > usage['B']:
        return 'A', usage['A'] - usage['B']
    elif usage['A'] < usage['B']:
        return 'B', usage['B'] - usage['A']
    else:
        return None, 0



def main():
    SERVER_ADDRESS = "192.168.0.105"
    SERVER_PORT = 5000



    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Socket successfully created.")

    tcp_socket.bind((SERVER_ADDRESS, SERVER_PORT))

    print(f"Socket binded to port {SERVER_PORT}.")

    tcp_socket.listen(5)

    print("Socket is listening...")
    

    while True:

        incoming_socket, incoming_address = tcp_socket.accept()

        print(f"Got connection from {incoming_address}")


        data = incoming_socket.recv(MAX_BYTES_TO_RECIEVE)

        decode = int(data.decode('utf-8'))

        res = None

        if decode == 1:
            res = fetchMoisture()
        elif decode == 2:
            res = fetchWaterConsumption()
        elif decode == 3:
            res = fetchMoreElecConsumption()

        if res is None:
            incoming_socket.send(bytearray("Error: Invalid input.", encoding="utf-8"))
        else:
            incoming_socket.send(bytearray(res, encoding="utf-8"))


        incoming_socket.close()

        print("Server: Closing socket")

main()