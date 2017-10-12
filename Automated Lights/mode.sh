#!/bin/bash

file_dir="/tmp/lights.state"

if [[ -f "/tmp/lights.state" ]];
then
	current_mode="$(cat $file_dir)"
	if [ "$current_mode" = "manual" ];
	then
		echo "automatic" > $file_dir
		echo "Mode: Automatic"
	elif [ "$current_mode" = "automatic" ];
	then
                echo "manual" > $file_dir
                echo "Mode: Manual"
	fi
fi
