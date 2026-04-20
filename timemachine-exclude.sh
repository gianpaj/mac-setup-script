sudo tmutil addexclusion -p ~/.agent-browser \
&& sudo tmutil addexclusion -p ~/.claude \
&& sudo tmutil addexclusion -p ~/.copilot \
&& sudo tmutil addexclusion -p ~/.cua-venv \
&& sudo tmutil addexclusion -p ~/.dropbox \
&& sudo tmutil addexclusion -p ~/.gemini \
&& sudo tmutil addexclusion -p ~/.gradle \
&& sudo tmutil addexclusion -p ~/.local \
&& sudo tmutil addexclusion -p ~/.nvm \
&& sudo tmutil addexclusion -p ~/Library/Android \
&& sudo tmutil addexclusion -p ~/Library/Caches \
&& sudo tmutil addexclusion -p ~/Library/pnpm \
&& sudo tmutil addexclusion -p ~/Dropbox \
&& sudo tmutil addexclusion -p ~/go \
&& sudo tmutil addexclusion -p ~/.antigravity \
&& sudo tmutil addexclusion -p ~/.asdf \
&& sudo tmutil addexclusion -p ~/.audio-tts \
&& sudo tmutil addexclusion -p ~/.bun \
&& sudo tmutil addexclusion -p ~/.cache \
&& sudo tmutil addexclusion -p ~/.codex \
&& sudo tmutil addexclusion -p ~/.kilocode \
&& sudo tmutil addexclusion -p ~/.lmstudio \
&& sudo tmutil addexclusion -p ~/.npm \
&& sudo tmutil addexclusion -p ~/.vscode \
&& sudo tmutil addexclusion -p ~/Downloads/youtube \
&& sudo tmutil addexclusion -p ~/OrbStack \
&& sudo tmutil addexclusion -p ~/backends \
&& sudo tmutil addexclusion -p ~/freelance \
&& sudo tmutil addexclusion -p ~/github

defaults read /Library/Preferences/com.apple.TimeMachine.plist SkipPaths

# See also <https://github.com/django23/asimov/tree/develop>

# git clone https://github.com/django23/asimov/tree/develop
# make install
