#getting spun up
step 1: extract username and password into environment variables from smart_client.py
step 2: get a valid username and password

then it's a normal flask-zappa app. get your aws creds in place, and swap out the s3 bucket in zappa_settings for one your creds owns. then `> zappa deploy` on the command line and you should be good to go. 
