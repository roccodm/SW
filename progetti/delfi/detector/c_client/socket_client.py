import socket
import numpy as np
import matplotlib.pyplot as plt

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"dump")
    for i in range(46*5):
        if i==0:
            data = s.recv(4096)
        else:
            data = data+s.recv(4096)
    myblock = np.frombuffer(data,dtype=np.float32)
    plt.plot(myblock)
    plt.show()
    print(myblock)
    from scipy.io.wavfile import write
    samplerate = 48000; 
    write("example2.wav", samplerate, myblock.astype(np.float32))
