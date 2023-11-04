#!/bin/bash

usage() {
	printf "\nUsage: run [option] \n\n"
	printf "    -p <port> \t Set a port (default: 4242)\n"
	printf "    -r <path> \t Run server with custom BIN path\n"
	printf "    -s  \t Run server with 'venv/bin/python3'\n"
	printf "\n"
}

PYTHON="python3"

while getopts ":p:r:hs" option; do
	HAS_OPTION=1
	case "${option}" in
		p)
			PORT=${OPTARG}
			;;
		r)
			PYTHON=${OPTARG}
			;;
		s)
			PYTHON="venv/bin/python3"
			;;
		d)
			DIR=${OPTARG}
			;;
		h)
			usage
			exit 1
			;;
		:)
			echo "Err: args are required for: -$OPTARG"
			usage
			exit 1
			;;
		*)
			echo "Invalid options: -$OPTARG"
			usage
			exit 1
			;;
  esac
done

$PYTHON protorh/main.py $PORT # custom port