/** @file socketserver.c
 * 
 */
 
 
 #include "jack-ring-socket-server.h"
 
 void *connection_handler(void *socket_desc)
{
	//Get the socket descriptor
	int sock = *(int*)socket_desc;
	int readed;
	char client_data[1024];
	char buffer[256];
	
	while ((readed = recv(sock, client_data, sizeof(client_data),0)) > 0) {
            
            sprintf(buffer,"Pointer corrente: %p\n", MyRing.last);
            if (strncmp(client_data,"dump",4)==0){
                ring_node *first,*current;
                first = current = MyRing.last;
    
                int i=0;
                printf ("Size of transission block: %ld\n", sizeof (jack_default_audio_sample_t) * MyRing.nframes);
                do {
                    send(sock, current->data, sizeof (jack_default_audio_sample_t) * MyRing.nframes, 0);
                    current = current -> next;        
                    i++;
                } while (current != first);
                printf ("Number of cycles: %d\n",i);
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
