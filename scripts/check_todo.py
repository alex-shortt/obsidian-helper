# purpose: to, given a folder, find all [[TODO]] blocks in all .md files and aggregate their bullet point children into a list

import os
import re
from pathlib import Path


path_to_vault = "/Users/alex/worlds/basis/basis-language"
target_folder = "/"
debug = True

########################################################################################

def get_todo_blocks(text):
    blocks = []
    matches = re.findall('\[\[TODO\]\]\n((?:- .+\n?)+)', text)
    for match in matches:
        blocks.append(match)

    return blocks


def get_bullet_points(text):
    bullet_points = []
    lines = text.split("\n")
    for line in lines:
        if line.startswith("- "):
            bullet_points.append(line[2:])

    return bullet_points

########################################################################################

folder_path = path_to_vault + "/" + target_folder

files_in_folder = []
todos = []

# go through folder looking for [[TODO]] blocks and their bullet points
for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        # register file
        clean_name = file.replace(".md", "")
        files_in_folder.append(clean_name)

        # sort out paths
        full_path = os.path.join(subdir, file)
        path = Path(full_path)

        # make sure it's an md file
        if full_path.find(".md") <= 0:
            continue

        # get data
        file_text = path.read_text()
        todo_blocks = get_todo_blocks(file_text)
        if not todo_blocks:
            continue
            
        # organize
        for block in todo_blocks:
            bullet_points = get_bullet_points(block)
            todos.extend(bullet_points)

# print raw
if debug:
    for todo in todos:
        print(todo)

########################################################################################

print("\nList of all TODO bullet points:")
for todo in todos:
    print("\t- " + todo)

print("\n")
