/** @file jack-ring-socket-server.h
 * 
 * called by: main.c
 *
 * calls: ringbuffer.h socketserver.h jackclient.h 
 *
 */


#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <jack/jack.h>

#include "jackclient.h"
#include "ringbuffer.h"
#include "socketserver.h"



#ifndef GLOBALS
#define GLOBALS

// initialize the ring structure as global variable 
extern sample_ring MyRing;

// inizialize jack-client environment
extern jack_port_t *input_port;
extern jack_port_t *output_port;
extern jack_client_t *client;

#endif
