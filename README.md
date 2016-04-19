The project REST services, to obtain statistics on bonus cards.
The data source is 1C web service. 1С provide data by SOAP.

The project is written on Python 3.4 and [django-rest-framework](http://www.django-rest-framework.org/) .


Available web services:

* /bonus_cards/get_uuid - get bonus card uuid by number
* /bonus_cards/balance - get balance of bonus card
* /bonus_cards/transactions - get transactions of bonus card 
