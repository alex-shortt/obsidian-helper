# purpose: fix all the broken page links from roam that should go from [term]([[terms_page]]) to [term](terms_page)


import os
import re

path_to_vault = "/Users/alex/worlds/basis/basis-language"

for subdir, dirs, files in os.walk(path_to_vault):
	for file in files:
		# Open file 
		full_path = os.path.join(subdir, file)
		if full_path.find(".md") > -1:
			print(full_path)
	
			f_hand = open(full_path, errors='ignore')
		
			for line in f_hand:
				fucked_links = re.findall(r'((\(.*\))(\[\[\[.*\]\]\]))+', line)
				print(len(fucked_links))
