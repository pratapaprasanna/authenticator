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

## Share Your Ideas in

- Discord NebbyStudios (https://discord.gg/zPPmtnx2)

### Setup Requisites
 - Mongo
 - docker
 - python
 - Kubernetes (Soon once the working prototype is ready)

### ENV setup 
 - docker-compose up

Post this start making changes to the code they should be reflected and you should be able to see them running.

### Current-state: 
In the repo you see signup with google until now. Moving forward we should add the ability to signup with facebook/twitter

## User Journey
### Google login
 - When user wishes to sign-up

![WhatsApp Image 2021-07-28 at 6 44 16 PM](https://user-images.githubusercontent.com/15846947/127329000-12621164-ba6d-4775-bd40-8c9f4395ed59.jpeg)

- Authorize with gmail/google login
![2](https://user-images.githubusercontent.com/15846947/127329338-7e20218f-cccb-4059-817a-c27fdce6510d.jpeg)

- Acknowledgment that the details are stored
![3](https://user-images.githubusercontent.com/15846947/127329361-2b7d2e96-4a13-4245-b0db-1c6ead685195.jpeg)

- Behaviour post logging out from google/gmail or from the session
 cannot show logging out from gmail for personal reasons obviously :D
 
-![logout](https://user-images.githubusercontent.com/15846947/128707098-0c98a932-0bb9-4a51-ab6d-9d372677dc67.png)
-![5](https://user-images.githubusercontent.com/15846947/127329414-3f56d681-28b2-47a4-9277-eba437d419d5.jpeg)
