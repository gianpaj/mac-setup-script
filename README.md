# Gian's current macOS setup

> as of Sept 2021, Big Sur

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
  curl -O https://dl.razerzone.com/drivers/Synapse2/mac/Razer_Synapse_Mac_Driver_v1.87.dmg
  # Install
  sudo chown -R `whoami` /Library/Application\ Support/Razer/
  source ~/Dropbox/Mac/razer-rz-start.sh
  ```

- Karabiner Elements
  - to fix the back tick character \` when pressing §
  - `non_us_backslash` to `grave_accent_and_tilde`

### Work desktop apps

Via home brew:

```bash
# brew install sketch --cask
brew install free-ruler --cask
# ImageOptim — compress images without losing quality - https://imageoptim.com/mac
brew install imageoptim --cask
# ImageAlpha — image minifier (like JPEG with transparency!) - https://pngmini.com
brew install imagealpha --cask
```

- Color picker:
  - <http://www.northernspysoftware.com/software/colorpicker>
  - plus

    ```bash
    brew install colorpicker-skalacolor --cask
    ```

- [Linear](https://github.com/mikaa123/linear) - Ruler app with web-development in mind

    My bug fix

    ```bash
    git clone git@github.com:gianpaj/linear.git
    git checkout -b upgrade-electron-package origin/upgrade-electron-package
    npm install
    npm run package
    ```

    Disable Gatekeeper:

    ```bash
    sudo spctl --master-disable
    ```

### Productivity apps

- [NightOwl](https://nightowl.kramser.xyz/) - Toggle the Dark mode via the Menu Bar
- [Horo](https://matthewpalmer.net/horo-free-timer-mac/) (timer/pomorodo menu app)
<!-- - [Grayscale Mode](https://github.com/rkbhochalya/grayscale-mode) -->

### Software development apps

- VSCode
- Android Studio
  - Android SDK path
- Xcode
  - Command-line tools
- nvm (Node.js)

  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

  nvm install --lts
  ```

- iTerm2
  - Zsh ([Guide](https://sourabhbajaj.com/mac-setup/iTerm/zsh.html))
  - oh-my-zsh

    ```bash
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```

    - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)

      ```bash
      git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
      ```

    - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

      ```bash
      git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
      ```

    - [zsh-completions](https://github.com/gianpaj/mac-setup-script)

       ```bash
       git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions
       ```

    - [pure](https://github.com/sindresorhus/pure) - Pretty, minimal and fast ZSH prompt

      ```bash
      brew install pure
      ```

    - Update `.zshrc`
  - Load `.zshrc` and `.aliases` from Dropbox

    ```bash
    ln -s ~/Dropbox/Mac/.zshrc .
    ln -s ~/Dropbox/Mac/.aliases .
    ```

e.g.

```bash
git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d
```

## Ubuntu linux useful commands

Upgrade all security packages

```bash
sudo apt-get -s dist-upgrade | grep "^Inst" | grep -i securi | awk -F " " {'print $2'}
sudo apt-get -s dist-upgrade | grep "^Inst" | grep -i securi | awk -F " " {'print $2'} | xargs sudo apt-get install -y
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

- Dropbox
- Spotify
- [App Cleaner](https://freemacsoft.net/appcleaner/)

### Firefox Settings

[about:config](about:config)

- [Disable zooming with Cmd + Mouse wheel](https://muffinman.io/blog/disable-cmd-mouse-wheel-zoom-in-firefox/)
`mousewheel.with_meta.action` = `0` disabled from `3` zoom

### Firefox Extensions

- [Auto Tab Discard](https://addons.mozilla.org/en-US/firefox/addon/auto-tab-discard/) (similar to The Great/Marvellous Suspender)
- [Grammarly](https://addons.mozilla.org/en-GB/firefox/addon/grammarly-1/)
- [uBlock origin](https://addons.mozilla.org/en-GB/firefox/addon/ublock-origin/)

### Chrome Extensions

- [New Tab Clock](https://chrome.google.com/webstore/detail/new-tab-clock/ljpapphpgkmigobbbakmnfoohclifanm)
- [uBlock origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
- [Ghostery - Privacy Blocker](https://chrome.google.com/webstore/detail/ghostery-%E2%80%93-privacy-ad-blo/mlomiejdfkolichcflejclcbmpeaniij)
- [The Marvellous Suspender](https://chrome.google.com/webstore/detail/the-marvellous-suspender/noogafoofpebimajpfpamcfhoaifemoa)
- [LastPass](https://chrome.google.com/webstore/detail/lastpass-free-password-ma/hdokiejnpimakedhajhdlcegeplioahd)
- [Grammarly](https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen)
- [Pushbullet](https://chrome.google.com/webstore/detail/pushbullet/chlffgpmiacpedhhbkiomidkjlcfhogd)
- [Wappalyzer](https://chrome.google.com/webstore/detail/wappalyzer/gppongmhjkpfnbhagpmjfkannfbllamg)
- [Time Zone Converter - Savvy Time](https://chrome.google.com/webstore/detail/time-zone-converter-savvy/plhnjpnbkmdmooideifhkonobdkgbbof)
  <!-- - [Motion](https://chrome.google.com/webstore/detail/motion/nidganghegonkcecgjgpppihfknjobec) - Never get distracted on the internet again -->
- [Hide Likes](https://chrome.google.com/webstore/detail/hide-likes/ebamaffgiechnomghfojkmlkaipoadni/related)
- [Hide Feed](https://chrome.google.com/webstore/detail/hide-feed/nfnpeneopnjggmcfdkhpjefammeonpjk)
- [xTab](https://chrome.google.com/webstore/detail/xtab/amddgdnlkmohapieeekfknakgdnpbleb) - Limit the maximum number of tabs that can be open at the same time.
- [Reader View](https://chrome.google.com/webstore/detail/reader-view/ecabifbgmdmgdllomnfinbmaellmclnh)
- [Google Image Search](https://chrome.google.com/webstore/detail/google-image-search/dbebidibfabmempkkbhabeehoncoaphf)

#### Web development

- [webhint](https://chrome.google.com/webstore/detail/webhint/gccemnpihkbgkdmoogenkbkckppadcag)
- [Preact Developer Tools](https://chrome.google.com/webstore/detail/preact-developer-tools/ilcajpmogmhpliinlbcdebhbcanbghmd)
- [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [OctoLinker](https://chrome.google.com/webstore/detail/octolinker/jlmafbaeoofdegohdhinkhilhclaklkp)

#### uBlock filters

[ublock-filters](./ublock-filters.txt)

### Desktop apps

- iStat Menu 6 (purchased)
- [Flow](https://apps.apple.com/ie/app/flow-focus-pomodoro-timer/id1423210932)
- Giphy Capture
  - or kap

    ```bash
    brew install kap --cask
    ```

## Resources

- [macOS Setup Guide by Sourabh Bajaj](https://sourabhbajaj.com/mac-setup/)
