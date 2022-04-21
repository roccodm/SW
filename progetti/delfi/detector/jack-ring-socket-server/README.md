# WhatIsThis?

 It's a simple, lightweight audio component that acts as:
 - Jackd audio client 
 - Tcp socket server
 and uses a particular ringbuffer to store the last ``n`` seconds of recording 
 the tcp socket server can trasmit to the client the whole buffer that contains
 exactely the last ``n`` seconds recorded (using ``dump`` request).

 The socket server can also return to the client other jack/audio sample 
 information (see below).
 
 An example python client in also available.


### Usage:
     
Options:
     
     -n <int> : number of seconds to be stored in the ring buffer (default: 5)
     -p <int> : tcp port number (default: 8888)
     -c <string> : jackd client name (default: RingServer)

### Tcp client commands:

     rate    - returns the bitrate
     len     - returns the number of stored blocks in the ring
     seconds - returns the lenght of the ring in seconds
     nframes - returns the number of frames (the Jackd -p option)
     dump    - returns the whole buffer containing the last ``n`` seconds

### Credits:

* jack client component based on https://github.com/jackaudio/example-clients/blob/master/simple_client.c
* tcp socket based on https://gist.github.com/jkuri/d30571c2ec78e0293f5f0bdafa8587d5

