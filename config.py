def get_config(field_name: str) -> str:
    with open('config.txt', 'r') as config_file:
        lines = [x.strip() for x in config_file.readlines()]
        for line in lines:
            if len(line) == 0:
                continue
            if line.count("\"") != 2:
                continue
            k,v,_ = line.split("\"")
            if field_name == k.strip():
                return v.strip()

    return None

if __name__=='__main__':
    pass