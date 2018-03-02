from __future__ import print_function
import socket
import logging
import zmq

def client_old(ip, port, message):
    response = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setblocking(0)
    try:
        sock.connect((ip, port))
        connection = True
    except:
        logging.error('Error: can not connect to the server')
        connection = False
        raise IOError('Can not connect to the server')
    if connection:
        try:
            sock.sendall(message)
            response = sock.recv(4096)
            # print "Received: {}".format(response)
        except:
            logging.error(
                'Error:  cannot send message to the server: %s' % message)
            raise IOError('Can not send a message to the server')
        finally:
            sock.close()
            return response

# HPD raspberry pi address: http://132.163.53.67:50000/
# String to get termperatures: 'getall'
# String to get temperature label names: 'getlabels'
# Todo: add if __main__ clause

def client_new(ip, port, message):
    REQUEST_TIMEOUT = 20000
    REQUEST_RETRIES = 3
    SERVER_ENDPOINT = "tcp://%s:%d" % (ip, port)
    context = zmq.Context(1)
    client = context.socket(zmq.REQ)
    client.connect(SERVER_ENDPOINT)
    poll = zmq.Poller()
    poll.register(client, zmq.POLLIN)
    retries_left = REQUEST_RETRIES
    reply = ''

    while retries_left:
        request = str(message)
        client.send_string(request)
        expect_reply = True
        try:
            while expect_reply:
                socks = dict(poll.poll(REQUEST_TIMEOUT))
                if socks.get(client) == zmq.POLLIN:
                    reply = client.recv()
                    if reply:
                        client.close()
                        retries_left = 0
                        expect_reply = False
                        #break
                    else:
                        logging.error("Error: No reply from server, empty string")
                else:
                    logging.error("Error: No response from server, retrying...")
                    raise IOError('No reply from server')
                    # Socket is confused. Close and remove it.
                    client.setsockopt(zmq.LINGER, 0)
                    client.close()
                    poll.unregister(client)
                    retries_left -= 1
                    if retries_left == 0:
                        logging.error("Error: Server seems to be offline, abandoning")
                        raise IOError('Abandoning server')
                        break
                    logging.error("Error: Reconnecting and resending (%s)" % request)
                    # Create new connection
                    client = context.socket(zmq.REQ)
                    client.connect(SERVER_ENDPOINT)
                    poll.register(client, zmq.POLLIN)
                    client.send_string(request)
        except KeyboardInterrupt:
            client.close()
            logging.error("Error: Keyboard interruption, stopping...")
            pass

    return reply
    context.term()

def client(ip, port, message):
    return client_new(ip, port, message)


if __name__ == "__main__":
    all_temps = client('132.163.53.67',50326,'getall')
    all_labels = client('132.163.53.67',50326,'getlabels')
    print(all_labels.decode('ascii'))
    print(all_temps.decode('ascii'))

    # to call from another file:
#    import client
#    client.client('132.163.53.67',50326,'getall')

