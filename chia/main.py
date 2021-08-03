# -*- coding: utf-8 -*-

import os
import sys
import os.path as osp
import time
import yaml
import json

ROOT_PATH = osp.abspath(osp.join(osp.dirname(__file__), '..'))
CA_PATH = osp.abspath(osp.join(osp.dirname(__file__), 'ca'))
CHIA_PATH = osp.join(ROOT_PATH, 'chia-blockchain')
BASE_CONFIG_PATH = osp.join(ROOT_PATH, '.chia/mainnet/config/config.yaml')
Main_Machine_IP = '170.10.0.14'
MOUNT_PATH = '/media/cs'
SUDO_PASSWORD = 'cs888'
FLAG_FILE_PATH = './main_config.yaml'

main_config = {'is_formatted' : True}

def sudo_exec(command, password=SUDO_PASSWORD):
    # sudo exec
    print(f'(exec) sudo {command}')
    os.system('echo %s | sudo -S %s' % (password, command))

def comm_exec(command):
    # common exec
    print(f'(exec) {command}')
    os.system(command)

def get_mkfs_flag():
    # True: 可以被格式化.
    if not osp.isfile(FLAG_FILE_PATH):
        with open(FLAG_FILE_PATH, 'w') as f:
            yaml.dump(main_config, f)
        main_config['is_formatted'] = True
        return True
    else:
        with open(FLAG_FILE_PATH, 'r') as f:
            flag_file_tmp = yaml.load(f, Loader=yaml.FullLoader)
        return not flag_file_tmp['is_formatted']

def Unmounted_drives(d_json):
    um = []
    for i in d_json:
        if 'children' in i.keys():
            um.extend(Unmounted_drives(i['children']))
        else:
            if not i["mountpoint"] and 'T' in i["size"]:
                um.append(i["name"])
    return um

def get_mount_point(mount_path):
    n = 1
    while True:
        is_mounted = os.popen(f'df -h | grep "{mount_path}/{n}"').read()
        if not is_mounted:
            break
        n += 1

    return mount_path + f'/{n}'

def disk_mount():
    disk_list = []
    letter_idx = 0
    disk_condition = os.popen('lsblk -J').read()
    d_json = json.loads(disk_condition)

    for i in Unmounted_drives(d_json["blockdevices"]):
        m_p = get_mount_point(MOUNT_PATH)
        sudo_exec(f'mkdir {m_p}')
        sudo_exec(f'mount /dev/{i} {m_p}')
        sudo_exec('sysctl -w "vm.drop_caches=3"')
    sudo_exec(f'chmod -R 777 {MOUNT_PATH}')

    #for i in range(ord('a'), ord('y') + 1):
    #    if f'sd{chr(i)}2' in disk_condition:
    #        disk_list.append(f'sd{chr(i)}2')
    #    elif f'sd{chr(i)}1' in disk_condition:
    #        disk_list.append(f'sd{chr(i)}1')
    #    elif f'sd{chr(i)}' in disk_condition:
    #        disk_list.append(f'sd{chr(i)}')

    #for i in range(1, len(disk_list) + 1):
    #    sudo_exec(f'mkdir {MOUNT_PATH}/{i}')
    #    sudo_exec(f'mount /dev/{disk_list[i - 1]} {MOUNT_PATH}/{i}')
    #    sudo_exec(f'sysctl -w "vm.drop_caches=3"')

    #sudo_exec(f'chmod -R 777 {MOUNT_PATH}')

def disk_umount():
    # 解除挂载.
    #for i in range(1, 24 + 1):
    #    sudo_exec(f'umount {MOUNT_PATH}/{i}')
        # sudo_exec(f'rm -r {MOUNT_PATH}/{i}')
    os.system("for i in `lsblk | grep media | awk '{print $NF}'`; do sudo umount $i ;done ")

def kill_create_chia():
    # kill 所有chia create进程.
    import psutil
    for process in psutil.process_iter():
        if 'plots' in process.cmdline() and 'create' in process.cmdline():
            print('(print) killing ', end='')
            print(process.cmdline())
            process.terminate()

def start_chia_manager():
    os.chdir(osp.abspath(osp.dirname(__file__)))
    # comm_exec('pip install psutil')
    # comm_exec('pip install dateparser')
    # comm_exec('pip install discord_notify')
    # comm_exec('pip install playsound')
    # comm_exec('pip install pushover')
    comm_exec('python manager.py start')

def stop_chia_manager():
    comm_exec('python manager.py stop')

def modify_harvester_config():
    def judge_suffix_in_list(l, suffix='.plot'):
        for i in l:
            if os.path.splitext(i)[1] == suffix:
                return True
        return False

    print('modify harvester config')
    plot_dir_list = []
    for i in range(1, 24 + 1):
        cur_walk_dir = f'{MOUNT_PATH}/{i}'
        print(f'now {i}')
        for dirpath, dirnames, filenames in os.walk(cur_walk_dir):
            print(dirpath, dirnames, filenames)
            if judge_suffix_in_list(filenames):
                plot_dir_list.append(dirpath)
    # for dirpath, dirnames, filenames in os.walk(MOUNT_PATH):
    #     if judge_suffix_in_list(filenames):
    #         plot_dir_list.append(dirpath)

    with open(BASE_CONFIG_PATH, 'r') as f:
        config_file = yaml.load(f, Loader=yaml.FullLoader)
    config_file['harvester']['plot_directories'] = sorted(plot_dir_list)

    config_file['harvester']['farmer_peer']['host'] = Main_Machine_IP
    config_file['full_node']['enable_upnp'] = False

    with open(BASE_CONFIG_PATH, 'w') as f:
        yaml.dump(config_file, f)
    print('config OK')

def farming_on_many_config():
    os.chdir(CHIA_PATH)
    comm_exec('chia stop all -d')
    comm_exec(f'chia init -c {CA_PATH}')

    # is_harvester_section, is_modified = False, False
    # with open(BASE_CONFIG_PATH, 'r') as f:
    #     base_config_file_tmp = f.readlines()
    #     for i, _ in enumerate(base_config_file_tmp):
    #         if 'enable_upnp' in base_config_file_tmp[i] and 'true' in base_config_file_tmp[i]:
    #             base_config_file_tmp[i] = base_config_file_tmp[i].replace('true', 'false')
    #         if 'harvester:' in base_config_file_tmp[i]:
    #             is_harvester_section = True
    #         if is_harvester_section and 'farmer_peer' in base_config_file_tmp[i] and 'host' in base_config_file_tmp[i + 1]:
    #             base_config_file_tmp[i + 1] = f'    host: {Main_Machine_IP}\n'
    #             is_modified = True
    #             break
    # if not is_modified:
    #     raise Exception('farming_on_many_config(): base config 文件没有被正确配置.')
    # with open(BASE_CONFIG_PATH, 'w') as f:
    #     f.writelines(base_config_file_tmp)

    modify_harvester_config()
    comm_exec('chia start harvester -r')

if __name__ == '__main__':
    #disk_mount()
    if len(sys.argv) == 1:
        disk_mount()
        farming_on_many_config()
    else:
        if '1' in sys.argv:
            disk_mount() # 1
        if '2' in sys.argv:
            farming_on_many_config() # 2
        if '3' in sys.argv:
            disk_umount()

    # stop_chia_manager()
    # kill_create_chia()
    # disk_umount()
