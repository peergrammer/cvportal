# cvportal
coding challenge


Testing

1. Clone the repository
2. Delete the cvportal/migrations folder
3. Update the cvportal/cvportal/settings.py
(commonly changed)
   - the database details
   - snmtp
4. Make sure the database is accessible
5. Run python3 manage.py makemigrations
6. Run python3 manage.py migrate
7. Create superuser 
8. Run python3 manage.py runserver
9. Admin login: http://127.0.0.1:8000/admin
10. User login: http://127.0.0.1:8080/account/
