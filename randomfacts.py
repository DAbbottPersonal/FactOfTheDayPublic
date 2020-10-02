import requests
from time import strftime
import re
from random import random
import webbrowser
from smtplib import SMTP
from yaml import safe_load
import argparse

def month_and_day(asString = True):
    if(asString):
        return strftime("%B_%d")
    return strftime("%m_%d")

def extractLines(rawtext):
    rawlist = rawtext.split('\n')
    eventlist = []
    eventswitch = False
    for curline in rawlist:
# Only extract Birthdays and Events.
        if 'id="Events"' in curline:
            eventswitch = True
        if 'id="Births"' in curline:
            eventswitch = False
        if eventswitch:
            eventlist.append(curline)

# This code will help clean up some of the wikipedia formatting
    startrecord = False
    parsedlist = []
    for curline in eventlist:
        if '<li>' in curline:
            startrecord = True
        if startrecord == True:
            modline = curline.replace('<li>', '')
            modline = modline.replace('</li>', '')
            modline = modline.replace('<lu>', '')
            modline = modline.replace('</lu>', '')
            modline = modline.replace('<ul>', '')
            modline = modline.replace('</ul>', '')
            modline = modline.replace('</a>','')
            modline = modline.replace('<a *>','')
            modline = modline.replace('<i>', '')
            modline = modline.replace('</i>', '')
            modline = modline.replace('<u>', '')
            modline = modline.replace('</u>', '')
            modline = modline.replace('&#8211; ','')
            subbed = re.sub('<a.*?>','', modline)
            parsedlist.append(subbed)
        if '</li>' in curline:
            startrecord = False

    return parsedlist

############################################################
###### Begin main body of code below #######################
############################################################

# Command line arguments here.
parser = argparse.ArgumentParser(description='Run the full chain of limit plot making for boosted.')
parser.add_argument('-e','--email',type=str, help='Email to a specific person, instead of a group yaml.')
parser.add_argument('-w','--html',action='store_true',help='Output an html with the fact of the day.')
parser.add_argument('-p','--printOnly',action='store_true',help='Will only print the fact.')
args = parser.parse_args()

doHTML = False
if args.html: doHTML = True

urlToGet = 'https://simple.wikipedia.org/wiki/' + month_and_day(True)
request = requests.get(urlToGet)
eventLines = extractLines( request.text )
fEvents=open('EventsOfToday.txt','w')

# Import list to send it to.
contactData = None
with open("contacts.yaml", 'r') as stream:
    contactData = safe_load(stream)

# Import list to email from.
emailData = None
with open("email.yaml", 'r') as stream:
    emailData = safe_load(stream)


contacts = []
for curContact in contactData.keys():
    contacts.append( contactData[curContact]["Email"] )

randomChoice = int(len(eventLines)*random())
# Write all facts out to a file.
for line in eventLines:
    fEvents.write(line+'\n')

randomLine = eventLines[randomChoice]
print ("A random event from this day in history...")
print ("On " + strftime("%B %d, ") + randomLine)
if not args.printOnly:
    if doHTML:
        fhtml = open('todaysevent.html','w')
        fhtml.write("A random event in history...\n")
        fhtml.write( ' '.join(["On", strftime("%B %d,"), line]) )
        fhtml.close()
        webbrowser.open("todaysevent.html")

    server = SMTP('smtp.gmail.com', 587) #should port be 587 or 465?
# Pull email and password from environment variables!
    fromEmail = emailData["Email"]
    password  = emailData["Password"]
# Hardcoded list for contacts that do not want emails!
    unsubscribeList = []

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromEmail,password)
    if args.email:
        try:
            if args.email in unsubscribeList:
                print (args.email + " is unsubbed!")
            else:
                server.sendmail( fromEmail, args.email, ("On " + strftime("%B %d, ") + line) )
        except:
            print (' '.join(["The email", args.email, "is invalid!"]) )
    else:
        for curremail in contacts:
            try:
                if curremail in unsubscribelist:
                    print (curremail + " is unsubbed!")
                else:
                    server.sendmail(fromemail, curremail, ("On " + strftime("%B %d, ") + line))
            except:
                print (' '.join(["The email", curremail, "is invalid!"]) )

fEvents.close()

print ("Done")
