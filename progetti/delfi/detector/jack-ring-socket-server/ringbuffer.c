/** @file ringbuffer.c
 * 
 */
#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include "ringbuffer.h"
 
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
        printf ("%d %p %p %p\n",i, last,new,last->next);
    }
    last->next = first;
    ring->last = first;
    return 1;
}

int ring_debug(sample_ring *ring){
    ring_node *first,*current;
    first = current = ring->last;
    
    printf ("il primo: %p \n",first);
    
    int i=0;
    do {
        printf ("%d: %p -> %p\n",i,current,current->next);
        i++;
        current = current -> next;        
    } while (current != first);
    printf ("esco con current: %p \n",current);
    printf ("il primo: %p \n",first);
    return 1;
}

int add_to_ring(sample_ring *ring, jack_default_audio_sample_t *data){
     ring_node *current;
     current = ring->last;
     memcpy (current->data, data, sizeof (jack_default_audio_sample_t) * ring->nframes);
     ring->last = current->next;
     return 1;     
}

