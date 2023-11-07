#!/bin/bash

case "$OSTYPE" in
solaris*)
	OS="SOLARIS"
	;;
darwin*)
	OS="OSX"
	;;
linux*)
	OS="LINUX"
	PYTHON_RUN="venv/bin/python3"
	;;
bsd*)
	OS="BSD"
	;;
msys*)
	OS="WINDOWS"
	PYTHON_RUN="venv/Scripts/python.exe"
	;;
*)
	echo "unknown: $OSTYPE"
	;;
esac

usage() {
	printf "\nUsage: run [option] \n\n"
	printf "    -p <port> \t Set a port (default: 4242)\n"
	printf "    -r <path> \t Run server with custom BIN path\n"
	printf "    -s  \t Run server with virtual env '$PYTHON_RUN'\n"
	printf "        \t   OS detected: '$OS'\n"
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
		PYTHON=$PYTHON_RUN
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
