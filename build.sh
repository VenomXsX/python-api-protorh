#!/bin/bash

if ! command -v python3 >/dev/null 2>&1 ; then
    printf "Python3 is not installed.\n"
    exit 1
fi

if ! command -v pip3 >/dev/null 2>&1 ; then
    printf "pip3 is not installed.\n"
    exit 1
fi

if ! command -v psql >/dev/null 2>&1 ; then
    printf "psql is not installed.\n"
    exit 1
fi

printf "Installing requirements...\n"
pip3 install -r requirements.txt

printf "Connecting to database and creating tables...\n"
psql postgresql://postgres:qXCt0DjuTjAnWonp@db.ubxhmfytehqpagvhclub.supabase.co:5432/ -f protorh/database_rh.psql