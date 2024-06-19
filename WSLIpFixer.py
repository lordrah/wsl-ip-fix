import subprocess


class WSLIpFixer(object):
    def __init__(self, _config):
        self.config = _config

    @staticmethod
    def __get_wsl_host_ip():
        ip = subprocess.check_output("ip route list default | awk '{print $3}'", shell=True)
        return ip.strip()

    @staticmethod
    def __get_wsl_ip():
        output = subprocess.check_output(["ip", "addr"])
        output_lines = output.decode('utf-8').split("\n")

        found_eth0 = False
        wsl_ip = None
        for line in output_lines:
            if not found_eth0:
                found_eth0 = line.find('eth0:') != -1
            else:
                line_parts = line.split(':')
                if len(line_parts) == 0 or line_parts[0].isdigit():
                    # Break if looking at the next section
                    break

                if line.find('inet ') != -1:
                    line_parts = line.split(' ')
                    valid_part_count = 0
                    for part in line_parts:
                        if part == '':
                            continue
                        if valid_part_count == 0:
                            valid_part_count = valid_part_count + 1
                        elif valid_part_count == 1:
                            ip_parts = part.split('/')
                            wsl_ip = ip_parts[0]
                            break
        return wsl_ip

    @staticmethod
    def validate_ip(s):
        a = s.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    @staticmethod
    def find_with_list(string, str_list):
        check = False
        for item in str_list:
            check = string.find(item) != -1
            if check:
                break
        return check

    def __get_ip_domains(self, config_key):
        domains = []
        if config_key in self.config:
            domains = self.config[config_key]
            if not isinstance(domains, list):
                domains = [str(domains)]

        return domains

    def fix_host_file(self, config_key, wsl_ip, wsl_host_ip):
        if config_key not in self.config:
            return

        wsl_host_ip_domains = self.__get_ip_domains('wsl_host_ip_domains')
        wsl_ip_domains = self.__get_ip_domains('wsl_ip_domains')

        with open(self.config[config_key], 'r') as reader:
            line_list = reader.readlines()
            for j in range(len(line_list)):
                formatted_line = line_list[j].replace('\t', ' ')
                line_parts = formatted_line.split(' ')

                i = 0
                while i < len(line_parts):
                    if line_parts[i] != '' and not line_parts[i].isspace():
                        break
                    i = i + 1
                else:
                    continue

                if line_parts[i] == '#':
                    continue

                k = i + 1
                while k < len(line_parts):
                    if line_parts[k] != '' and not line_parts[k].isspace():
                        break
                    k = k + 1

                # check if part is ip
                if self.validate_ip(line_parts[i]) and k < len(line_parts):
                    if self.find_with_list(line_parts[k], wsl_host_ip_domains):
                        line_list[j] = line_list[j].replace(line_parts[i], wsl_host_ip)
                    elif self.find_with_list(line_parts[k], wsl_ip_domains):
                        line_list[j] = line_list[j].replace(line_parts[i], wsl_ip)

        with open(self.config[config_key], 'w') as reader:
            reader.writelines(line_list)

    def fix(self):
        wsl_ip = self.__get_wsl_ip()
        wsl_host_ip = self.__get_wsl_host_ip()

        self.fix_host_file('win_host_file_path', wsl_ip, wsl_host_ip)
        self.fix_host_file('wsl_host_file_path', wsl_ip, wsl_host_ip)
