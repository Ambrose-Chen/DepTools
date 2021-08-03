import yaml

config_path = '~/.chia/mainnet/config/config.yaml'

with open(config_path, 'r') as f:
    config_file = yaml.load(f, Loader=yaml.FullLoader)

cur_plot_dir = config_file['harvester']['plot_directories']
cur_plot_dir.append('/media/cs/1')
config_file['harvester']['plot_directories'] = sorted(list(set(cur_plot_dir)))

print(config_file['harvester']['plot_directories'])
