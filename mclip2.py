#! python3
# mclip.py - A multi clipboard program
import sys, pyperclip

text = pyperclip.paste()

lines = text.split('\n')

for idx in range(len(lines)):
    lines[idx] = '*' + lines[idx]
text = '\n'.join(lines)

pyperclip.copy(text)
