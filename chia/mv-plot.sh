#!bin/bash


PROC_NUM=8
FIFO_FILE="/tmp/$$.fifo"
mkfifo ${FIFO_FILE}
exec 9<>${FIFO_FILE}
for process_num in $(seq ${PROC_NUM})
do
	echo "$(date +%F\ %T) Processor-${process_num} " >&9
done


for i in `seq 1 782`
do
	read -u 9 P
	{
		echo "${P}"
		_line_p=`sed -n "${i}p" left_stack_random`
		_line_m=`sed -n "${i}p" mv_plots_random`

		src_host=`echo $_line_m | awk '{print $1}'`
		src_plots=`echo $_line_m | awk '{print $2}'`

		dest_host=`echo $_line_p | awk '{print $1}'`
		dest_plots=`echo $_line_p | awk '{print $2}'`/`echo $src_plots | awk -F'/' '{print $NF}'`

		_tmp_playbook_=$i-`date +%d-%H-%M-%S-%N`
		cat > playbook/$_tmp_playbook_ <<EOF
- hosts: $dest_host
  gather_facts: no
  tasks:
    - synchronize:
        src: $src_plots
        dest: $dest_plots
      delegate_to: $src_host
EOF
		echo "ansible-playbook playbook/$_tmp_playbook_ > playbook/${_tmp_playbook_}.log"
		ansible-playbook playbook/$_tmp_playbook_ > playbook/${_tmp_playbook_}.log
		echo ${P} >&9
	} &
done


wait
echo "All Completed"
exec 9>&-
rm -f ${FIFO_FILE}
