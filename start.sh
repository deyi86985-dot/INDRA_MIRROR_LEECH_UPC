#!/bin/bash

cd /app

aria2c --enable-rpc \
       --rpc-listen-port=6800 \
       --rpc-listen-all=false \
       --daemon=true

exec /app/mltbenv/bin/python -m bot
