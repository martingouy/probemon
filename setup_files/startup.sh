# startup script for sniffer

# 1) pull updated repo from git
cd ~/sniffing/probemon/
git pull 

# 2) copy supervisor config files
cp pythonhook.conf /etc/supervisor/conf.d/

# 3) start process
supervisorctl stop pythonsniff
supervisorctl update
supervisorctl start pythonsniff
