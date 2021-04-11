#!/bin/sh
if [[ $(nmcli -t -f NAME connection show --active) =~ "CQUPT" ]]
then 
  python ~/Github/login4cqupt/main.py 1658xxxx passxxxx
fi
