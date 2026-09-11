# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

fpath=(/usr/local/share/zsh-completions $fpath)

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="agnoster" 

DEFAULT_USER="$USER"

# gianrtx is the Ubuntu box; anything else is the Mac.
IS_MAC=true
[[ "$HOST" == 'gianrtx' ]] && IS_MAC=false

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

setopt APPEND_HISTORY

# Add env.sh
source ~/Dropbox/Mac/env.sh

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/copyfile
plugins=(aws git git-auto-fetch extract colorize github colored-man-pages brew macos zsh-completions zsh-autosuggestions zsh-syntax-highlighting npm asdf copyfile virtualenv)

#if [[ DEFAULT_USER == 'gpalumbo' ]]; then
#    plugins+=(adb)
#else
#    plugins+=(adb)
#fi

export GIT_AUTO_FETCH_INTERVAL=3600

source $ZSH/oh-my-zsh.sh

AGNOSTER_PROMPT_SEGMENTS[1]=

# Load RVM into a shell session *as a function*
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"
# This loads NVM
# Defer initialization of nvm until nvm, node or a node-dependent command is
# run. Ensure this block is only run once if .bashrc gets sourced multiple times
# by checking whether __init_nvm is a function.
#if [ -s "$HOME/.nvm/nvm.sh" ] && [ ! "$(whence -w __init_nvm)" = function ]; then
#  export NVM_DIR="$HOME/.nvm"
#  [ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"
#  declare -a __node_commands=('nvm' 'node' 'npm' 'yarn' 'react-native' 'npx' 'browser-sync' 'm' 'lt' 'tldr' 'npm-check' 'snyk' 'expo' 'amplify')
#  function __init_nvm() {
#    for i in "${__node_commands[@]}"; do unalias $i; done
#    . "$NVM_DIR"/nvm.sh
#    unset __node_commands
#    unset -f __init_nvm
#  }
#  for i in "${__node_commands[@]}"; do alias $i='__init_nvm && '$i; done
#fi

autoload -U compinit && compinit

# Customize to your needs...
PATH=${HOME}/Library/Python/2.7/bin:$PATH
PATH=${HOME}/Library/Python/3.7/bin:$PATH
PATH=/usr/local/opt/openssl/bin:$PATH
PATH=/usr/local/sbin:$PATH
PATH=${HOME}/bin:$PATH
PATH=/usr/local/opt/qt/bin:$PATH
PATH=/usr/local/opt/findutils/libexec/gnubin:$PATH

# golang
PATH=${HOME}/go/bin:$PATH

unsetopt correct_all
unsetopt share_history # share command history data
# unsetopt inc_append_history

if $IS_MAC; then
    # Android development
    export ANDROID_HOME=$HOME/Library/Android/sdk
    export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools
    export JAVA_HOME="$(/usr/libexec/java_home)"
    export JDK_HOME="$(/usr/libexec/java_home)"
fi

# # To enable shims and autocompletions
# if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
# # To enable auto-activation
# if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi

# for ec2-api-tools ec2-ami-tools
#export EC2_HOME="/usr/local/opt/ec2-api-tools/jars/"
#export EC2_PRIVATE_KEY="$HOME/.ssh/id_rsa"
#export EC2_CERT="$HOME/.ssh/id_rsa.pub"
#export EC2_CERT="$(/bin/ls "$HOME"/.ec2/cert-*.pem | /usr/bin/head -1)"
#export EC2_AMITOOL_HOME="/usr/local/Library/LinkedKegs/ec2-ami-tools/jars"

#export AWS_ACCESS_KEY=
#export AWS_SECRET_KEY=

# yarn-completion
[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion

# eval "$(rbenv init -)"

# for react-native debugging emulator/simulator opening the Code editor
REACT_EDITOR=zed

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Python
pip-save ()
{
    for pkg in $@;
    do
        pip install "$pkg" && {
            name="$(pip show "$pkg" | grep Name: | awk '{print $2}')";
            version="$(pip show "$pkg" | grep Version: | awk '{print $2}')";
            echo "${name}==${version}" >> requirements.txt
        };
    done
}

# tabtab source for packages
# uninstall by removing these lines
[[ -f ~/.config/tabtab/__tabtab.zsh ]] && . ~/.config/tabtab/__tabtab.zsh || true

#source ~/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
[ -f $HOME/.cargo/env ] && source $HOME/.cargo/env


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/homebrew/Caskroom/miniconda/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
        . "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
    else
        export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

PATH="/opt/homebrew/opt/mongodb-community@7.0/bin:$PATH"

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
PATH="$BUN_INSTALL/bin:$PATH"

eval "$(starship init zsh)"

source $HOME/.aliases

PATH="$HOME/.deno/bin:$PATH"

# pnpm
if $IS_MAC; then
  export PNPM_HOME="$HOME/Library/pnpm"
else
  export PNPM_HOME="$HOME/.local/share/pnpm"
fi
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

PATH="/opt/homebrew/opt/rustup/bin:$PATH"

[ -f "$HOME/.local/bin/env" ] && . "$HOME/.local/bin/env"
[ -f uv ] && eval "$(uv generate-shell-completion zsh)"
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"

# limbo sqlite turso
[ -f "$HOME/.limbo/env" ] && . "$HOME/.limbo/env"

# LM Studio CLI (lms)
if $IS_MAC; then
  export PATH="$PATH:$HOME/.lmstudio/bin"
fi

# GPG git SSH key
export GPG_TTY=$(tty)

export PATH="$HOME/.local/bin:$PATH"

#export AGENT_BROWSER_ENGINE=lightpanda

export PATH="$HOME/.cargo/bin:$PATH"
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

alias get_idf=". $HOME/esp/esp-idf/export.sh"

if command -v wt >/dev/null 2>&1; then eval "$(command wt config shell init zsh)"; fi

export NPM_PRECOMMIT_HOOK=true


# Added by Antigravity
export PATH="$HOME/.antigravity/antigravity/bin:$PATH"

# Added by Antigravity IDE
export PATH="$HOME/.antigravity-ide/antigravity-ide/bin:$PATH"

CLAUDE_CODE_NO_FLICKER=1

# Darkbloom
export PATH="$HOME/.darkbloom/bin:$PATH"

# gcloud-cli
export PATH=/opt/homebrew/share/google-cloud-sdk/bin:"$PATH"


export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"
