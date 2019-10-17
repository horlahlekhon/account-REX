from project.app.controllers.user_controller import UserResource, Users

from project.app.tests.base import BaseTestCase
import json
import unittest
from flask import request


def register_user(self):
    return self.client.post(
        '/api/user/',
        data= json.dumps(dict(
            name='Junior',
            user_id='Olalekan@gmail.com',
            password='Kopenhagen',
            country='Nigerian',
            is_admin=False
        )),
        content_type='application/json'
        )


class TestCreateUser(BaseTestCase):


    def test_register_new_user_view(self):
        """
        test_register_new_user Tests the user regusteration endpoint
        """
        with self.client:
            response= register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data["message"] == "successfully created")
            self.assertTrue(isinstance(data["authentication"], str))
            self.assertTrue(request.path == '/api/user/')
            self.assertTrue(response.status_code == 200)

    def test_get_all_users_view(self):
        """
        test_get_all_users_view test the /api/user/ endpoint that returns a all the  users
        """
        response =  self.client.get(
            path='/api/user/',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 200)
        self.assertTrue(isinstance(data["data"], list))
        self.assertTrue(response.content_type == 'application/json')

    def test_get_user_view(self):
        """
        test_get_user test the /api/user/ endpoint that returns a single user
        """
        with self.client:
            register_user(self)
            response = self.client.get(path='/api/user/Olalekan@gmail.com', content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data["name"])
            self.assertTrue(isinstance(data["name"], str))
            self.assertTrue(response.status_code == 200)
            self.assertTrue(response.content_type == 'application/json')

    def test_update_user_view(self):
        """
        test_update_user_view test the update user endpoint , the user must be an existing user
        """
        with self.client:
            register_user(self)
            response = self.client.put(
                path='/api/user/Olalekan@gmail.com',
                data=json.dumps(dict(
                name='Junior',
                password='lekanAdebari',
                country='Nigerian',
                )),
                content_type='application/json')
            # data = json.loads(response.data.decode())
            self.assertTrue(response.status_code == 204)

    def test_delete_user_view(self):
        """
        test_delete_user_view test the user delete endpoint
        """

        with self.client:
            register_user(self)
            response = self.client.delete(
                path='/api/user/Olalekan@gmail.com',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(response.status_code == 201)
            self.assertTrue(response.content_type == 'application/json')

    # def test_get_user_biz(self):
    #     """
    #     test_get_user_biz test the endpoint that returns all the businesses of a user
    #     """
    #     with self.client:
    #         register_user(self)
    #         response = self.client.get(
    #             path='api/user/business/Olalekan@gmail.com',
    #             content_type='application/json'
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertTrue()
    #         self.assertTrue(response.status_code == 200)
    #         self.assertTrue(response.content_type == 'application/json')