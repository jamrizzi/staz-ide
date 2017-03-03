#!/usr/bin/env python2

import sys
import os
import platform
import fileinput
from helper import Helper
helper = Helper()

def main():
    helper.is_root()
    options = gather_information(get_defaults())
    helper.prepare()
    install_spacemacs(options)
    install_tmux(options)
    install_zshrc(options)

def get_defaults():
    return {}

def gather_information(defaults):
    options = {
        user: os.environ['SUDO_USER'] if 'SUDO_USER' in os.environ else os.environ['USER']
    }
    return options

def install_powerline(options):
    os.system('pip install powerline-status')
    helper.user_system('''
    curl -O https://raw.githubusercontent.com/jamrizzi/staz-ide/master/tmux/.tmux.conf
    curl -O https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
    curl -O https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf
    mv PowerlineSymbols.otf ~/.fonts/
    fc-cache -vf ~/.fonts/
    mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
    cp -r /usr/share/powerline/config_files/ ~/.config/powerline/
    ''')
    os.system('''
    curl -O https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
    curl -O https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf
    mv PowerlineSymbols.otf /root/.fonts/
    fc-cache -vf /root/.fonts/
    mv 10-powerline-symbols.conf /root/.config/fontconfig/conf.d/
    ln -s /home/''' + options['user'] + '''/.config/powerline/ /root/.config/powerline/
    ''')

def install_tmux(options):
    if (platform.dist()[0] == 'centos'):
        os.system('yum install -y tmux')
    elif (platform.dist()[0] == 'Ubuntu'):
        os.system('apt-get install -y tmux')
    else:
        print('Operating system not supported')
        sys.exit('Exiting installer')
    helper.system('git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm')
    os.system('ln -s /home/' + options['user'] + '/.tmux/ /root/.tmux/')
    helper.append_to_user_file('~/.zshrc', '''
    if [[ -z "\$TMUX" ]]; then
      tmux
    fi
    ''')

def install_zshrc(options):
    if (platform.dist()[0] == 'centos'):
        os.system('yum install -y zsh')
    elif (platform.dist()[0] == 'Ubuntu'):
        os.system('apt-get install -y zsh')
    else:
        print('Operating system not supported')
        sys.exit('Exiting installer')
    helper.user_system('''
    curl -L https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
    git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k/
    ''')
    helper.find_replace('~/.zshrc', 'ZSH_THEME="robbyrussell"', 'ZSH_THEME="powerlevel9k/powerlevel9k"')
    os.system('''
    curl -L https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
    git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k/
    ''')
    helper.find_replace('/root/.zshrc', 'ZSH_THEME="robbyrussell"', 'ZSH_THEME="powerlevel9k/powerlevel9k"')

def install_spacemacs(options):
    if (platform.dist()[0] == 'centos'):
        os.system('yum install -y emacs')
    elif (platform.dist()[0] == 'Ubuntu'):
        os.system('apt-get install -y emacs')
    else:
        print('Operating system not supported')
        sys.exit('Exiting installer')
    helper.user_system('''
    git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d
    touch ~/.spacemacs
    ''')
    os.system('''
    ln -s /home/''' + options['user'] + '''/.emacs.d /root/.emacs.d
    ln -s /home/''' + options['user'] + '''/.spacemacs /root/.spacemacs
    ''')

main()