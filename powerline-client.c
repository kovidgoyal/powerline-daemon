/*
 * powerline-client.c
 * Copyright (C) 2013 Kovid Goyal <kovid at kovidgoyal.net>
 *
 * Distributed under terms of the GPL3 license.
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/un.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#define handle_error(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)

void do_write(int sd, const char *raw, int len) {
    int written = 0, n = -1;

    while (written < len) {
        n = write(sd, raw+written, len-written);
        if (n == -1) {
            close(sd);
            handle_error("write() failed");
        }
        written += n;
    }
}
        
int main(int argc, char *argv[]) {
    int sd = -1, i, j=0;
    struct sockaddr_un server;
    char address[50] = {};
    const char eof[2] = "\0\0";
    char buf[4096] = {};
    char *newargv[200] = {};

    if (argc < 2) { printf("Must provide at least one argument.\n"); return EXIT_FAILURE; }

    snprintf(address, 50, "powerline-ipc-%d", getuid());

    sd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sd == -1) handle_error("socket() failed");

    memset(&server, 0, sizeof(struct sockaddr_un)); // Clear 
    server.sun_family = AF_UNIX;
    strncpy(server.sun_path+1, address, strlen(address));

    if (connect(sd, (struct sockaddr *) &server, sizeof(server.sun_family) + strlen(address)+1) < 0) {
        close(sd);
        // We failed to connect to the daemon, execute powerline instead
        argc = (argc < 199) ? argc : 199;
        for (i=1, j=0; i < argc; i++) {
            // We dont need the --cwd option since we are already in the correct directory
            if (strstr(argv[i], "--cwd=") == argv[i]) { j += 1; continue; }
            if (strcmp("--cwd", argv[i]) == 0) { j += 2; i+=1; continue; }
            newargv[i-j] = argv[i];
        }
        newargv[0] = "powerline";
        newargv[argc-j] = NULL;
        execvp("powerline", newargv);
    }

    for (i = 1; i < argc; i++) {
        do_write(sd, argv[i], strlen(argv[i]));
        do_write(sd, eof, 1);
    }
    do_write(sd, eof, 2);

    i = -1;
    while (i != 0) {
        i = read(sd, buf, 4096);
        if (i == -1) {
            close(sd);
            handle_error("read() failed");
        }
        if (i > 0) 
            write(STDOUT_FILENO, buf, i);
    }

    close(sd);

    return 0;
}


