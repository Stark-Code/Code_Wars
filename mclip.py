#! python3
# mclip.py - A multi clipboard program
import sys, pyperclip

clips = {
    'd': "I eat.",
    's': 'Thats why I dont like breakfast anymore : (.'
}

if len(sys.argv) < 2:
    print(f'Usage: Enter keywords {clips.keys()} for full text')
    sys.exit()
keyPhrase = sys.argv[1]

if keyPhrase in clips:
    print(f'{clips[keyPhrase]} copied to clipboard')
    pyperclip.copy(clips[keyPhrase])
else:
    sys.exit('Key not found in clipboard shortcuts!')