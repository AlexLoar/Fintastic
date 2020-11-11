from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from tests.users.factories import UserFactory

User = get_user_model()


class UserTestCase(APITestCase):

    def test_create_user_without_name_returns_error(self):
        url = reverse('user-list')
        request_body = {
            "email": "batman@email.com",
            "age": 27
        }
        response = self.client.post(url, request_body)

        expected_response = {"name": ["This field is required."]}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_create_user_without_email_returns_error(self):
        url = reverse('user-list')
        request_body = {
            "name": "Batman",
            "age": 27
        }
        response = self.client.post(url, request_body)

        expected_response = {"email": ["This field is required."]}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_create_user_without_age_returns_error(self):
        url = reverse('user-list')
        request_body = {
            "name": "Batman",
            "email": "batman@email.com"
        }
        response = self.client.post(url, request_body)

        expected_response = {"age": ["This field is required."]}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_create_user_with_existing_email_returns_error(self):
        user = UserFactory()

        url = reverse('user-list')
        request_body = {
            "name": "Batman",
            "email": user.email,
            "age": 27
        }
        response = self.client.post(url, request_body)

        expected_response = {'email': ['user with this Email address already exists.', 'Enter a valid email address.']}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_list_all_users_may_list_them(self):
        UserFactory.create_batch(5)

        url = reverse('user-list')
        response = self.client.get(url)
        
        expected_users_number = User.objects.count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_users_number, len(response.data['results']))

    def test_user_detail_when_does_not_exists_returns_error(self):
        non_existent_user_id = "99"

        url = reverse('user-detail', kwargs={'pk': non_existent_user_id})
        response = self.client.get(url)

        expected_response = {"detail": "Not found."}
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_user_detail_when_user_exists_returns_its_data(self):
        user = UserFactory()

        url = reverse('user-detail', kwargs={'pk': user.id})
        response = self.client.get(url)

        expected_response = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'age': user.age
        }
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_response, response.data)

