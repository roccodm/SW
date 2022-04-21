/** @file jackclient.c
 * 
 */
 
 
 #include "ringbuffer.h"
 #include "jack-ring-socket-server.h"
 #include "jackclient.h"
 
 
/**
 * The process callback for this JACK application is called in a
 * special realtime thread once for each audio cycle.
 *
 * This client does nothing more than copy data from its input
 * port to its output port. It will exit when stopped by 
 * the user (e.g. using Ctrl-C on a unix-ish operating system)
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

