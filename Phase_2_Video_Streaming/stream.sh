#!/bin/bash
./mjpg_streamer -o "output_http.so -w ./www"  -i "input_raspicam.so -x 1280 -y 720 -fps 10"

