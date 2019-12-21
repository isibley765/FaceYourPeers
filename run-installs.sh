# Runs the installs, 

pip_installs="requirements.txt"
apt_installs="apt-get_installs.txt"

while read p; do
  echo "|sudo apt-get install $p|"
  sudo apt-get install $p
done <$apt_installs


python3 -m venv dev; source dev/bin/activate
pip --version
pip3 --version
pip install -r $pip_installs