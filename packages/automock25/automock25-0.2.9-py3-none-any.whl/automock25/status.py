import configparser


def get_config_params():
    # 读取 config.ini 文件
    config = configparser.ConfigParser()
    config_file_path = 'config.ini'

    try:
        with open(config_file_path, 'r', encoding='utf-8') as config_file:
            config.read_file(config_file)

        config_params = dict(config['DEFAULT'])
        return config_params
    except FileNotFoundError:
        print(f"Error: {config_file_path} not found.")
        return {}
    except Exception as e:
        print(f"Error reading {config_file_path}: {e}")
        return {}


