#!/usr/bin/env bash

important_casks=(
  iterm2
  dropbox
  istat-menus
  visual-studio-code
  slack
)

brews=(
  # xonsh
  # jabba
  # "bash-snippets --without-all-tools --with-cryptocurrency --with-stocks --with-weather"
  bat

  # Install GNU core utilities (those that come with macOS are outdated).
  coreutils

  # dfc

  # A modern version of ‘ls’.
  exa
  # findutils
  # "fontconfig --universal"
  # fpp
  # gh
  git
  # git-extras
  # git-fresh
  # git-lfs
  # "gnuplot --with-qt"
  # "gnu-sed --with-default-names"
  # gpg
  # hh
  htop
  httpie
  # iftop
  # "imagemagick --with-webp"
  # lnav
  # m-cli
  # mackup
  # mas
  # micro
  # moreutils
  # mtr
  ncdu
  # neofetch
  nmap
  # poppler
  # osquery
  # sbt
  # shellcheck
  # stormssh
  # teleport
  # thefuck
  # "wget --with-iri"
  # xsv
  tree
  youtube-dl

  # Terminal Prompt
  
  pure
  # general-purpose command-line fuzzy finder
  fzf

  # Software Development
  jq
)

casks=(
  # aerial

  # Security

  authy
  boxcryptor

  # Productivity
  
  alfred
  karabiner-elements
  nightowl

  # background-music
  # cakebrew
  # docker
  firefox
  # google-backup-and-sync
  # github
  # handbrake
  # iina
  # istat-server
  # kap
  # launchrocket
  # little-snitch
  # macdown
  # muzzle
  # plex-media-player
  # plex-media-server
  # private-eye

  # Quick Look plugins
  qlcolorcode
  qlmarkdown
  qlprettypatch
  qlstephen
  quicklook-csv
  quicklook-json

  # satellite-eyes
  # sidekick
  # skype
  # sloth
  # steam
  # synergy
  # transmission
  # transmission-remote-gui
  # xquartz

  # Software Development

  android-platform-tools
  postman
  sublime-merge
  sublime-text

  vlc

  # Work

  microsoft-teams
  zoom

  # PM

  airdroid

  # Design

  colorpicker-skalacolor
  figma
  free-ruler
  imagealpha
  imageoptim
  sketch
)

# pips=(
#   pip
#   glances
#   ohmu
#   pythonpy
# )

# gems=(
#   bundler
#   travis
# )

# npms=(

#   fenix-cli
#
#   gitjk
#   kill-tabs
#   n
# )

# gpg_key='3E219504'
gian_name='Gianfranco Palumbo'
git_email='gianpa@gmail.com'
git_configs=(
  "branch.autoSetupRebase always"
  "color.ui auto"
  "core.autocrlf input"
  "credential.helper osxkeychain"
  "merge.ff false"
  "pull.rebase true"
  "push.default simple"
  "rebase.autostash true"
  "rerere.autoUpdate true"
  "remote.origin.prune true"
  "rerere.enabled true"
  "user.name ${gian_name}"
  "user.email ${git_email}"
  # "user.signingkey ${gpg_key}"
)

vscode=(
  # DeepScan - Detect bugs and quality issues in JavaScript, TypeScript, React and Vue.js more precisely 
  DeepScan.vscode-deepscan
  # JavaScript (ES6) code snippets
  xabikos.JavaScriptSnippets
  # Prettier - Code formatter
  esbenp.prettier-vscode
  # Markdown All in One - keyboard shortcuts, table of contents, auto preview and more
  yzhang.markdown-all-in-one
  # markdownlint - Markdown linting and style checking
  DavidAnson.vscode-markdownlint
  # npm Intellisense - autocompletes npm modules in import statements
  christian-kohler.npm-intellisense
  # Path Intellisense - autocompletes filenames
  christian-kohler.path-intellisense
  # TODO Highlight - highlight TODOs, FIXMEs, and any keywords, annotations...
  wayou.vscode-todo-highlight
  # Color Highlight - Highlight web colors in your editor
  naumovs.color-highlight
  # Sublime Text Keymap and Settings Importer
  ms-vscode.sublime-keybindings

  eamodio.gitlens

  dbaeumer.vscode-eslint
)

fonts=(
  font-fira-code
  font-source-code-pro
)

# JDK_VERSION=amazon-corretto@1.8.222-10.1

######################################## End of app list ########################################
set +e
set -x

function prompt {
  if [[ -z "${CI}" ]]; then
    read -p "Hit Enter to $1 ..."
  fi
}

function install {
  cmd=$1
  shift
  for pkg in "$@";
  do
    exec="$cmd $pkg"
    #prompt "Execute: $exec"
    if ${exec} ; then
      echo "Installed $pkg"
    else
      echo "Failed to execute: $exec"
      if [[ ! -z "${CI}" ]]; then
        exit 1
      fi
    fi
  done
}

function brew_install_or_upgrade {
  if brew ls --versions "$1" >/dev/null; then
    if (brew outdated | grep "$1" > /dev/null); then
      echo "Upgrading already installed package $1 ..."
      brew upgrade "$1"
    else
      echo "Latest $1 is already installed"
    fi
  else
    brew install "$1"
  fi
}

if [[ -z "${CI}" ]]; then
  sudo -v # Ask for the administrator password upfront
  # Keep-alive: update existing `sudo` time stamp until script has finished
  while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &
fi

if test ! "$(command -v brew)"; then
  prompt "Install Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
else
  if [[ -z "${CI}" ]]; then
    prompt "Update Homebrew"
    brew update
    brew upgrade
    brew doctor
  fi
fi
export HOMEBREW_NO_AUTO_UPDATE=1

echo "Install important software ..."
brew tap homebrew/cask-versions
install 'brew install' "${important_casks[@]} --cask"

prompt "Install packages"
install 'brew_install_or_upgrade' "${brews[@]}"
# brew link --overwrite ruby

git config --global user.name "Gianfranco Palumbo"
git config --global user.email "gianpa@gmail.com"

# prompt "Install JDK=${JDK_VERSION}"
# curl -sL https://github.com/shyiko/jabba/raw/master/install.sh | bash && . ~/.jabba/jabba.sh

prompt "Set git defaults"
for config in "${git_configs[@]}"
do
  git config --global ${config}
done

# if [[ -z "${CI}" ]]; then
#   gpg --keyserver hkp://pgp.mit.edu --recv ${gpg_key}
#   prompt "Export key to Github"
#   ssh-keygen -t rsa -b 4096 -C ${git_email}
#   pbcopy < ~/.ssh/id_rsa.pub
#   open https://github.com/settings/ssh/new
# fi

prompt "Upgrade bash"
# brew install bash bash-completion2 fzf
brew install fzf
$(brew --prefix)/opt/fzf/install
# sudo bash -c "echo $(brew --prefix)/bin/bash >> /private/etc/shells"
# #sudo chsh -s "$(brew --prefix)"/bin/bash

echo "
alias ls='exa -l'
alias cat=bat
" >> ~/.bash_profile

# prompt "Setting up xonsh"
# sudo bash -c "which xonsh >> /private/etc/shells"
# sudo chsh -s $(which xonsh)
# echo "source-bash --overwrite-aliases ~/.bash_profile" >> ~/.xonshrc

prompt "Install software"
install 'brew install' "${casks[@]} --cask"

# prompt "Install secondary packages"
# install 'pip3 install --upgrade' "${pips[@]}"
# install 'gem install' "${gems[@]}"
# install 'npm install --global' "${npms[@]}"

install 'code --install-extension' "${vscode[@]}"

brew tap homebrew/cask-fonts
install 'brew install svn'
install 'brew install' "${fonts[@]} --cask"

brew tap mongodb/brew
brew install mongodb-community@4.4

# prompt "Update packages"
# pip3 install --upgrade pip setuptools wheel
# if [[ -z "${CI}" ]]; then
#   m update install all
# fi

# if [[ -z "${CI}" ]]; then
#   prompt "Install software from App Store"
#   mas list
# fi

prompt "Cleanup"
brew cleanup

echo "Run [mackup restore] after Dropbox has done syncing ..."
echo "Done!"
