import os
import linecache


def get_cluster_plots_ansible_based(input_file):
    os.system(' '.join([
        "ansible 'all' -m shell -b -a 'find /media/ -type f -name *plot -exec ls -l {} \;' >",
        input_file
        ]))
    #os.system(' '.join([
    #    "ansible 'all:!chia-170-10-0-48' -m shell -b -a 'find /media/ -type f -name *plot -exec ls -l {} \;' >",
    #    input_file
    #    ]))
    #os.system(' '.join([
    #    "ansible chia-170-10-0-48 -m shell -b -a 'find /media/cs/{[1-9],[1-9][^0]*} -type f -name *plot -exec ls -l {} \;' >>",
    #    input_file
    #    ]))


def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()

def ansible_plots_file_handle(input_file, output_file):
    with open(output_file, 'w') as wf:
        host_name = ''
        line_number = 1
        while True:
            line = get_line_context(input_file, line_number)
            if 'chia-' in line:
                host_name = line.split()[0]
                line_number += 1
                continue

            if line[-4:] == 'plot':
                _tmp_ = line.split()
                abs_plot = _tmp_[len(_tmp_) - 1]

                _tmp_ =abs_plot.split('/')
                plot_name = _tmp_[len(_tmp_) - 1]

                _tmp_ = abs_plot.split('/')
                _tmp_[len(_tmp_) - 1] = ''
                plot_dir = '/'.join(_tmp_)
                
                _tmp_ = line.split()
                _tmp_[len(_tmp_) - 1] = ''
                other_para = ' '.join(_tmp_)

                wf.writelines(plot_name + ' ' + host_name + ' ' + plot_dir + ' ' + other_para + '\n')
            else:
                print(line)

            if not line:
                break

            line_number += 1

def find_Invalid_plots(input_file, output_file):
    with open(output_file, 'w') as wf:
        line_number = 1
        while True:
            line = get_line_context(input_file, line_number)
            if not line:
                break

            if int(line.split()[7]) < 108000000000:
                wf.writelines(line + '\n')

            line_number += 1

def sort_file(input_file, output_file):
    os.system(' '.join([
            'cat',
            input_file,
            '| sort -u >',
            output_file
        ]))

def find_repeat_plots(input_file, output_file):
    with open(output_file + '.tmp', 'w') as wf:
        line_number = 1
        pre_plot_name = ''
        while True:
            line = get_line_context(input_file, line_number)

            if not line:
                break

            plot_name = line.split()[0]
            if pre_plot_name == plot_name:
                wf.writelines(get_line_context(input_file, line_number - 1) + '\n')
                wf.writelines(line + '\n')

            pre_plot_name = plot_name
            line_number += 1

    sort_file(output_file + '.tmp', output_file)

def ready_to_delete(input_file, output_file):
    with open(output_file, 'w') as wf:
        line_number = 1
        while True:
            line = get_line_context(input_file, line_number)
            if not line:
                break
            plot_name = line.split()[0]
            host_name = line.split()[1]
            plot_dir = line.split()[2]
            wf.writelines(host_name + ' ' + plot_dir + plot_name + '\n')

            line_number += 1

def ready_to_delete_by_repeat(input_file, output_file):
    with open(output_file, 'w') as wf:
        line_number = 1
        a_plot_name = []
        a_host_name = []
        a_plot_dir = []
        while True:
            line = get_line_context(input_file, line_number)

            if not line:
                
                if a_plot_name:
                    for index, item in enumerate(a_host_name):
                        if a_host_name[index] not in 'chia-170-10-0-32 chia-170-10-0-33 chia-170-10-0-34' or (a_host_name[index] == 'chia-170-10-0-35' and '22' in a_plot_dir[index]):
                            a_plot_name.pop(index)
                            a_host_name.pop(index)
                            a_plot_dir.pop(index)
                            break

                    if len(a_plot_name) > 0:
                        for i in range(len(a_plot_name)):
                            wf.writelines(a_host_name[i] + ' ' + a_plot_dir[i] + a_plot_name[i] + '\n')

                break

            plot_name = line.split()[0]
            host_name = line.split()[1]
            plot_dir = line.split()[2]

            if a_plot_name and a_plot_name[0] == plot_name:
                a_plot_name.append(plot_name)
                a_host_name.append(host_name)
                a_plot_dir.append(plot_dir)
            else:
                if a_plot_name:
                    for index, item in enumerate(a_host_name):
                        if a_host_name[index] not in 'chia-170-10-0-32 chia-170-10-0-33 chia-170-10-0-34' or (a_host_name[index] == 'chia-170-10-0-35' and '22' in a_plot_dir[index]):
                            a_plot_name.pop(index)
                            a_host_name.pop(index)
                            a_plot_dir.pop(index)
                            break

                    if len(a_plot_name) > 0:
                        for i in range(len(a_plot_name)):
                            wf.writelines(a_host_name[i] + ' ' + a_plot_dir[i] + a_plot_name[i] + '\n')

                a_plot_name = [plot_name]
                a_host_name = [host_name]
                a_plot_dir = [plot_dir]


            line_number += 1


if __name__ == '__main__':
    full_plots_file = './A0719'
    full_plots_file_handle = full_plots_file + '.h'
    Invalid_plots_file = full_plots_file_handle + 'i'
    full_plots_file_sort = full_plots_file_handle + 's'
    repeat_plots_file = full_plots_file_sort + 'r'
    ready_to_delete_repeat_file = repeat_plots_file + '_rm'
    ready_to_delete_Invalid_file = Invalid_plots_file + '_rm'

    print("get_cluster_plots_ansible_based")
    get_cluster_plots_ansible_based(full_plots_file)
    print("ansible_plots_file_handle")
    ansible_plots_file_handle(full_plots_file, full_plots_file_handle)

    print("find_Invalid_plots")
    find_Invalid_plots(full_plots_file_handle, Invalid_plots_file)
    print("ready_to_delete")
    ready_to_delete(Invalid_plots_file, ready_to_delete_Invalid_file)
    

    print("sort_file")
    sort_file(full_plots_file_handle, full_plots_file_sort)
    print("find_repeat_plots")
    find_repeat_plots(full_plots_file_sort, repeat_plots_file)
    print("ready_to_delete_by_repeat")
    ready_to_delete_by_repeat(repeat_plots_file, ready_to_delete_repeat_file)
