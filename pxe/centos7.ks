#version=DEVEL
install
auth --enableshadow --passalgo=sha512
text
lang en_US.UTF-8
keyboard --vckeymap=us --xlayouts='us'
network --onboot=on --device=ens33  --bootproto=dhcp --activate --ipv6=auto
rootpw --iscrypted  $1$tjDtFUYd$H6Mil6cJXY5bg3Cuvh9rS.
firewall --disabled
url --url=http://%s/iso
selinux --disabled
timezone Asia/Shanghai --isUtc
bootloader --location=mbr --driveorder=sda --append="crashkernel=auto"
zerombr
clearpart --none --initlabel
reboot
part /boot --fstype=ext4 --ondisk=sda --size=400
part swap  --ondisk=sda --size=4000
part / --fstype=ext4 --ondisk=sda --grow --size=200
 
%packages
@^minimal
@core
httpd
vsftpd
%end
 
%addon com_redhat_kdump --disable --reserve-mb='auto'
 
%end
