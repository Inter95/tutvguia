Introduction
===================
It is just a provider for Pulsar (XBMC Addon).
More information about how to write a provider: https://github.com/steeve/script.pulsar.dummy.



Testing the provider without Pulsar
===================

I wrote this script to help to test new providers.

Usage: ./test.py HTTP_PORT METHOD ARG1 "ARG TWO" ARG3 ...
```
./test.py 9001 search divergent
./test.py 9001 search tt1840309
./test.py 9001 search_movie tt1840309 divergent 2014
./test.py 9001 search "spider man"
```
