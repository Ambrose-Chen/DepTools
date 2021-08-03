#!/bin/bash

PROC_NUM=20
FIFO_FILE="/tmp/$$.fifo"
mkfifo ${FIFO_FILE}
exec 9<>${FIFO_FILE}

for process_num in $(seq ${PROC_NUM})
do
	echo "$(date +%F\ %T) Processor-${process_num} " >&9
done

ready_to_delete_file='A0719.hi_rm'
line_num=`cat $ready_to_delete_file | wc -l`

for i in `seq 1 $line_num`
do
	read -u 9 P
	{
		host=`cat $ready_to_delete_file | sed -n "${i}p" | awk '{print $1}'`
		plot=`cat $ready_to_delete_file | sed -n "${i}p" | awk '{print $2}'`
		ansible $host -m file -b -a "path=$plot state=absent"
		echo ${P} >&9
	} &
done

wait
echo "All Completed"
exec 9>&-
rm -f ${FIFO_FILE}
exit 0
