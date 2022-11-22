#!/bin/bash

docker build -t jnascimento/annotapi .

docker run -it --rm \
-v /hahomes/jnascimento/exps/2022-is-al/datasets/our_events/BangladeshFire:/home/app/static/dataset \
-v /hahomes/jnascimento/exps/2022-annota-interface/annotadb:/home/annotadb \
-p 30193:30193 jnascimento/annotapi /bin/sh
