/* WhatIsThis?
 *
 * It's a simple, lightweight audio component that acts as:
 * - Jackd audio client 
 * - Tcp socket server
 * and uses a particular ringbuffer to store the last ``n`` seconds of recording 
 * the tcp socket server can trasmit to the client the whole buffer that contains
 * exactely the last ``n`` seconds recorded (using ``dump`` request).
 *
 * The socket server can also return to the client other jack/audio sample 
 * information (see below).
 * 
 * An example python client in also available.
 *
 * Compiling:
 *
 *     this software requires the jackd-dev library. In debian world is called libjack-jackd2-dev 
 *     the following command shold be enought to compile and build:
 *           gcc ``source file`` -o ``program name`` -lm -lsndfile -ljack 
 *
 *
 * Usage:
 *     
 *
 *     Options (all of these are mandatory):
 *     
 *     -n <int> : number of seconds to be stored in the ring buffer
 *     -p <int> : tcp port number
 *     -c <string> : jackd client name
 *
 * Tcp client commands:
 *
 *     dump - returns the whole buffer containing the last ``n`` seconds
 *
 * Credits:
 *
 * jack client component based on https://github.com/jackaudio/example-clients/blob/master/simple_client.c
 * tcp socket based on https://gist.github.com/jkuri/d30571c2ec78e0293f5f0bdafa8587d5
 */
