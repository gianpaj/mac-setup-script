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
brew cask install sketch
brew cask install free-ruler
# ImageOptim — compress images without losing quality - https://imageoptim.com/mac
brew cask install imageoptim
# ImageAlpha — image minifier (like JPEG with transparency!) - https://pngmini.com
brew cask install imagealpha
```
- Color picker:
  - http://www.northernspysoftware.com/software/colorpicker
  - plus
    ```
    brew cask install colorpicker-skalacolor
    ```

- [Linear](https://github.com/mikaa123/linear) - Ruler app with web-development in mind

    My bug fix
    ```
    git clone git@github.com:gianpaj/linear.git
    git checkout -b upgrade-electron-package origin/upgrade-electron-package
    npm install
    npm run package
    ```
    
    Disable Gatekeeper:
    ```
    sudo spctl --master-disable
    ```
 

### Productivity apps

- [NightOwl](https://nightowl.kramser.xyz/) - Toggle the Dark mode via the Menu Bar 
  ```
  brew cask install nightowl
  ```
- [Pomodoro](https://github.com/G07cha/pomodoro) (Electron app)
  - Look for similar app but native (or uses less CPU)
  - Also, add sounds 
- [Grayscale Mode](https://github.com/rkbhochalya/grayscale-mode)

### Software development apps

- VSCode

  ```bash
    brew cask install sublime-merge
  ```

- Android Studio
  - Android SDK path
- Xcode
  - Command-line tools
- iTerm2
  - Zsh ([Guide](https://sourabhbajaj.com/mac-setup/iTerm/zsh.html))
  ```
  brew install zsh
  ```
  - oh-my-zsh
    ```
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
    - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
      ```
      git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
      ```
    - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
      ```
      git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
      ```
    - [pure](https://github.com/sindresorhus/pure) - Pretty, minimal and fast ZSH prompt
    ```
    npm install --global pure-prompt
    ```
    - Update `.zshrc`
  - bash [aliases](./bash/.aliases)

e.g.

```bash
git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d
```

#### Git configs

```bash
git config --system core.ignorecase false
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
- [TODO Highlight](https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight) - highlight TODOs, FIXMEs, and any keywords, annotations...
- [Color Highlight](https://marketplace.visualstudio.com/items?itemName=naumovs.color-highlight) - Highlight web colors in your editor

### General apps

Via home brew:

```bash
brew cask install dropbox
brew cask install spotify
brew cask install app-cleaner
```

### Chrome Extensions

- [uBlock origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
- [The Great Suspender](https://chrome.google.com/webstore/detail/the-great-suspender/klbibkeccnjlkjkiokjodocebajanakg)
- [LastPass](https://chrome.google.com/webstore/detail/lastpass-free-password-ma/hdokiejnpimakedhajhdlcegeplioahd)
- [Grammarly](https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen)
- [Pushbullet](https://chrome.google.com/webstore/detail/pushbullet/chlffgpmiacpedhhbkiomidkjlcfhogd)
- [Wappalyzer](https://chrome.google.com/webstore/detail/wappalyzer/gppongmhjkpfnbhagpmjfkannfbllamg)
- [Time Zone Converter - Savvy Time](https://chrome.google.com/webstore/detail/time-zone-converter-savvy/plhnjpnbkmdmooideifhkonobdkgbbof)
- [Motion](https://chrome.google.com/webstore/detail/motion/nidganghegonkcecgjgpppihfknjobec) - Never get distracted on the internet again

#### Web development

- [webhint](https://chrome.google.com/webstore/detail/webhint/gccemnpihkbgkdmoogenkbkckppadcag)
- [Preact Developer Tools](https://chrome.google.com/webstore/detail/preact-developer-tools/ilcajpmogmhpliinlbcdebhbcanbghmd)
- [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [OctoLinker](https://chrome.google.com/webstore/detail/octolinker/jlmafbaeoofdegohdhinkhilhclaklkp)

#### uBlock filters

```
! 27/02/2020 https://github.com
github.com##.unread.mail-status

! 06/03/2020 https://twitter.com
twitter.com##.r-qvutc0.r-3s2u2q.r-1m4drjs.r-kquydp.r-u8s1d.r-1b8eohn.r-ad9z0x.r-1777fci.r-50lct3.r-16dba41.r-1gkfh8e.r-1qd0xha.r-1q142lx.r-6koalj.r-jwli3a.r-1tjplnt.r-rs99b7.r-1phboty.r-sdzlij.r-f6ebdl.r-urgr8i.r-1awozwy.css-901oao

! 17/06/2020 https://www.google.com
www.google.com###eob_8

! 07/07/2020 https://kanban-chi.appspot.com
kanban-chi.appspot.com##.upgrade
```

### Desktop apps

- iStat Menu 6 (purchased)
- Giphy Capture
  - or kap
      ```
      brew cask install kap
      ```

## macOS configuration

## Resources

- [macOS Setup Guide by Sourabh Bajaj](https://sourabhbajaj.com/mac-setup/)