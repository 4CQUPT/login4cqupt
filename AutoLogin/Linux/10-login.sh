#!/bin/sh
if [[ $(nmcli -t -f NAME connection show --active) =~ "CQUPT" ]]
then 
  /home/ourongxing/miniconda3/envs/python36/bin/python3 /home/ourongxing/Github/login4cqupt/main.py 1658xxx passxxxx
fi
