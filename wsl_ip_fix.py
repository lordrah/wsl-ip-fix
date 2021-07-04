from WSLIpFixer import WSLIpFixer
import config

if __name__ == '__main__':
    fixer = WSLIpFixer(config.config)
    fixer.fix()
