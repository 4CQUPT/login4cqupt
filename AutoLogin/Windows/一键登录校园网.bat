@echo off
@for /f "tokens=1,2,3" %%i in ('netsh WLAN show interfaces') do (
    if [%%i]==[SSID] set ssid=%%k
)
if "%ssid:CQUPT=%"=="%ssid%" (echo) else C:\ProgramData\Miniconda3\envs\py36\python.exe D:\Desktop\Github\login4cqupt\main.py 1658xxx Tenderxxxxxx