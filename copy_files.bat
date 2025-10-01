@echo off
echo Copying Django files to VM...
scp -r . admin123@172.27.2.132:/home/admin123/app/
echo Files copied successfully!
pause
