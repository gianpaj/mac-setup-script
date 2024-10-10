#!/usr/bin/env bash

important_casks=(
  authy
  iterm2
  dropbox
  visual-studio-code
  slack
  stats   # https://github.com/exelban/stats
  itsycal # https://github.com/sfsam/Itsycal/
  spotify
  zed
)

brews=(
  ##### Install these first ######

  git
  jabba # java version manager

  ################################

  asdf # https://asdf-vm.com

  # "bash-snippets --without-all-tools --with-cryptocurrency --with-stocks --with-weather"
  bat

  # Remove large files or passwords from Git history like git-filter-branch
  bfg

  # Install GNU core utilities (those that come with macOS are outdated).
  coreutils

  dfc # https://github.com/rolinh/dfc

  exa # A modern version of ‘ls’. https://the.exa.website/
  # findutils
  # "fontconfig --universal"
  fd
  # git-extras    # for git undo
  git-lfs
  # "gnuplot --with-qt"
  # "gnu-sed --with-default-names"
  grep
  ripgrep
  # gpg
  # hstr          # https://github.com/dvorka/hstr
  htop   # https://htop.dev/
  httpie # https://httpie.io/
  iftop  # https://www.ex-parrot.com/~pdw/iftop/
  # "imagemagick --with-webp"
  # lnav          # https://lnav.org/
  # m-cli         # https://github.com/rgcr/m-cli
  # macvim        # https://macvim-dev.github.io/macvim/
  # micro         # https://github.com/zyedidia/micro
  # mtr           # https://www.bitwizard.nl/mtr/
  # neofetch      # https://github.com/dylanaraps/neofetch
  ncdu
  nmap
  # poppler       # https://poppler.freedesktop.org/
  postgresql
  # pv            # https://www.ivarch.com/programs/pv.shtml
  # python3
  prettyping
  # osquery
  # sbt
  # shellcheck	# https://www.shellcheck.net/
  # thefuck       # https://github.com/nvbn/thefuck
  # "wget --with-iri"
  # xsv
  tree

  # An open-source cross-platform alternative to AirDrop
  localsend

  # Terminal Prompt
  pure
  # general-purpose command-line fuzzy finder
  fzf

  # Software Development
  jq
  # runjs

  # Audio

  # Route Audio Between Apps
  blackhole-2ch

  # for Alfred workflow
  switchaudio-osx

  # Window management

  # koekeishiya/formulae/skhd
  # koekeishiya/formulae/yabai
  spectacle

  # Security

  tailscale
)

casks=(
  # aerial

  # Security

  # Productivity

  alfred
  nightowl
  remarkable
  simplenote

  # Hardware

  lunar
  karabiner-elements

  # Desktop tools

  hiddenbar

  appcleaner
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
  # private-eye

  # Quick Look plugins
  qlcolorcode
  qlmarkdown
  qlprettypatch
  qlstephen
  quicklook-csv
  quicklook-json

  the-unarchiver

  # satellite-eyes
  # sidekick
  # sloth
  # steam
  # synergy
  # transmission

  # qbittorrent#@HOME
  # xquartz
  vlc

  # Software Development

  mongodbsh
  postman
  sublime-merge
  sublime-text

  # Mobile App Development

  # vysor #@WORK
  # android-platform-tools #@WORK
  # android-studio #@WORK
  # Xcode Dev Cleaner
  devcleaner

  # Back-end Development

  dbeaver-community

  # Work

  grammarly-desktop
  zoom

  # Design

  colorpicker-skalacolor # http://www.northernspysoftware.com/software/colorpicker
  figma
  free-ruler
  imagealpha # image minifier (like JPEG with transparency!) - https://pngmini.com
  imageoptim # using https://squoosh.app for single images and lossy compression
  pika # picker app

  # Audio

  audacity

  # Terminal
  fig

  # Communication
  telegram
)

# Hardware
drivers=(
  elgato-camera-hub
  logi-options-plus
)

# pips=(
#   pip
#   glances
#   ohmu
#   pythonpy
# )

# gems=(
#   bundler
# )

npms=(
  surge
#
#   gitjk
#   n	# https://github.com/tj/n
)

# Git configs
# gpg_key='3E219504'
gian_name='Gianfranco Palumbo'
git_email='gianpa@gmail.com'
git_configs=(
  # do not check the status of the repo after each command
  "--add oh-my-zsh.hide-dirty 1"
  "branch.autoSetupRebase always"
  "color.ui auto"
  "core.autocrlf input"
  "core.ignorecase true"
  "credential.helper osxkeychain"
  "init.defaultBranch master"
  "merge.ff false"
  "pull.rebase true"
  "push.default simple"
  "rebase.autostash true"
  "remote.origin.prune true"
  "rerere.autoUpdate true"
  "rerere.enabled true"
  "user.email ${git_email}"
  "user.name ${gian_name}"
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
  for pkg in "$@"; do
    exec="$cmd $pkg"
    #prompt "Execute: $exec"
    if ${exec}; then
      echo "Installed $pkg"
    else
      echo "Failed to execute: $exec"
      if [[ -n "${CI}" ]]; then
        exit 1
      fi
    fi
  done
}

function brew_install_or_upgrade {
  if brew ls --versions "$1" >/dev/null; then
    if (brew outdated | grep "$1" >/dev/null); then
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
  while true; do
    sudo -n true
    sleep 60
    kill -0 "$$" || exit
  done 2>/dev/null &
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

echo "Install cask ..."
brew tap homebrew/cask-versions # for logi-options-plus and elgato-camera-hub
brew tap localsend/localsend
install 'brew install' "${important_casks[@]} --cask"

prompt "Install packages"
install 'brew_install_or_upgrade' "${brews[@]}"
# brew link --overwrite ruby

prompt "Install drivers"
brew tap homebrew/cask-drivers
install 'brew_install_or_upgrade' "${drivers[@]}"

prompt "Set git defaults"
for config in "${git_configs[@]}"; do
  git config --global "${config}"
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
$(brew --prefix)/opt/fzf/install
# sudo bash -c "echo $(brew --prefix)/bin/bash >> /private/etc/shells"
# #sudo chsh -s "$(brew --prefix)"/bin/bash

# echo "
# alias ls='exa -l'
# alias cat=bat
# " >> ~/.bash_profile

# prompt "Setting up xonsh"
# sudo bash -c "which xonsh >> /private/etc/shells"
# sudo chsh -s "$(which xonsh)"
# echo "source-bash --overwrite-aliases ~/.bash_profile" >> ~/.xonshrc

prompt "Install software"
install 'brew install' "${casks[@]} --cask"

# prompt "Install secondary packages"
# install 'pip3 install --upgrade' "${pips[@]}"
# install 'gem install' "${gems[@]}"
install 'npm install --global' "${npms[@]}"

install 'code --install-extension' "${vscode[@]}"

brew tap homebrew/cask-fonts
install 'brew install svn' # for font-source-code-pro
install 'brew install' "${fonts[@]} --cask"

brew tap mongodb/brew
brew install mongodb-community@5.0

# prompt "Update packages"
# pip3 install --upgrade pip setuptools wheel
# if [[ -z "${CI}" ]]; then
#   m update install all
# fi

# if [[ -z "${CI}" ]]; then
#   prompt  "Install following software from the App Store"
#   mas list
# fi

prompt "Cleanup"
brew cleanup

# Install Node

asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
asdf install nodejs lts
asdf global nodejs lts

echo "Done!"
