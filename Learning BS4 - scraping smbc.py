#!/usr/bin/env python
# coding: utf-8

# # WebScrape Functions 
# 
# In this notebook, we will define each essential function that we need for web scraping. 
# We will of course be depending on _requests_ and _BeautifulSoup4_ libraries as well. 
# 

# In[47]:


def get_comic(comic_index):
    
    # If successful returns the webpage as soup object, otherwise returns 0 
    import requests 
    from bs4 import BeautifulSoup
    
    base_url = "https://www.smbc-comics.com/comic/2002-09-05"
    page = requests.get(base_url)
    
    if str(page) == "<Response [200]>" :

        return BeautifulSoup(page.content, 'html.parser')
    else:
        return 0


# ## Single Comic Retrieval

# In[51]:


comic_index = 1
soup = get_comic(comic_index)

if soup == 0:
    print ("something went wrong")
else: 
    details = []
    details.append(comic_index)
    print (comic_index)

    title = str(soup.title.string[6:])
    details.append(title)
    print (title)

    sip_str = str(soup.find_all(id="middleContainer"))
    alt_text = sip_str.split(sep = "title=")[1]
    alt_text = alt_text[1:].split(sep = ">")[0][0:-1]
    details.append(alt_text)
    print (alt_text)

    sip_str = str(soup.find_all(id="middleContainer"))
    comic_url = sip_str.split(sep = "Permanent link to this comic: ")[1]
    img_url = comic_url.split(sep = "Image URL (for hotlinking/embedding): ")[1].split()[0]

    comic_url = comic_url.split()[0][0:-5]
    print (comic_url)
    details.append(comic_url)
    print (img_url)
    details.append(img_url)


# # Looped comic retrieval 

# In[135]:


# comic_list = {}
start = 800
stop = 1000
for comic_index in range(start,stop):
    
    soup = get_comic(comic_index)
    
    details = []
    details.append(comic_index)
#     print (comic_index)

    title = soup.title.string[6:]
    details.append(title)
#     print (title)

    sip_str = str(soup.find_all(id="middleContainer"))
    alt_text = sip_str.split(sep = "title=")[1]
    alt_text = alt_text[1:].split(sep = ">")[0][0:-1]
    details.append(alt_text)
#     print (alt_text)

    sip_str = str(soup.find_all(id="middleContainer"))
    comic_url = sip_str.split(sep = "Permanent link to this comic: ")[1]
    img_url = comic_url.split(sep = "Image URL (for hotlinking/embedding): ")[1].split()[0]

    comic_url = comic_url.split()[0][0:-5]
#     print (comic_url)
    details.append(comic_url)
#     print (img_url)
    details.append(img_url)

    print (details)
    comic_list[comic_index] = details
print ("All info collected")
    


# ## Retrieve the .png image file from the image url and save it to system 

# In[139]:


copy = comic_list # Just in case something goes wrong, the original dict is safe  


# In[134]:


import urllib.request
import shutil, os

for key in range(start,stop):
    print (copy[key][-1])  # Current comic being downloaded
    
    # Generate a safe filename (windows friendly)
    disallowed_characters = "<>:/\|?*&\"\'"
    safe_filename = str(key) +' ' + copy[key][1] + ".png"
    for character in disallowed_characters:
        safe_filename = safe_filename.replace(character, "")
    
    # Download image from the the stored img URL and save to system with safe filename
    urllib.request.urlretrieve(copy[key][-1], safe_filename)
    
    
    # Move the downloaded picture to appropriate folder
    target_folder = "C:/Users/kevin/Pictures/XKCD"
    shutil.move(safe_filename,target_folder)
    
print ("IMG retrieval completed")


# Create a CSV file that represents the comic_list dictionary 

# In[209]:


# copy = comic_list # Just in case something goes wrong, the original dict is safe  

# import csv
# with open('comic_details_file.csv', 'w') as csv_file:  
#     writer = csv.writer(csv_file)
#     for row in copy.items():
#         number = row[1][0]
#         print (number)
#         safe_filename = str(row[1][0]) +' ' + row[1][1] + ".png"
#         safe_filename = safe_filename.replace(character, "")
#         writer.writerow([row[1][0], row[1][1], row[1][2], row[1][3], row[1][4],safe_filename])

# Found a solution that uses json format instead of csv, this allows for the handling of special characters in the title and alt text
import json

copy2 = comic_list

# as requested in comment
copy2 = {'copy2': copy2}

with open('comicListFile.txt', 'w') as file:
     file.write(json.dumps(copy2)) # use `json.loads` to do the reverse
        


# In[210]:


import json

copy2 = comic_list

# as requested in comment
copy2 = {'copy2': copy2}

with open('comicListFile.txt', 'w') as file:
     file.write(json.dumps(copy2)) # use `json.loads` to do the reverse


# In[155]:


# comic_list = {}
# error_list = {}
import urllib.request
import shutil, os

start = 2490
stop = 2500


for comic_index in range(start,stop): # Collect the Raw Page HTML data and extract info
    
    soup = get_comic(comic_index) # a function to retrieve the page as bs4soup object 
    if soup == 0:  # Skip this comic if it's not available in html 
        error_list[comic_index] = ["Error in HTML retrieval"]
        print ("comic " + str(comic_index) +  " : Erorr in HTML retrieval")
        continue
        
    details = [] # info extracted from current page will be temporarily be stored in this list 
    details.append(comic_index)
#     print (comic_index)

    try:
        title = soup.title.string[6:]  # The main title of the comic
        details.append(title)
    #     print (title)

        sip_str = str(soup.find_all(id="middleContainer")) # The hidden text in the object 
        alt_text = sip_str.split(sep = "title=")[1]
        alt_text = alt_text[1:].split(sep = ">")[0][0:-1]
        details.append(alt_text)
    #     print (alt_text)

        sip_str = str(soup.find_all(id="middleContainer")) 
        comic_url = sip_str.split(sep = "Permanent link to this comic: ")[1]
        img_url = comic_url.split(sep = "Image URL (for hotlinking/embedding): ")[1].split()[0]

        comic_url = comic_url.split()[0][0:-5]
    #     print (comic_url)   # Permanent URL to the comic
        details.append(comic_url)
    #     print (img_url)
        details.append(img_url) # comic image link

        print (details)
        comic_list[comic_index] = details # store the current page into a master dict
    except:
        error_list[comic_index] = ["info extraction error"]
        print ("error in info extraction")
        continue
        
    try:         
        # Generate a safe filename (windows friendly)
            disallowed_characters = "<>:/\|?*&\"\'"
            safe_filename = str(comic_index) +' ' + copy[comic_index][1] + ".png"
            for character in disallowed_characters:
                safe_filename = safe_filename.replace(character, "")

            urllib.request.urlretrieve(copy[comic_index][-1], safe_filename) # Download image from the the stored img URL and save to system with safe filename
    except:
        error_list[comic_index] = ["img url retrieve error"]
        print ("error in img url retrieve")
        continue
    
    try:
        # Move the downloaded picture to appropriate folder
        target_folder = "C:/Users/kevin/Pictures/XKCD"
        shutil.move(safe_filename,target_folder)
    except:
        error_list[comic_index] = ["file moving error"]
        print ("error in file moving")
        continue
    
print ("Completed range of comics")


# In[156]:


error_list

