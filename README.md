# FactOfTheDay
This code pulls daily information from wikipedia, parses the text, randomly selects one of the many events, then sends it as an email.

## Setup
You must use an email to "send" the email from. It can be your personal email or a dummy one. 
There may be security protocals for some email services, which will need to be disabled so this can work. 
Add your email and password to ```email.yaml``` in the format of ```example_email.yaml``` to send the email fact. 
Alternatively, use the ```--printOnly``` option to simple print the fact to the screen without emailing it.

## How to run
Send via email list contact.yaml (must be filleId by user): <br /> 
```python randomfacts.py``` <br />
Send via single emaill: <br />
```python randomfacts.py -e youremail@foo.bar```
