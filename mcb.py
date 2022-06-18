#! python3
# mcb.py - A multi clipboard program
import pyperclip, json, sys, pprint
print('Testing')
try:
    openFile = open('C:\\Users\\John\\PycharmProjects\\pythonProject\\clip_dictionary.json', 'r')
    clip_dictionary = json.load(openFile)  # Reading from json file
    pprint.pprint(clip_dictionary)
    openFile.close()
except FileNotFoundError:
    print('File Not Found')
    clip_dictionary = {}

if len(sys.argv) == 2:  # Retrieve list of keys or paste value.
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(clip_dictionary.keys())))
    elif sys.argv[1] in clip_dictionary:
        pyperclip.copy(clip_dictionary[sys.argv[1]])
    else:
        pyperclip.copy('Key not found')

elif len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
    clip_dictionary[sys.argv[2]] = pyperclip.paste()
    json_object = json.dumps(clip_dictionary)  # Serializing json
    with open('C:\\Users\\John\\PycharmProjects\\pythonProject\\clip_dictionary.json', "w") as outfile:
        outfile.write(json_object)
else:
    pyperclip.copy('Type help for details on how to use Multi-ClipBoard')

