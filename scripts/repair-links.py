# purpose: fix all the fucked links from roam that should go from [term]([[terms_page]]) to [term|terms_page]


import os
import re

path_to_vault = "/Users/alex/worlds/muse/muse-stories"

test_mode = False

# aggregate links while in test mode
links = []

# in case you wanna test a couple before committing
max_docs = 100000000
count = 0

for subdir, dirs, files in os.walk(path_to_vault):
	for file in files:
		full_path = os.path.join(subdir, file)
			
		# make sure it's an md file
		if full_path.find(".md") > 0:
			file = open(full_path, errors='ignore')
			
			data = file.read()
			fucked_links = re.findall(r'((\[[^\)\]\n]+\])(\(\[\[[^\)\]\n]+\]\]\)))', data)

			# go through fucked links
			if len(fucked_links) > 0 and (not test_mode or count < max_docs):
				print("fixing " + full_path)		
				
				if test_mode:
					print("before")
					print(data)

				count += 1

				for fucked_link in fucked_links:
					old_text = fucked_link[0]
					name = fucked_link[1].replace("[", "").replace("]", "")
					link = fucked_link[2].replace("(", "").replace(")", "").replace("[[", "").replace("]]", "")
					new_text = "[[" + link + "|" + name + "]]"
					data = data.replace(old_text, new_text)
					links.append(old_text + " --> " + new_text)

				if not test_mode:
					with open(full_path, 'w', errors='ignore') as write_file:
						write_file.write(data)

				if test_mode:
					print("after")
					print(data)

for link in links:
	print(link)
