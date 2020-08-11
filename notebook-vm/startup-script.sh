#! /bin/bash
echo "running startup script"

echo "Apt get upgrade"
sudo apt-get upgrade -y

if  [ ! -d "/home/jupyter/" ]; then
  mkdir /home/jupyter/
  echo "created /home/jupyter/"
else
  echo "/home/jupyter was already created."
fi


PROJ=$(gcloud config list --format 'value(core.project)')
mkdir /home/jupyter/.ssh
gcloud secrets versions access latest --secret="$PROJ"-private-key-secret > /home/jupyter/.ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add /home/jupyter/.ssh/id_rsa
chmod 400 /home/jupyter/.ssh/id_rsa
ssh-keyscan github.com >> /home/jupyter/.ssh/known_hosts
sudo chown jupyter: /home/jupyter/.ssh//id_rsa

if  [ ! -f "/home/jupyter/notebook.ipynb" ]; then
  wget  -O /home/jupyter/notebook.ipynb "https://raw.githubusercontent.com/vwt-digital/notebook-deployment/develop/notebook-vm/notebook.ipynb"
  echo "downloaded notebook"
fi

export HOME=/home/jupyter
mkdir /home/jupyter/.git-commit-hooks
wget  -O /home/jupyter/.git-commit-hooks/commit-msg "https://raw.githubusercontent.com/vwt-digital/commit-hooks/develop/hooks/commit-msg"
sudo chmod a+x /home/jupyter/.git-commit-hooks/commit-msg
git config --global core.hooksPath /home/jupyter/.git-commit-hooks
echo "configured the commit-hook"
