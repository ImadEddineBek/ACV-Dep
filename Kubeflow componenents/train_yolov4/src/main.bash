#!/bin/bash
cd "$1"
mkdir results
darknet detector train "$1"/obj.data "$2" "$3" -dont_show  -clear
tar -zcvf results.tar.gz results
mkdir -p /tmp/outputs/output_path/
cp results.tar.gz "$4"
