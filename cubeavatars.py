import datetime
today = datetime.date.today()
print(today)

base_url="https://www.cubecraft.net"

import requests  
from bs4 import BeautifulSoup
import pandas as pd
import re
import shutil

# Location:
# python -i /mnt/c/Users/kinga/OneDrive/Desktop/PYTHON/cubeavatars.py
# python -m pip install mysql-connector


namepattern = re.compile('(?:\w*\/){4}(\d*)(\d{3}).jpg')


userIDs=[]
avatars=[]
totalPages = 29
thread="https://www.cubecraft.net/threads/cubecraft-book-of-world-records.213611/page-"
# "https://www.cubecraft.net/threads/selfieftw.5889/page-"

# "https://www.cubecraft.net/threads/eggwars-skywars-team-skywars-community-suggestions.63856/page-"
# 'https://www.cubecraft.net/threads/ccg-memes.10860/page-'

for page in range(1,totalPages+1):
    r = requests.get(thread+str(page))
    soup = BeautifulSoup(r.text, 'html.parser') 
    print('Searching page : '+str(page)+'/'+str(totalPages))
    messages = soup.find_all('li',class_="message")
    for message in messages:
        avatar_url = message.find('a',class_="avatar").find('img').get('src')
        avatar_alt = message.find('a',class_="avatar").find('img').get('alt')
        user_ign = message.find('div', class_="playerUsername")

        if(namepattern.match(avatar_url)!=None):
            userimageid=namepattern.match(avatar_url).group(1)

            if(userimageid!=None):
                userId = namepattern.match(avatar_url).group(1)
                imageId = namepattern.match(avatar_url).group(2)
            else:
                userId='unknown'
                imageId='unknown'
            if(user_ign!=None):
                userName = user_ign.text
            else:
                userName = avatar_alt

            # print(userName+' ['+userId+'] : '+imageId)
            # Check if user exists, then save these to database if new:
            imageUrl='https://www.cubecraft.net/data/avatars/l/'+userId+'/'+userId+imageId+'.jpg'
            imageName=userName+'.jpg'

            # Prevent duplicates:
            if userId not in userIDs:
                userIDs.append(userId)
                avatars.append({'userId':userId, 'userName':userName, 'imageId':imageId, 'imageName':imageName, 'imageUrl':imageUrl})
                print(userName+' -> '+imageUrl)
            
def saveAvatar(userId, userName, imageId, imageName, imageUrl):
    try:
        # Open the url image, set stream to True, this will return the stream content.
        resp = requests.get(imageUrl, stream=True)
        # Open a local file with wb ( write binary ) permission.
        local_file = open('/mnt/c/Users/kinga/OneDrive/Desktop/PYTHON/avatars/'+imageName, 'wb')
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)
        # Remove the image url response object.
        del resp
    except:
        print('failed for: '+userName)

for avatar in avatars:
    userId = avatar['userId']
    userName = avatar['userName']
    imageId = avatar['imageId']
    imageName = avatar['imageName']
    imageUrl = avatar['imageUrl']
    saveAvatar(userId, userName, imageId, imageName, imageUrl)