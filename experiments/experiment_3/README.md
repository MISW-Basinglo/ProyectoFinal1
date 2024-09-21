# Steps to test experiment 3

1. Launch "docker-compose up" to deploy database with table Users (this table containt the field role)

![image](https://github.com/user-attachments/assets/7f4939f9-1024-4404-aaed-665ee781bf80)

2. Configure CLIENT_ID and CLIENT_SECRET with user proyect. (Lines 23 and 24)
3. Configura the API (Cloud Identity) with the redirection URL to the app Oauth

![image](https://github.com/user-attachments/assets/e7cfa5a7-04ac-44ba-b22a-25a6a72793d2)

4. Launch de application Oauth with the command "py oauth.py"

![image](https://github.com/user-attachments/assets/28f1ca27-2c7a-4e65-b68d-1b83ac561485)

5. Test the application with URL (https://localhost:5000)

![image](https://github.com/user-attachments/assets/e2445e24-0815-442e-ba08-74b7e1ccde48)

6. You should login with google 

![image](https://github.com/user-attachments/assets/cb9efe2d-d865-4c56-9cf5-4980bf238a09)

7. When you login with Google, the Cloud Identity API, redirect you to de application with all information profile.

![image](https://github.com/user-attachments/assets/5d882581-9643-42ea-9bf7-1bc07a5a8172)

8. You can see the register into DB

![image](https://github.com/user-attachments/assets/7345639a-3ea1-4484-bc27-48e1bbda0486)

9. Finally, you can try the autorize, with the roles to user (Default is user) with these URL's.

No autorizado 
https://localhost:5000/admin

![image](https://github.com/user-attachments/assets/04d37322-7e10-4c7a-9c04-a10e722c9115)

Autorizado 
https://localhost:5000/user

![image](https://github.com/user-attachments/assets/0a954c9b-c704-4b31-a33c-e689b4934e3b)

