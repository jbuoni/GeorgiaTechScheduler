Commands I used to setup mongo/pymongo/python on the class vm. Some of this might not be accurate so if you find errors setting it up, please adjust this document. I'm throwing this together by looking at my history. At some point, I'll download a clean version of the vm and retry.


1. sudo apt-get install -y mongodb-org
2. sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
3. echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
4. sudo apt-get update
5. sudo apt-get install -y mongodb-org
6. sudo service mongod start
7. sudo apt-get install build-essential python-dev
8. sudo pip install pymongo
