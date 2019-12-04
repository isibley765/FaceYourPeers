# Runs the installs, 

pip_installs="requirements.txt"
apt_installs="apt-get_installs.txt"


cat $apt_installs | xargs sudo apt-get install

python3 -m venv ./dev/; source dev/bin/activate
pip install -r $pip_installs