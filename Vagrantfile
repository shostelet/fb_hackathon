# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |django_config|
  # Every Vagrant virtual environment requires a box to build off of.
  django_config.vm.box = "ubuntu/trusty64"

  # Configure virtual machine specs. Keep it simple, single user.
  django_config.vm.provider :virtualbox do |p|
    p.customize ["modifyvm", :id, "--memory", 2048]
    p.customize ["modifyvm", :id, "--cpus", 2]
    p.customize ["modifyvm", :id, "--cpuexecutioncap", 50]
  end

  # Configure a synced folder between HOST and GUEST
  django_config.vm.synced_folder ".", "/vagrant", :nfs => true, :mount_options => ["actimeo=1"]

  # Config hostname and IP address so entry can be added to HOSTS file
  django_config.vm.hostname = "vagrant"
  django_config.vm.network :private_network, ip: '192.168.99.100'

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  django_config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  django_config.vm.network "forwarded_port", guest: 8004, host: 8004, host_ip: "127.0.0.1"

  # kickoff a shell script to install Python essentials
  django_config.vm.provision :shell, path: "provision.sh"
end