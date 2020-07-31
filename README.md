# Gian's current macOS setup

> as of July 2020

## Initial setup

> Taken from <https://github.com/pathikrit/mac-setup-script>

1. Install [brew](https://brew.sh/)
2. Clone repo

    ```bash
    git clone git@github.com:gianpaj/mac-setup-script.git
    ```

3. Set macOS settings

    ```bash
    cd mac-setup-script
    bash defaults.sh
    ```

4. Install apps

    ```bash
    bash install.sh
    ```

5. Reboot

## Applications

### Hardware apps

- Razer Synapse
  - and script to load the app but hide mac menubar icon

```bash
brew tap homebrew/cask-drivers
brew cask install razer-synapse
```

- Karabiner Elements
  - to fix the back tick character ` when pressing §

### Work desktop apps

Via home brew:

```bash
brew cask install figma
brew cask install free-ruler
```

### Productivity apps

- NightOwl
- [Pomodoro](https://github.com/G07cha/pomodoro) (Electron app)
  - Look for similar app but native (or uses less CPU)
  - Also, add sounds 
- [Grayscale Mode](https://github.com/rkbhochalya/grayscale-mode)

### Software development apps

- VSCode
- Sublime Merge

  ```bash
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

```bash
git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d
```

### VSCode extensions

- GitLens
- Sublime Text Keymap and Settings
- ESLint
- EditorConfig for VS Code
- [DeepScan](https://marketplace.visualstudio.com/items?itemName=DeepScan.vscode-deepscan) - Detect bugs and quality issues in JavaScript, TypeScript, React and Vue.js more precisely
- [JavaScript (ES6) code snippets](https://marketplace.visualstudio.com/items?itemName=xabikos.JavaScriptSnippets)
- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) - keyboard shortcuts, table of contents, auto preview and more
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) - Markdown linting and style checking
- [npm Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.npm-intellisense) - autocompletes npm modules in import statements
- [Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense) - autocompletes filenames

### General apps

Via home brew:

- Dropbox
- Spotify

  ```bash
  brew cask install spotify
  ```

### Chrome Extensions

- [uBlock origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
- [The Great Suspender](https://chrome.google.com/webstore/detail/the-great-suspender/klbibkeccnjlkjkiokjodocebajanakg)
- [LastPass](https://chrome.google.com/webstore/detail/lastpass-free-password-ma/hdokiejnpimakedhajhdlcegeplioahd)
- [Grammarly](https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen)
- [Pushbullet](https://chrome.google.com/webstore/detail/pushbullet/chlffgpmiacpedhhbkiomidkjlcfhogd)
- [Wappalyzer](https://chrome.google.com/webstore/detail/wappalyzer/gppongmhjkpfnbhagpmjfkannfbllamg)
#### uBlock filters

```
! 27/02/2020 https://github.com
github.com##.unread.mail-status.js-indicator-modifier

! 06/03/2020 https://twitter.com
twitter.com##.r-qvutc0.r-3s2u2q.r-1m4drjs.r-kquydp.r-u8s1d.r-1b8eohn.r-ad9z0x.r-1777fci.r-50lct3.r-16dba41.r-1gkfh8e.r-1qd0xha.r-1q142lx.r-6koalj.r-jwli3a.r-1tjplnt.r-rs99b7.r-1phboty.r-sdzlij.r-f6ebdl.r-urgr8i.r-1awozwy.css-901oao

! 17/06/2020 https://www.google.com
www.google.com###eob_8

! 07/07/2020 https://kanban-chi.appspot.com
kanban-chi.appspot.com##.upgrade
```

### Desktop apps

- iStat Menu 6 (purchased)

## macOS configuration

## Resources

- [macOS Setup Guide by Sourabh Bajaj](https://sourabhbajaj.com/mac-setup/)