powerline-daemon
================

A daemon to reduce the resource consumption of powerline by having a single
python process that serves all powerline requests.

Currently only works on linux.

To use it, compile the powerline-client as

```
gcc -O3 powerline-client.c -o powerline-client
```
Make powerline-daemon executable

```
chmod +x powerline_daemon
```

Then copy powerline-daemon and powerline-client somewhere on your path, like
/usr/local/bin

Launch the daemon with:

```
powerline-daemon
```

Then where-ever you have calls to powerline, like in your .bashrc or tmux
config, replace them with:

```
powerline-client
```

That's it. powerline-client is a drop in replacement for powerline, it supports
all the same arguments and options and produces identical output.
