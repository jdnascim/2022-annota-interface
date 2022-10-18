#!/bin/bash

dataset_path=/hahomes/jnascimento/exps/2022-is-al/datasets/our_events/BangladeshFire/

docker run -it --rm -p 30193:30193 -v $dataset_path:/home/dataset jnascimento/annotapi
