#!/bin/bash

set -e

cleanup() {
	echo "Exitting..."
	pkill fcgiwrap
}

trap cleanup EXIT

fcgiwrap -s tcp:127.0.0.1:7070 &

uwsgi --emperor "./*/*.ini"

