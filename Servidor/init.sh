#!/bin/bash

python /app/BD/create-database.py 192.168.1.3 3306 
python /app/BD/create-tables.py 192.168.1.3 3306
