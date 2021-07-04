## WSL IP Address Fixer
This script helps in fixing the Windows Subsystem Linux (WSL) IP address in the host files (ie. the Windows and WSL host files) whenever your whole system or just the WSL is restarted since the WSL IP address always changes. This is particularly useful if you have set up virtual hosts on your WSL and need to point these virtual hosts to the current WSL's IP address in the hosts file in order to access them on your browser. It also helps in fixing the WSL-Host IP address if you need access the Windows IP address from within the WSL.

### Dependencies
Python needs to be installed on the WSL. It works with Python 2.7 and Python3.*. No third-party library used.

### Configuration
The default configuration for the script can be found in the `config.py` file. The following is the default setting:

    {  
      "win_host_file_path": "/mnt/c/WINDOWS/system32/drivers/etc/hosts",  
	  "wsl_host_file_path": "/etc/hosts",  
	  "wsl_ip_domains": ["local."],  
	  "wsl_host_ip_domains": ["wsl2.host"]  
	}

| Parameter | Description |
|--|--|
| win_host_file_path | The Windows host file path |
| wsl_host_file_path| The WSL host file path |
| wsl_ip_domains| A list of domains whose IP addresses are to be updated with the current WSL IP address in a host file |
| wsl_host_ip_domains| A list of domains whose IP addresses are to be updated with the current WSL-Host (ie. Windows) IP address in a host file |

The script fixes the IP addresses in the Windows and WSL host files whose paths are specified using `win_host_file_path` and `wsl_host_file_path` respectively. 

In order to target the domains within the hosts file to be updated with the current WSL IP address, use `wsl_ip_domains`. For the domains that need to be updated with the current WSL-Host IP address, use `wsl_host_ip_domains`. `wsl_ip_domains` and `wsl_host_ip_domains` can also contain parts of a domain in order to target more than one domain which contain that string. Eg. if you use `local.` it will target `local.example.com` and `local.ping.com`.

### Usage
Git pull the project into your WSL , `cd` to the directory then you can run the following in the WSL terminal:

    python wsl_ip_fix.py
or

    bash wsl-ip-fix.sh

**NOTE: Ensure that you are running the WSL Terminal as Administrator in order to save the Windows Host file.** 