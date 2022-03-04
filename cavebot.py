from config import BOT_HOME_DIR
from credentials import *
import tweepy
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import glob
import random
import shutil

## load the image list and choose one at random
file_list = glob.glob(BOT_HOME_DIR + "images/*.jpg")
image_file = random.choice(file_list)

## open the image and resize it
img = Image.open(image_file)
new_width = 1400
new_height = int(1400/img.width * img.height)
img = img.resize((new_width,new_height))

## load the quotes, shuffle, and pick the first one in the list
quote_file = open(BOT_HOME_DIR + 'quotes.txt','r')
quotes = quote_file.readlines()
quote_file.close()
random.shuffle(quotes)
quote = "\"" + quotes[0].strip() + "\""

## for shorter quotes, make the font larger and place them at the top of the image, for longer quotes, make the font smaller and place them at the bottom
if len(quote) <=90: 
    font_size = 100
    text = textwrap.fill(quote, width=30)
    text_top = True
else:
    font_size = 50
    text = textwrap.fill(quote, width=60)
    text_top = False

## load the font, and calculate the dimensions and position of the text
font = ImageFont.truetype(BOT_HOME_DIR + "impact.ttf", font_size)
draw = ImageDraw.Draw(img)
textw, texth = draw.textsize(text, font)
if text_top:
    textX = (img.width / 2) - (textw/2) + 2
    textY = 20
else:
    textX = (img.width / 2) - (textw/2) + 2
    textY = img.height - texth - 20

## draw the text onto the image
draw.text((textX-2, textY-2), text,(0,0,0),font=font)
draw.text((textX+2, textY-2), text,(0,0,0),font=font)
draw.text((textX+2, textY+2), text,(0,0,0),font=font)
draw.text((textX-2, textY+2), text,(0,0,0),font=font)
draw.text((textX, textY), text, (255,255,255), font=font)

## save the image output
img.save(BOT_HOME_DIR + "output/out.jpg")

## authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

## post the tweet
image_path = BOT_HOME_DIR + "output/out.jpg"
status = api.update_status_with_media(status="",filename=image_path)

## move the used image to the used_images folder
file_name = image_file.split("/")[-1]
shutil.move(BOT_HOME_DIR + 'images/'+file_name, BOT_HOME_DIR + 'used_images/'+file_name)

## add the used quote to the used_quotes file
used_quote_file = open(BOT_HOME_DIR + 'used_quotes.txt','a')
used_quote_file.write(quote.strip('"') + "\n")
used_quote_file.close()

## remove the used quote from the list, and re-write the quotes file
del quotes[0]
quote_file = open(BOT_HOME_DIR + 'quotes.txt','w')
quote_file.truncate(0)
for element in quotes:
    quote_file.write(element)
quote_file.close()