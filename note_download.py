import dotenv
import requests
import os
import sys

#print command line arguments 
# print(sys.argv)
dotenv.load_dotenv()
# check if token is passed as argument
if len(sys.argv) > 1:
    token = sys.argv[2]
    tag = sys.argv[4] 
    api_key = token
    tag = tag
else:
    try:
        api_key = dotenv.dotenv_values(".env")['TOKEN'] 
        tag = dotenv.dotenv_values(".env")['TAG'] 
    except:
        # print("Please set the token and tag in .env file")
        # usage
        print("Usage: python3 note_download.py --token <token> --tag <tag>")
        sys.exit(1)
print(tag)
print(api_key)

# print(api_key)
url = "https://api.hackmd.io/v1/notes"
headers = { "Authorization": "Bearer " + api_key}
response = requests.get(url, headers=headers)
# print(response.json())

# get note id from json when tag has 5g in it
note_id_list = []
for note in response.json():
    try:
        if tag in note['tags']:
            note_id = note['id']
            note_id_list.append(note_id)
            # print(note_id_list)
    except:
        pass
print(note_id_list)

# create a directory to store the notes
# if file doesn't exist, create it
if not os.path.exists("5g_notes"):
    os.mkdir("5g_notes")
else:
    pass
# cd into the directory
os.chdir("5g_notes")

for note_id in note_id_list:
    url = "https://api.hackmd.io/v1/notes/" + note_id
    response = requests.get(url, headers=headers)
    # get title from note id
    title = response.json()['title']
    # get note content from note id
    content = response.json()['content']
    # store the note content in a file with the title name
    # if there's a space in title add escape symbol
    title = title.replace("/", ".")
    print(title)
    with open(title + ".md", "w+") as f:
        f.write(content)

