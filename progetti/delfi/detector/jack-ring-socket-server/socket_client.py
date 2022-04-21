import socket
import numpy as np
import matplotlib.pyplot as plt

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

size_of_float = 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"nframes")
    nframes = int(s.recv(256).decode("utf8").split("\n")[0])
    s.sendall(b"len")
    nblocks = int(s.recv(256).decode('utf8').split("\n")[0])
    s.sendall(b"rate")
    samplerate = int(s.recv(256).decode('utf8').split("\n")[0])
    s.sendall(b"seconds")
    seconds = int(s.recv(256).decode('utf8').split("\n")[0])
    
    blocksize = size_of_float * nframes
    
    s.sendall(b"dump")
    for i in range(nblocks):
        if i==0:
            data = s.recv(blocksize)
        else:
            data = data+s.recv(blocksize)
    myblock = np.frombuffer(data,dtype=np.float32)
    plt.plot(myblock)
    plt.show()
    print(myblock)
    from scipy.io.wavfile import write

    write("example2.wav", samplerate, myblock.astype(np.float32))
