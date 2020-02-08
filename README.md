# icon.community portal site

## All-in-one Portal icon.community

We have a lot of ICON related websites scattered all over the place, information is sometimes difficult to find.
This website aims to become the all-in-one portal for all ICONists, this includes but not limited to DAPP information,
utility tools, token market information, block producer information, block explorers, wallets, exchanges, dev resources,
various events and campaign information and so on.

This project also aims to extract relevant data from ICON chain and displayed in a user friendly interface.
We'll initially focus on the ICONSENSUS campaign, starting off with P-Rep election data and tools.

## Installation

#Create virtual environment with python 3.6 or 3.7
```
virtualenv venv -p python3 
source venv/bin/activate 
```

#Requirements are mainly, postgresql, django2+, ICON SDK and some misc libraries
```
pip install -r requirements.txt 
```

#Migrate models
```
python manage.py makemigrations 
python manage.py migrate 
```

#Start postgresql
```
sudo start postgresql service 
```

#Start local server
```
python manage.py runserver 
```

#Visit
```
https://localhost:8000 
```
