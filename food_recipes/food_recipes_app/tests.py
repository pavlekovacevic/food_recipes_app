from rest_framework.test import APIClient
from food_recipes_app.models import UserProfile, Recipe
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class MyTestCase(APITestCase):
    def setUp(self):
        
        self.user = UserProfile.objects.create_user(name='Test', email='test@test.com', password='password')
        self.user.save()
        
        token = Token.objects.create(user=self.user)
        #simulira login samim tim sto nam je dao token i vazi za kredencijale ovog usera
        self.client = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)

    

    def test_firstOne(self):
        
        user = UserProfile.objects.get(name='Test')
        
        print(user)

# def test_create_user(), all data is valid and user is created
    def test_create_user(self):
        response = self.client.post('/api/profile/', data={
            'name':'new_user1',
            'email':'newgmail@gmail.com',
            'password':'password'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# def test_create_user_invalid_data(), data is not valid and the req is interupted
    def test_create_user_invalid_data(self):
        response = self.client.post('/api/profile/', data={
            'name':1,
            'email':'test@test.com',
            'password':'password'
        })
        import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# def test_create_user_already_in_db(), user tries to signup but the profile is already create
    def test_create_user_already_in_db(self):
        response = self.client.post('/api/profile/',data={
            'name':'Test',
            'email':'test@test.com',
            'password':'password'
        })
        import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# def test_user_login(), correct credentials and user gets a token, request continues
    def test_user_login(self):
        response = self.client.post('/api/login/', data={
            'username':'test@test.com',
            'password':'password'
        })
        import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# def test_user_login_forbidden_user(), credentials not correct user does not get a token
    def test_user_login_forbidden_user(self):
        response = self.client.post('/api/login/', data={
            'username':'forb@forb.com',
            'password':'forbidden'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
# def test_user_login_invalid_data(), form is not fullfiled and user cant log in    
    def test_user_login_invalid_data(self):
        response = self.client.post('/api/login/', data={
            'username':123,
            'password':'forbidden'
        })
        import pdb;pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)