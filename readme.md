# Django Blog project (work in progress)

#### Run the local develop server:
	    docker-compose up -d --build
        docker-compose logs -f

Server will bind 8000 port. You can get access to server by browser [http://localhost:8008](http://localhost:8008)


## How to use:

To login as admin use - admin@admin.com / cool123

***Authorization and Registration***

If you want to register or authorize, use "sign in" or "sign up" page
> *Authorization* and *Registration* uses email confirmation and MailHog as an SMTP testing service
> 
> In order to see emails go to [http://localhost:8025](http://localhost:8025)

***Contact Us***

If you want to use *Contact Us* form, go to "Contact" page

> *Contact us* uses MailHog as an SMTP testing service
> 
> In order to see emails go to [http://localhost:8025](http://localhost:8025)
> > Django-Admin has *Feedback* tab with *Contact Us* queries where you can answer user's queries and check queries statuses

***Swagger***

In order to see an API docs with Swagger, go to - [http://localhost:8008/swagger](http://localhost:8008/swagger)

> Also, you could visit the page within Django-Admin 
