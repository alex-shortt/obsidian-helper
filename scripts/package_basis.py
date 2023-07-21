# purpose: to package files that need to be shipped live to logic map

import os
import time
import json
from datetime import datetime
from pathlib import Path

path_to_vault = "/Users/alex/worlds/basis/basis-language"
folders = ["1_metaphysics", "2_basis", "3_society", "4_logic"]
upload = True

# format: link_name_1;link_name_2;...link_name_n;

content = ""
contents = []
count = 0

for folder in folders:
    folder_path = path_to_vault + "/" + folder
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith("."):
                continue
            clean_name = file.replace(".md", "")
            full_path = os.path.join(subdir, file)
            relative_path = full_path.replace(path_to_vault + "/", "")
            relative_path_clean = relative_path.replace(".md", "")

            path = Path(full_path)
            file_text = path.read_text()
            create_time = datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d')
            mod_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d')
            
            data = {}
            data["name"] = clean_name
            data["path"] = relative_path_clean
            data["create_time"] = create_time
            data["mod_time"] = mod_time
            data["text"] = file_text
            contents.append(data)
            
            # content += "\n~~~~~~"
            # content += relative_path_clean + ";"
            # content += str(create_time) + ";"
            # content += str(mod_time) + ";"
            # content += file_text
            # content += "~~~~~~\n"

            count += 1

out_file_name = "basis_content_" + str(int(time.time())) + ".json"
script_dir = os.path.dirname(os.path.abspath(__file__))
content_file = os.path.join(script_dir, out_file_name)
with open(content_file, "w") as f:
    f.write(json.dumps(contents))

if upload == False:
    print("Wrote " + str(count) + " files to " + content_file)
    exit()

# upload new file to s3, set acl to public-read
aws_profile = 'alex'
bucket = 'mediated-assets'
path = '/basis/content'
s3_path = path + "/" + out_file_name
os.system("aws s3 cp " + content_file + " s3://" + bucket + s3_path + " --profile " + aws_profile + " --acl public-read")

prod_url = "https://assets.mediated.world" + path + "/" + out_file_name

print("Uploaded " + str(count) + " files to " + prod_url)