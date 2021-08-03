#!/bin/bash

mv_plots_file='323334.txt'
space_left='space_left.txt'

ansible chia-170-10-0-32,chia-170-10-0-33,chia-170-10-0-34 -m shell -a 'find /media/ -type f -name *plot | sort -t "/" -k 4n' > $mv_plots_file

line_num=`cat $mv_plots_file | wc -l`

> mv_plots

for n in `seq 1 $line_num`
do
	_line_=`sed -n "${n}p" $mv_plots_file`
	if [[ "$_line_" =~ "chia" ]];then
		_host_=`echo "$_line_" | awk '{print $1}'`
		continue
	fi
	echo "$_host_ $_line_" >> mv_plots
done

ansible-playbook df.yml | grep -wE '^ok|stdout' | sed  's/ => {//g' | sed 's/ok: \[//g' | sed 's/\]//g' | sed 's/"stdout": "//g' | sed 's/",//g'| grep -v '^\ *$' > $space_left

_line_num_=`cat $space_left | wc -l`

> left_stack

for i in `seq 1 $_line_num_`
do
	_line_=`sed -n "${i}p" $space_left`
	if [[ "$_line_" =~ "chia" ]];then
		_host_="$_line_"
		continue
	fi

	for x in $(seq 1 `echo -e "$_line_" | wc -l`)
	do
		__line__=`echo -e "$_line_" | sed -n "${x}p"`
		__num__=`echo -e "$__line__" | awk '{print $1}'`
		__path__=`echo "$__line__" | awk '{print $2}'`
		echo "$_host_ $__num__ $__path__"
		for y in `seq 1 $__num__`
		do
			echo "$_host_ $__path__" | grep -v "chia-170-10-0-73 /media/cs/1" >> left_stack
		done
	done
done


#for i in `seq 1 324`
#do
#	_line_=`sed -n "${i}p" disk-.txt`
#	loop_count=`echo "$_line_" | awk '{print $1}'`
#	host=`echo "$_line_" | awk '{print $2}'`
#	dir=`echo "$_line_" | awk '{print $3}'`
#	
#	for x in `seq $loop_count`
#	do
#		echo "$host $dir $x"
#	done
#done
