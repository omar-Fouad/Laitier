from github import Github
from  PIL  import Image
import os
import io
g=Github("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")
#g = Github("omar.19761116@gmail.com","ocima@2021")
repo = g.get_repo("omar-Fouad/Laitier")
message = "Commit Message"
branch = "main"
print(repo.name)
def push_image(path,commit_message,content,branch,update=False):
    if update:
        contents = repo.get_contents(path, ref=branch.name)
        repo.update_file(contents.path, commit_message, content, branch, sha=contents.sha)
    else:
        repo.create_file(path, commit_message, content, branch)
branches = repo.get_branches()
for branch in branches:
  contents = repo.get_contents("", ref=branch.name)
  while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
      contents.extend(repo.get_contents(file_content.path, ref=branch.name))
    else:
      print(file_content)
uploaded_image = Image.open("datasets/good/IMG_1170.JPG")
# #repo.create_file("/dataset/bad/image1.jpg", message, contents, branch.name)
img_byte_arr = io.BytesIO()
uploaded_image.save(img_byte_arr, format='png')
img_byte_arr = img_byte_arr.getvalue()
#repo.create_file('datasets/good/image2.jpg', 'upload image',img_byte_arr,branch='main')
push_image('datasets/good/image3.jpg','upload image',img_byte_arr,branch='main',update=False)