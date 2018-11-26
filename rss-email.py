# -*- coding: utf-8 -*-
import requests
import xml
from xml.dom import minidom
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html2text
import time
import os
# retrieve previously stored IDS to send only new posts
currentids=[]
try:
	f=open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ids.json'), "r")
	currentids=json.load(f)
	f.close()
except:
	# there are no ids, the entire feed will be sent
	pass
r=requests.get("https://nvda.es/feed")
document=minidom.parseString(r.content)
# Store all post IDS
newids=[]
for i in document.getElementsByTagName("post-id"):
	newids.append(i.firstChild.data)
# We need to know which posts are new. If we find an already shared post, stop the loop
newposts_count=0
for id in newids:
	if id not in currentids:
		newposts_count=newposts_count+1
	else:
		break
allposts=document.getElementsByTagName("item")
posts=[]
# Insert new posts in reversed order. We want to share older ones first
for i in range(0, newposts_count):
	posts.insert(0, allposts[i])
feedtitle=document.getElementsByTagName("title")[0].firstChild.data
for post in posts:
	msg = MIMEMultipart('alternative')
	msg['Subject'] = post.getElementsByTagName("title")[0].firstChild.data + "-" + feedtitle
	msg['From'] = "wordpress@nvda.es"
	msg['To'] = "nvda-es@googlegroups.com"
	html=post.getElementsByTagName("content:encoded")[0].firstChild.data
	author=post.getElementsByTagName("dc:creator")[0].firstChild.data
	category=post.getElementsByTagName("category")[0].firstChild.data
	link=post.getElementsByTagName("link")[0].firstChild.data
	html=html+u"<p>Esta entrada ha sido publicada por "+author+u" en la categoría"+category+u".</p><p><a href='"+link+u"'>Ver la entrada en la web</a></p>"
	part1 = MIMEText(html2text.html2text(html), 'plain', 'UTF-8')
	part2 = MIMEText(html, 'html', 'UTF-8')
	msg.attach(part1)
	msg.attach(part2)
	s = smtplib.SMTP('localhost')
	s.sendmail("wordpress@nvda.es", "nvda-es@googlegroups.com", msg.as_string())
	s.quit()
	time.sleep(1)
# Finally, save the new IDS to a file
try:
	f=open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ids.json'), "w")
	json.dump(newids, f)
	f.close()
except:
	raise
