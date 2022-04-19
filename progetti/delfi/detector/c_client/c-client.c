/** @file c_client.c
 * based on https://github.com/jackaudio/example-clients/blob/master/simple_client.c
 *
 
 samplerate = numero di campioni per secondo
 frame = blocco di campionamento composto da n campioni. Più è basso, più è realtime (e a rischio xrun)
 nframe = samplerate/frame = numero di frame per un secondo di campionamento
 
 
 
 */

#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>	//inet_addr
#include <jack/jack.h>

void *connection_handler(void *);


typedef struct ring_node_t {
    jack_default_audio_sample_t *data;
    struct ring_node_t *next;  
    unsigned short int populated; 
} ring_node, *p_ring_node;


typedef struct sample_ring_t{
    int len;
    unsigned short int populated;
    jack_nframes_t nframes;
    jack_nframes_t samplerate;
    int seconds;
    ring_node *last;  
} sample_ring;


sample_ring MyRing;

int create_sample_ring(sample_ring *ring, int nelements, jack_nframes_t samplerate, jack_nframes_t nframes, int seconds){
    ring->len = nelements;
    ring->nframes = nframes;
    ring->samplerate = samplerate;
    ring->seconds = seconds;
    ring_node *first,*last,*new;
    jack_default_audio_sample_t *data;
    
    int i;
    for (i=0; i<nelements; i++) {
        data = (jack_default_audio_sample_t *) malloc(sizeof (jack_default_audio_sample_t) * nframes);
        if (data == NULL){
            return -1;
            printf("Impossibile allocare memoria per i dati");
        }
        if (i == 0) { // primo elemento   
             first =  malloc(sizeof(ring_node));
             last = first;
        } else {
             new =  malloc(sizeof(ring_node));
             last->next = new;
             last = new;
        }
        last->data = data;
        printf ("%d %x %x %x\n",i, (int) last,(int)new,(int)last->next);
    }
    last->next = first;
    ring->last = first;
    return 1;
}


int ring_debug(sample_ring *ring){
    ring_node *first,*current;
    first = current = ring->last;
    
    int i=0;
    while (current->next != first){
        printf ("%d: %x -> %x\n",i,(int)current,(int)current->data);
        current = current -> next;        
        i++;
    } 
    return 1;
}



int add_to_ring(sample_ring *ring, jack_default_audio_sample_t *data){
     ring_node *current;
     current = ring->last;
     memcpy (current->data, data, sizeof (jack_default_audio_sample_t) * ring->nframes);
     ring->last = current->next;
     return 1;     
}


jack_port_t *input_port;
jack_port_t *output_port;
jack_client_t *client;

/**
 * The process callback for this JACK application is called in a
 * special realtime thread once for each audio cycle.
 *
 * This client does nothing more than copy data from its input
 * port to its output port. It will exit when stopped by 
 * the user (e.g. using Ctrl-C on a unix-ish operating system)
 */
int
process (jack_nframes_t nframes, void *arg)
{
	jack_default_audio_sample_t *in;
	in = jack_port_get_buffer (input_port, nframes);
	
	add_to_ring (&MyRing,in);
	
     //ring_node *current;
     //current = MyRing.last;
     //memcpy (current->data, in, sizeof (jack_default_audio_sample_t) * nframes);
     //MyRing.last = current->next;
	
	
//	memcpy (buffer, in,
//		sizeof (jack_default_audio_sample_t) * nframes);

        //printf ("Nframes: %ld", nframes * sizeof (jack_default_audio_sample_t));
	return 0;      
}

/**
 * JACK calls this shutdown_callback if the server ever shuts down or
 * decides to disconnect the client.
 */
void
jack_shutdown (void *arg)
{
	exit (1);
}

int
main (int argc, char *argv[])
{
	const char **ports;
	const char *client_name = "DolphinDetector";
	const char *server_name = NULL;
	jack_options_t options = JackNullOption;
	jack_status_t status;
	
	/* open a client connection to the JACK server */

	client = jack_client_open (client_name, options, &status, server_name);
	if (client == NULL) {
		fprintf (stderr, "jack_client_open() failed, "
			 "status = 0x%2.0x\n", status);
		if (status & JackServerFailed) {
			fprintf (stderr, "Unable to connect to JACK server\n");
		}
		exit (1);
	}
	if (status & JackServerStarted) {
		fprintf (stderr, "JACK server started\n");
	}
	if (status & JackNameNotUnique) {
		client_name = jack_get_client_name(client);
		fprintf (stderr, "unique name `%s' assigned\n", client_name);
	}

       // inizializzo struttura dati
       int nelements=jack_get_sample_rate (client) / jack_get_buffer_size(client)*1;  // manca n seconds!
       
       create_sample_ring(&MyRing, nelements, jack_get_sample_rate (client), jack_get_buffer_size(client), 1);

       printf ("len %d\n", MyRing.len);
       printf ("nframes %d\n", MyRing.nframes);
       printf ("sr %d\n",MyRing.samplerate);
       printf ("pointer %x\n",(int)MyRing.last);

       ring_debug(&MyRing);

	/* tell the JACK server to call `process()' whenever
	   there is work to be done.
	*/

	jack_set_process_callback (client, process, 0);

	/* tell the JACK server to call `jack_shutdown()' if
	   it ever shuts down, either entirely, or if it
	   just decides to stop calling us.
	*/

	jack_on_shutdown (client, jack_shutdown, 0);

	/* display the current sample rate. 
	 */

	printf ("engine sample rate: %" PRIu32 "\n",
		jack_get_sample_rate (client));

	/* create two ports */

	input_port = jack_port_register (client, "input",
					 JACK_DEFAULT_AUDIO_TYPE,
					 JackPortIsInput, 0);

	if (input_port == NULL) {
		fprintf(stderr, "no more JACK ports available\n");
		exit (1);
	}

	/* Tell the JACK server that we are ready to roll.  Our
	 * process() callback will start running now. */

	if (jack_activate (client)) {
		fprintf (stderr, "cannot activate client");
		exit (1);
	}

	/* Connect the ports.  You can't do this before the client is
	 * activated, because we can't make connections to clients
	 * that aren't running.  Note the confusing (but necessary)
	 * orientation of the driver backend ports: playback ports are
	 * "input" to the backend, and capture ports are "output" from
	 * it.
	 */

	ports = jack_get_ports (client, NULL, NULL,
				JackPortIsPhysical|JackPortIsOutput);
	if (ports == NULL) {
		fprintf(stderr, "no physical capture ports\n");
		exit (1);
	}

	if (jack_connect (client, ports[0], jack_port_name (input_port))) {
		fprintf (stderr, "cannot connect input ports\n");
	}


	free (ports);

	/* keep running until stopped by the user */

	//sleep (-1);


        // gestione socket
        
	int socket_desc , new_socket , c , *new_sock;
	struct sockaddr_in server , socket_client;
	char *message;
	
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
	if (socket_desc == -1)
	{
		printf("Could not create socket");
	}
	
	//Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons( 8888 );
	
	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
	{
		puts("bind failed");
		return 1;
	}
	puts("bind done");
	
	//Listen
	listen(socket_desc , 3);
	
	//Accept and incoming connection
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while( (new_socket = accept(socket_desc, (struct sockaddr *)&socket_client, (socklen_t*)&c)) )
	{
		puts("Connection accepted");
		
	        pthread_t sniffer_thread;
		new_sock = malloc(1);
		*new_sock = new_socket;
		
		if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) new_sock) < 0)
		{
			perror("could not create thread");
			return 1;
		}
		
		puts("Handler assigned");
	}        
        
        
       // fine gestione socket

	/* this is never reached but if the program
	   had some other way to exit besides being killed,
	   they would be important to call.
	*/

	jack_client_close (client);
	exit (0);
}

void *connection_handler(void *socket_desc)
{
	//Get the socket descriptor
	int sock = *(int*)socket_desc;
	int readed;
	char client_data[1024];
	char buffer[256];
	
	while ((readed = recv(sock, client_data, sizeof(client_data),0)) > 0) {
            
            sprintf(buffer,"Pointer corrente: %x\n", MyRing.last);
            if (strncmp(client_data,"dump",4)==0){
                ring_node *first,*current;
                first = current = MyRing.last;
    
                int i=0;
               while (current->next != first){
                   send(sock, current->data, sizeof (jack_default_audio_sample_t) * MyRing.nframes, 0);
                   printf ("%d: %x -> %x\n",i,(int)current,(int)current->data);
                   current = current -> next;        
                   i++;
               } 

            }	
            write (sock, buffer, sizeof(buffer));
 	}
	
        if (readed == 0) {
		puts("Client disconnected");
		fflush(stdout);                   
        }
	
	//Free the socket pointer
	free(socket_desc);
	
	return 0;
}



