# Runs the installs, 

pip_installs="requirements.txt"
apt_installs="apt-get_installs.txt"

while read p; do
  echo "|sudo apt-get install $p|"
  sudo apt-get install $p -y
done <$apt_installs


python3 -m venv dev; source dev/bin/activate
pip --version
pip3 --version
pip install -r $pip_installs

echo "You'll need to download a display software! More Windows/Linux crossover stuff"
echo "https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/"