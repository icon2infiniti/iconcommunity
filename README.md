# icon.community portal site

## All-in-one Portal icon.community

We have a lot of ICON related websites scattered all over the place, information is sometimes difficult to find. 
This website aims to become the all-in-one portal for all ICONists, this includes but not limited to DAPP information, 
utility tools, token market information, block producer information, block explorers, wallets, exchanges, dev resources, 
various events and campaign information and so on.

This project also aims to extract relevant data from ICON chain and displayed in a user friendly interface. 
We'll initially focus on the ICONSENSUS campaign, starting off with P-Rep election data and tools.


## Installation

virtualenv venv -p python3 #Create virtual environment with python 3.6 or 3.7

source venv/bin/activate #Activate environment

pip install -r requirements.txt #Requirements are mainly, postgresql, django2+, ICON SDK and some misc libraries

python makemigrations #Migrate database

python migrate #Migrate database

sudo start postgresql service #Start postgresql 

python manage.py runserver #Start local server

https://localhost:8000 #Visit starting page
