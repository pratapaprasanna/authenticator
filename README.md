## UseCase
- Any idea or application a developer wants to develop. He has to put-in efforts to develop an authenticator using which a user signs up to the app.
- Authenticator is just that component which adds user to a db and validates if any request is coming from a person belonging to the application.

In signup you have multiple ways of doing it
- Manual sign-up {where you enter first name, lastname, email etc.}
- Signup with google/facebook/twitter

## Architecture or Idea

We want to go on a micro-frameworks architecture for easy plugin facility.

Some other day we want to work on some idea we should be able to use this authenticator to add users.

![image](https://user-images.githubusercontent.com/15846947/128825120-878b0e01-3bcf-4004-9add-4c4d50c60d0d.png)

## Stay updated with

- Discord https://discord.com/channels/876714663059025921/876714833150631996

### Setup Requisites
 - Mongo
 - docker
 - python
 - Kubernetes (Soon once the working prototype is ready)

### ENV setup
 - docker-compose up

Post this start making changes to the code they should be reflected and you should be able to see them running.

### Local Setup

##### Run

 - ```pip install poetry```
 - ```poetry install```
 - ```poetry run python authenticator/app.py```

### Current-state:
In the repo you see signup with google until now. Moving forward we should add the ability to signup with facebook/twitter

## User Journey
### Google login
 - When user wishes to sign-up

![1](https://user-images.githubusercontent.com/15846947/130355612-d9974e00-f6c2-4418-916d-907d9064b9b4.png)


- Authorize with gmail/google login
![3](https://user-images.githubusercontent.com/15846947/130355624-3777ce21-7ba2-41b4-9c8c-ef922a4a89ef.png)


- auth-token generated
![4](https://user-images.githubusercontent.com/15846947/130355640-57690aa0-199d-4525-90ae-b7ed345dc228.png)

- How auth-requests made and used

- Behaviour post logging out from google/gmail or from the session
![6](https://user-images.githubusercontent.com/15846947/130355653-12c2a454-dd82-499f-90a9-18f0297ff8e1.png)
![7](https://user-images.githubusercontent.com/15846947/130355661-36264201-8e34-4979-9e72-932feeb77b0c.png)
