pywatcher
===================

monitor file and reload process. like gulp watch

install
-----------

```sh
$ pip install pywatcher
```

usage
-----------

```sh
usage: pywatcher [-h] -t TARGET_DIR_PATH -c TARGET_COMMAND_STR
                 [-i RELOAD_THRESHOLD_SECONDS] [--disable-capture-stdout]

-----------------------------------------------------------------------
PyWatcher:

monitor file and reload process. like gulp watch

e.g:

pywatcher -t .  -c 'ping localhost'
-> if some file on current dir changed, restart process 'ping localhost'.

-----------------------------------------------------------------------

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_DIR_PATH, --target-dir TARGET_DIR_PATH
                        target directory for watching.
  -c TARGET_COMMAND_STR, --command TARGET_COMMAND_STR
                        target command. this command execute and restart when file changed.
  -i RELOAD_THRESHOLD_SECONDS, --reload-interval-seconds RELOAD_THRESHOLD_SECONDS
                        reload threshold seconds.
  --disable-capture-stdout
                        is_disable_capture_stdout
```

if you quit PyWatcher, then `ctrl + c`.

examples
-------------

#### standard

```sh
(pywatcher) denzownoMacBook-Pro:pywatcher denzow$ pywatcher -t. -c 'ping localhost'
2018-03-11 23:35:37,114 - INFO - [start process]: ping localhost
2018-03-11 23:35:37,124 - DEBUG - [subprocess_output]: PING localhost (127.0.0.1): 56 data bytes
2018-03-11 23:35:37,124 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.043 ms
2018-03-11 23:35:38,129 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.132 ms
2018-03-11 23:35:39,133 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.161 ms
2018-03-11 23:35:40,138 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.152 ms
2018-03-11 23:35:41,142 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.062 ms
2018-03-11 23:35:42,147 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.095 ms
2018-03-11 23:35:43,141 - INFO - [reload process]: ping localhost  <-- file changed. so reload 
2018-03-11 23:35:43,141 - DEBUG - [subprocess_output]: b''
2018-03-11 23:35:43,141 - INFO - [start process]: ping localhost
2018-03-11 23:35:43,149 - DEBUG - [subprocess_output]: PING localhost (127.0.0.1): 56 data bytes
2018-03-11 23:35:43,149 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.044 ms
2018-03-11 23:35:44,152 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.063 ms
2018-03-11 23:35:45,152 - DEBUG - [subprocess_output]: 64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.048 ms
```

#### more silently

```sh
(pywatcher) denzownoMacBook-Pro:pywatcher denzow$ pywatcher -t. -c 'ping localhost' --disable-capture-stdout
2018-03-11 23:36:12,559 - INFO - [start process]: ping localhost
2018-03-11 23:36:19,136 - INFO - [reload process]: ping localhost  <-- file changed. so reload
2018-03-11 23:36:19,136 - INFO - [start process]: ping localhost
:
```