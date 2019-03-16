#!/bin/bash

export CURDIR=`dirname $0`
PXE_SH=`ls $CURDIR | egrep ^pxe[0-9]+`

chmod +x $PXE_SH

source ${CURDIR}/pxe_config # config
source ${CURDIR}/pxe_func	# function

for SH in $PXE_SH 
do
	if [[ $? != 0  ]];then
		exit 1
	fi

	${CURDIR}/${SH}
done
