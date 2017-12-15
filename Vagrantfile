# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # config.vm.provision :shell, path: "pg_config.sh"
  config.vm.box = "bento/ubuntu-16.04-i386"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"


  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update

    # Work around https://github.com/chef/bento/issues/661
    # apt-get -qqy upgrade
    DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

    apt-get -qqy install make zip unzip postgresql

    apt-get -qqy install python3 python3-pip

    pip3 install virtualenv
    pip3 install --upgrade pip
    pip3 install virtualenv

    virtualenv /vagrant/venv -p /usr/bin/python3.5 --always-copy
    source /vagrant/venv/bin/activate

    # Should now be running in virtual environment
    pip install flask
    pip install --upgrade pip
    pip install flask packaging oauthlib flask-oauthlib
    pip install oauth2client flask-httpauth flask-login passlib
    pip install flask-bootstrap flask-moment flask-mail flask-wtf
    pip install sqlalchemy flask-sqlalchemy bleach
    pip install httplib2
    pip install validate_email
    pip install coverage
    #pip install redis
    pip install psycopg2

    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd

    #wget http://download.redis.io/redis-stable.tar.gz
    #tar xvzf redis-stable.tar.gz
    #cd redis-stable
    #make
    #make install

    echo "Done installing your virtual machine!"
  SHELL
end
