from main import app
import json
import unittest


class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """

    def test_get_all_books(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    # TODO: unittest for another apis

    def test_register(self):
        user = {
            "username": "huynew3",
            "password": "123"
        }
        request, response = app.test_client.post('auth/register', json = user)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data['status'], 'success')
        auth_token = data["token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        return headers
    def test_login(self):

        user = {
            "username": "huy",
            "password": "123"
        }
        request, response = app.test_client.post('auth/login', json = user)
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data['status'], 'success')
        auth_token = data["token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        return headers
    def test_create_book(self):
        # Define a test book
        headers = self.test_login()
        print("header: ", headers)
        book = {
          "title": "a very new test 2",
          "authors": ["huy"],
          "description": "The test book in the huy series.",
          "publisher": "2024"
        }

        # Make a POST request to create the book
        request, response = app.test_client.post('/books', json = book, headers = headers)

        # Assert the response status code is 200
        self.assertEqual(response.status, 200)


        # Assert the response contains the expected data
        data = json.loads(response.text)
        self.assertEqual(data['status'], 'success')

        # Assert the book is now in the list of books
        request, response = app.test_client.get('/books')
        data = json.loads(response.text)
        books = data['books']
        self.assertTrue(any(b['title'] == 'test huy' for b in books))

    def test_get_book_by_id(self):
        book_id = '10729227-e701-42ae-9db9-21ab2778cce2'
        request, response = app.test_client.get(f'/books/{book_id}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('_id'), '10729227-e701-42ae-9db9-21ab2778cce2')

    def test_update_book(self):
        # Define a test book
        headers = self.test_login()
        print("header: ", headers)
        update_title= "new test 01"
        update_book = {
          "title": update_title
        }
        book_id = '10729227-e701-42ae-9db9-21ab2778cce2'

        # Make a POST request to create the book
        request, response = app.test_client.put(f'/books/{book_id}', json = update_book, headers = headers)

        # Assert the response status code is 200
        self.assertEqual(response.status, 200)


        # Assert the response contains the expected data
        data = json.loads(response.text)
        self.assertEqual(data['status'], 'success')

        # Assert the book is now in the list of books
        request, response = app.test_client.get(f'/books/{book_id}')
        data = json.loads(response.text)
        self.assertEqual(data["title"], update_title)

    def test_delete_book(self):
        # Define a test book
        headers = self.test_login()
        print("header: ", headers)
        book_id = '3e6530ea-111b-4b9a-a160-21df718c6df2'

        request, response = app.test_client.delete(f'/books/{book_id}', headers = headers)

        # Assert the response status code is 200
        self.assertEqual(response.status, 200)


        data = json.loads(response.text)
        self.assertEqual(data['status'], 'success')

        request, response = app.test_client.get(f'/books/{book_id}')
        self.assertEqual(response.status, 500)


if __name__ == '__main__':
    unittest.main()
