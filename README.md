# Hotel Reservation System Backend API.

This is a web api that allows users to book reseravations, check room availability, and also cancel a reservation.

## Documentation

- Documentation: [docs](https://documenter.getpostman.com/view/10693271/2sAYX3rP6u)

### Prerequisites and Installing

You need to install the following software/technologies to have the app running on your local machine for development and testing purposes. Instructions on how to install will also be provided next to the software.

| Software                      | Installation Instructions/Terminal Commands      |
| ----------------------------- | ------------------------------------------------ |
| Python3.8                     | 1. sudo apt-get update                           |
|                               | 2. sudo apt-get install python3.8                |
| Virtual Environment           | 1. Python3 -m venv venv                          |
|                               | 2. Activate by running: source venv/bin/activate |
| Pip                           | pip install --upgrade pip                        |
| Django 4.2.18                 | pip install Django                               |
| djangorestframework           | pip install djangorestframework                  |
| djangorestframework.authtoken | pip install djangorestframework.authtoken        |
| Pyscopg2-binary               | pip install psycopg2-binary                      |

## Built With

- [Django] - 4.2 (https://docs.djangoproject.com/en/4.2/)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Wendy Munyasi**

## License

This project is licensed under the Apache License.

## Api Link and description

**Postman** can be used to access the api routes as the token identifier is provided directly.

## Project-Setup Instructions.

1.Open your github account and search for github username: **wendymunyasi**

1. git clone using the following links.

   link: https://github.com/wendymunyasi/hotel-booking-api.git

2. For Django app, set the database to your own url then run `python3 manage.py makemigrations` and `python3 manage.py migrate`.
3. Run the command `python3 manage.py runserver`.
4. Click the local host link on your terminal and navigate to the api root.

## NOTE

Almost every action is documented on the console, from creating a booking or deleting a booking. For curiouser and curiouser, open your console and view what messages display when you perform an action.

## Collaborate

To colloborate, reach me through my email address wendymunyasi@gmail.com
