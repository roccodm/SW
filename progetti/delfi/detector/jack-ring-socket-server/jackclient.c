/** @file jackclient.c
 *  
 * Simple jack client that manage a single audio input port and populate the ringbuffer 
 *  
 */
 
 
 #include "ringbuffer.h"
 #include "jack-ring-socket-server.h"
 #include "jackclient.h"
 
 
/** function process
 * this is a JACK callback function called every time there is a new audio block available
 */
int process (jack_nframes_t nframes, void *arg)
{
	jack_default_audio_sample_t *in;
	in = jack_port_get_buffer (input_port, nframes);
	add_to_ring (&MyRing,in);
	return 0;      
}

/**
 * JACK calls this shutdown_callback if the server ever shuts down or
 * decides to disconnect the client.
 */
void jack_shutdown (void *arg) {
	exit (1);
}

