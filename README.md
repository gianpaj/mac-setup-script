# Gian's current macOS setup

> as of July 2020

## Initial setup

> Taken from 

1. Install [brew](https://brew.sh/)
2. Clone repo

    ```
    git clone git@github.com:gianpaj/mac-setup-script.git
    ```

1. Set macOS settings

    ```
    cd mac-setup-script
    bash defaults.sh
    ```

1. Install apps 

    ```
    bash install.sh
    ```
1. Reboot

## Applications

### Hardware apps

- Razer Synapse
  - and script to load the app but hide mac menubar icon

```
brew tap homebrew/cask-drivers
brew cask install razer-synapse
```

- Karabiner Elements
  - to fix the back tick character (` \` `) when pressing §

### Work desktop apps

Via home brew:

```

```

### Productivity apps

- NightOwl
- [Pomodoro](https://github.com/G07cha/pomodoro) (Electron app)
  - Look for similar app but native (or uses less CPU)
  - Also, add sounds 
- [Grayscale Mode](https://github.com/rkbhochalya/grayscale-mode)

### Work Software development app

- VSCode
- Sublime Merge

  ```
    brew cask install sublime-merge
  ```
- Android Studio
  - Android SDK path
- Xcode
  - Command-line tools
- iTerm2
  - Zsh
  - oh-my-zsh
  - bash [aliases](./bash/.aliases)

e.g.

    git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d

### General apps

Via home brew:

- Dropbox
- Spotify
  ```
  brew cask install spotify
  ```


### Chrome Extensions

- [uBlock origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
- [The Great Suspender](https://chrome.google.com/webstore/detail/the-great-suspender/klbibkeccnjlkjkiokjodocebajanakg)
- [LastPass](https://chrome.google.com/webstore/detail/lastpass-free-password-ma/hdokiejnpimakedhajhdlcegeplioahd)
- [Grammarly](https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen)
- [Pushbullet](https://chrome.google.com/webstore/detail/pushbullet/chlffgpmiacpedhhbkiomidkjlcfhogd)

### Desktop apps

- iStat Menu 6 (purchased)
- 


## macOS configuration

## Resources

- [macOS Setup Guide by Sourabh Bajaj](https://sourabhbajaj.com/mac-setup/)