#include<stdlib.h>
#include<argp.h>

// need to mention a version string.
const char *argp_program_version = "your-cool-app 1.0.0";

// documentation string that will be displayed in the help section.
static char doc[] = "documentation for your cool application :)";

// email address for bug reporting.
const char *argp_program_bug_address = "<your e-mail address>";

// argument list for doc. This will be displayed on --help
static char args_doc[] = "ClientName";

// cli argument availble options.
static struct argp_option options[] = {
    {"name", 'n', "name", 0, "jack-client name"},
    {"port", 'p', "port", 0, "daemon tcp port"},
    {"seconds", 's', "seconds", 0, "seconds to store in the ringbuffer"},
    {0}
};


// define a struct to hold the arguments.
struct arguments{
    int  port;
    int  seconds;
    char *name;
};


// define a function which will parse the args.
static error_t parse_opt(int key, char *arg, struct argp_state *state){

    struct arguments *arguments = state->input;
    switch(key){

        case 'p':
            arguments->port = atoi(arg);
            break;
        case 's':
            arguments->seconds = atoi(arg);
            break;
        case 'n':
            arguments->name = arg;
            break;

        default:
            return ARGP_ERR_UNKNOWN;
    }

    return 0;
}


// initialize the argp struct. Which will be used to parse and use the args.
static struct argp argp = {options, parse_opt, args_doc, doc};


int main(int argc, char *args[]){

    // create a new struct to hold arguments.
    struct arguments arguments;

    // set the default values for all of the args.
  arguments.name="RingServer";
  arguments.port=8888;
  arguments.seconds=5;
    // parse the cli arguments.
    argp_parse(&argp, argc, args, 0, 0, &arguments);

    printf("\nNAME: %s", arguments.name);
    printf("\nPORT: %d", arguments.port);
    printf("\nSECONDS: %d", arguments.seconds);
    printf("\n");
}
