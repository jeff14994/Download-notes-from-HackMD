import dotenv
import requests
import os

dotenv.load_dotenv()
api_key = dotenv.dotenv_values(".env")['TOKEN']
# print(api_key)
url = "https://api.hackmd.io/v1/notes"
headers = { "Authorization": "Bearer " + api_key}
response = requests.get(url, headers=headers)
# print(response.json())

# get note id from json when tag has 5g in it
note_id_list = []
for note in response.json():
    try:
        if "5g_notes" in note['tags']:
            note_id = note['id']
            note_id_list.append(note_id)
            # print(note_id_list)
    except:
        pass
print(note_id_list)

# create a directory to store the notes
os.mkdir("5g_notes")
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

