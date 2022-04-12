import numpy as np
import queue
import sys
import threading

buffersize = 3
clientname = "ImpedanceTubeTest2"
q = queue.Queue(maxsize=buffersize*100)
global rec_end
rec_end = False
event = threading.Event()

def print_error(*args):
    print(*args, file=sys.stderr)


def xrun(delay):
    print_error("An xrun occured, increase JACK's period size?")


def shutdown(status, reason):
    print_error('JACK shutdown!')
    print_error('status:', status)
    print_error('reason:', reason)
    event.set()


def stop_callback(msg=''):
    if msg:
        print_error(msg)
    event.set()
    raise jack.CallbackExit


def process(frames):
    if frames != blocksize:
        stop_callback('blocksize must not be changed, I quit!')
    if rec_end:
        stop_callback()  # Recording is finished
    try:
        q.put_nowait(client.inports[0].get_array()[:])
    except (queue.Full):
        print("Full Queue")
        stop_callback()

from IPython.display import clear_output
from time import sleep
from scipy.signal import stft
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl

mpl.use("Qt5Agg")

size = 4
olap = 0
olap_inv = size - olap

global fig, ax
fig, ax = plt.subplots()

sound = None
log_spec = None

def animate(i):
    global sound, spectrum, stft_data, log_spec
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        sound = np.roll(sound, -shift, axis=0)
        sound[-shift:] = data
    # arr = plt.mlab.specgram(sound, NFFT=blocksize, Fs=48000)[0]
    # print(arr.shape)
    # im.set_array(arr)
    stft_data = stft(sound, fs= samplerate, nperseg=FFT_size)
    spectrum = stft_data[2]*np.conj(stft_data[2])
    # print(spectrum.max())
    log_spec = (5*log_spec + 10*np.log10(spectrum.mean(axis=1)))/6
    line.set_ydata(log_spec)
    return line,

try:
    import jack

    client = jack.Client(clientname, no_start_server=True)
    
    blocksize = client.blocksize
    samplerate = client.samplerate
    FFT_size = size * blocksize
    overlap = olap * blocksize
    overlap_inv = olap_inv*blocksize
    
    client.set_xrun_callback(xrun)
    client.set_shutdown_callback(shutdown)
    client.set_process_callback(process)
    client.inports.register('in_1')

    timeout = blocksize * buffersize / samplerate
    sound = np.ones(blocksize*32)
    stft_data = stft(sound, fs= samplerate, nperseg=FFT_size)
    spectrum = stft_data[2]*np.conj(stft_data[2])
    log_spec = 10*np.log10(spectrum.mean(axis=1))
    line, = ax.plot(stft_data[0], log_spec)
    # line.set_ydata(spectrum.T[0])
    # fig = plt.figure(figsize=(10,5))
    # arr, freqs = plt.mlab.specgram(sound, NFFT=blocksize, Fs=samplerate)[0:2]
    # im = plt.imshow(arr, animated=True)
    ax.set_xlim(20, samplerate/2)
    ax.set_ylim(-140, 0)
    ax.set_xscale('log')
    ani = FuncAnimation(
        fig, animate, interval=timeout, blit=True)
    
    with client:
        target_ports = client.get_ports(
            is_physical=True, is_output=True, is_audio=True)
        #client.inports[0].connect(target_ports[0])
        # plt.ion()
        plt.show()
        rec_end = True
        event.wait()  # # # Wait until recording is finished
except (queue.Empty):
    # A timeout occured, i.e. there was an error in the callback
    print("Empty Queue")

