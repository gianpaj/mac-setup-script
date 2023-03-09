#/bin/bash

TOGGLE_TO="Scarlett Solo USB"

CURRENT=$(SwitchAudioSource -c -f cli | sed -e 's/,.*//')

echo "Current audio device: \"$CURRENT\""

if [ "$CURRENT" = "External Headphones" ]; then
    SwitchAudioSource -s "Scarlett Solo USB"
else
    SwitchAudioSource -s "External Headphones"
fi

CURRENT=$(SwitchAudioSource -c -f cli | sed -e 's/,.*//')

echo "✅ Switched to: \"$CURRENT\" 🎉"
