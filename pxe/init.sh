#!/bin/bash

export baseurl=`cd $(dirname $0) ; pwd`

source $baseurl/common
source $baseurl/config

sed -i "s/{filePath}/`echo $mount_addr | sed 's/\//\\\\\//g'`/g"  $baseurl/base.repo
cp $baseurl/base.repo /etc/yum.repos.d/

[ -d $mount_addr ]
step_check "config: mount directory ------ exist" "config: mount directory ------ not exist" 1

check_cdrom
step_check "cdrom ------ yes" "cdrom ------ no" 1

check_mount '/dev/sr0'
step_check "/dev/sr0 not mount yet" "/dev/sr0 already mounted" 1

mount /dev/sr0 $mount_addr >/dev/null 2>&1

check_yum
step_check  "yum ------ sccess" "yum ------ error" 1

yum -y install \
                bash-completion \
                wget \
                vim \
                &>/dev/null

                
echo_green "init sccessful"

umount $mount_addr