# purpose: to, given a folder, find which terms used in all definitions are not contained in the same folder

import os
import re
from pathlib import Path


path_to_vault = "/Users/alex/worlds/basis/basis-language"
target_folder = "1_metaphysics/1_axioms"
debug = False

########################################################################################

def get_definition(text):
	lines = text.split("\n")
	def_block = None
	for line in lines:
		if "**definition:**" in line:
			def_block = line
			break
	
	return def_block


def get_links(text):
    words = []
    matches = re.findall('\[\[.*?\]\]', text)
    for match in matches:
        words.append(match.replace("[[", "").replace("]]", "").split("|")[0])

    return words


########################################################################################


folder_path = path_to_vault + "/" + target_folder

files_in_folder = []
ideas = []

# go through folder definitions looking for terms
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
		definition = get_definition(file_text)
		if definition is None:
			print("no definition in " + clean_name)
			raise FileNotFoundError
		file_links = get_links(definition)

		# organize
		for link in file_links:
			found = False
			for item in ideas:
				if item['term'] == link:
					found = True
					if clean_name not in item['sources']:
						item['sources'].append(clean_name)

			if found:
				continue

			idea = { 
				"term": link,
				"sources": [clean_name],
			}
			ideas.append(idea)
			

# check for any files that aren't linked at all			
for file in files_in_folder:
	found = False
	for idea in ideas:
		if idea['term'] == file:
			found = True
	
	if not found:
		idea = {
			"term": file,
			"sources": [],
		}
		ideas.append(idea)

# update complete status
for idea in ideas:
	idea['complete'] = idea['term'] in files_in_folder

# print raw
if debug:		
	for idea in ideas:
		print(idea)

########################################################################################

num_complete = 0
for idea in ideas:
	if idea['complete']:
		num_complete += 1
pct_complete = num_complete / len(ideas)
pct_complete_str = str(round(pct_complete * 100))
complete_str = "complete" if pct_complete == 1 else "incomplete" 
print("\nthis folder is " + complete_str)
print("\t" + str(num_complete) + " complete ideas")
print("\t" + str(len(ideas)) + " mentioned ideas")
print("\t" + pct_complete_str + "% complete")

print('\nthese ideas are used but not in the folder:')
for idea in ideas:
	if not idea['complete']:
		print("\t" + idea['term'])
		for source in idea['sources']:
			print("\t   |-" + source)

print('\nthese ideas are in the folder but not used:')
for idea in ideas:
	if len(idea['sources']) == 0:
		print("\t" + idea['term'])


print("\n")