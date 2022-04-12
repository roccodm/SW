import time

# global vars

clientName="DolphinDetector"



# jack client callbacks
def xrun_call(delay):
    print ("XRUN occoured with delay:", delay)

def stop_call(message=""):
    raise jack.CallbackExit

def data_process(frames):
    print(size(frames))





# main routines



try:
    import jack
    client = jack.Client(clientName, no_start_server=True)
    blocksize = client.blocksize
    samplerate = client.samplerate
    print (blocksize, samplerate)
    client.set_xrun_callback(xrun_call)
    client.set_process_callback(data_process)
    client.inports.register('input')
    i=client.inports[0]
    capture = client.get_ports(is_physical=True, is_output=True)
    print (i)
    time.sleep(5)
    with client:
        i.connect(capture[0])
    print ("ok ci sono")
    while True:
       pass
except:
    print ("Unable to connect to jack server (is it running?)")
    exit()


