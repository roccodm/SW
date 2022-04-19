import numpy as np
import queue
import sys
import threading

buffersize = 3
clientname = "RecTest"
rec_time = 10
q = queue.Queue(maxsize=buffersize)
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


try:
    import jack
    import soundfile as sf

    client = jack.Client(clientname, no_start_server=True)
    blocksize = client.blocksize
    samplerate = client.samplerate
    rec_blocks = int(rec_time * samplerate / blocksize)
    client.set_xrun_callback(xrun)
    client.set_shutdown_callback(shutdown)
    client.set_process_callback(process)
    with sf.SoundFile('pok_rec.wav', mode = 'w+', samplerate=samplerate, channels=1) as f:
        client.inports.register('in_1')
        with client:
            target_ports = client.get_ports(
                is_physical=True, is_output=True, is_audio=True)
            
            client.inports[0].connect(target_ports[0])
            
            timeout = blocksize * buffersize / samplerate
            f.write(q.get(timeout=timeout))
            for i in range(rec_blocks):
                f.write(q.get(timeout=timeout))
            rec_end = True
            event.wait()  # # # Wait until recording is finished
except (queue.Empty):
    # A timeout occured, i.e. there was an error in the callback
    print("Empty Queue")
