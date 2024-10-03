from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task, Category
from users.models import User


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        
        # Create a second user for testing ownership
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass', email='otheruser@example.com')
        self.category = Category.objects.create(name='Test Category', user=self.user)

        # create a tasks for test
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            due_date='2025-09-30',
            priority='high',
            user=self.user
        )

        self.task = Task.objects.create(
            title='Another Task',
            description='Task Description',
            due_date='2025-10-30',
            priority='high',
            user=self.user
        )

        # Generate JWT tokens for the test user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_create_task(self):
        url = reverse('Task-create')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'due_date': '2025-10-01',
            'priority': 'Medium',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)  # ensure the new task is created in addition to the existing two
   
    def test_create_task_missing_title(self):
        url = reverse('Task-create')
        data = {
            'description': 'New Task Description',
            'due_date': '2025-10-01',
            'priority': 'Medium'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 2) # ensure the task is not created

    def test_create_task_with_unauthenticated_user(self):
        url = reverse('Task-create')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'due_date': '2025-10-01',
            'priority': 'Medium',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
       
    def test_create_duplicate_task(self):
        url = reverse('Task-create')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'due_date': '2025-10-01',
            'priority': 'Medium',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        
        # duplicate
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('task with this title already exists.', response.data['title'])
        error_detail = response.data["title"][0]
        self.assertEqual(error_detail.code, 'unique')
        self.assertEqual(Task.objects.count(), 3)

    def test_list_tasks(self):
        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure the response contains the user's task

    def test_list_tasks_with_unauthenticated_user(self):
        url = reverse('Task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_detail(self):
        url = reverse('Task-detail', kwargs={'title': self.task.title})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)
 
    def test_task_detail_with_unexisting_task(self):
        url = reverse('Task-detail', kwargs={'title': 'don`t exist'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        url = reverse('Task-delete', kwargs={'title': self.task.title})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)  # Task should be deleted

    def test_delete_unexisting_task(self):
        url = reverse('Task-delete', kwargs={'title': 'don`t exist'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_update(self):
        url = reverse('Task-create')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            'title': 'update test',
            'description': 'Test the functionality of the updating feature.',
            'due_date': '2025-10-10',
            'priority': 'Low'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Task-update', kwargs = {'title': self.task.title})
        data = {
            'title': 'updated title',
            'description': 'description',
            'due_date': '2025-10-12',
            'priority': 'High',
            'status': 'Completed'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_tasks(self):

        Task.objects.create(
            title ='Unrelated Task',
            description ='Different Task with the description to search with.',
            due_date ='2025-10-06',
            priority ='Medium',
            user = self.user
        )
        # test search with title 
        url = reverse('Task-list')  # Assuming you support search via query params
        search_term = 'Another'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(f'{url}?title={search_term}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the matching task should be returned
        self.assertEqual(response.data[0]['title'], 'Another Task')

        # test search with description
        url = reverse('Task-list')  # Assuming you support search via query params
        search_term = 'Different Task'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(f'{url}?description={search_term}')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the matching task should be returned
        self.assertIn('Different Task with the', response.data[0]['short_description'])

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        Task.objects.create(
            title='Low Priority Task',
            description='Low Priority Task Description',
            due_date='2025-10-05',
            priority='low',
            user=self.user
        )
        Task.objects.create(
            title='Medium Priority Task',
            description='Medium Priority Task Description',
            due_date='2024-10-10',
            priority='medium',
            user=self.user
        )

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Filter by priority = low
        response = self.client.get(f'{url}?priority=low')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Low Priority Task')

        # Filter by priority = medium
        response = self.client.get(f'{url}?priority=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Medium Priority Task')

        # assertion of the test

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_tasks_by_status(self):
        Task.objects.create(
            title='Completed Task',
            description='Low Priority Task Description',
            due_date='2025-10-05',
            priority='low',
            status = 'Completed',
            user=self.user
        )
        Task.objects.create(
            title='Pending Task',
            description='Medium Priority Task Description',
            due_date='2024-10-10',
            priority='medium',
            status = 'Pending',
            user=self.user
        )

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Filter status cCompleted
        response = self.client.get(f'{url}?status=Completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

        # Filter by status = pending
        response = self.client.get(f'{url}?status=Pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Pending Task')

        # assertion of the test

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_sort_tasks_by_due_date(self):
        """Test sorting tasks by due_date."""
        Task.objects.create(
            title='Earlier Task',
            description='Earlier Task Description',
            due_date='2025-09-20',
            priority='medium',
            user=self.user
        )
        Task.objects.create(
            title='Later task',
            description='Medium Priority Task Description',
            due_date='2025-10-10',
            priority='medium',
            user=self.user
        )

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Sort by due_date in ascending order
        response = self.client.get(f'{url}?sort_by=due_date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Earlier Task')
        self.assertEqual(response.data[1]['title'], 'Test Task')
        self.assertEqual(response.data[2]['title'], 'Later task')

        # Sort by due_date in descending order
        response = self.client.get(f'{url}?sort_by=due_date&sort_order=desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Another Task')
        self.assertEqual(response.data[1]['title'], 'Later task')

    # assertion of the test

        url = reverse('Task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_category(self):
        url = reverse('Category-create')
        data = {
            'name': 'New Category'
            }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2) 

    def test_create_category_with_unauthenticated_user(self):
        url = reverse('Category-create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('Category-create')
        data = {
            'name': 'test category'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Category-update', kwargs = {'name': self.category.name})
        data = {
            'name': 'updated name'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated name')

    def test_delete_category(self):
        url = reverse('Category-delete', kwargs={'name': self.category.name})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  # Category should be deleted

    def test_delete_unexisting_category(self):
        url = reverse('Category-delete', kwargs={'name': 'don`t exist'})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_task_access(self):
        url = reverse('Task-detail', kwargs={'title': self.task.title})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')  # Logged in as testuser
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should be able to access own task

        # Now test accessing the task with the other user (not the owner)
        self.client.logout()
        other_refresh = RefreshToken.for_user(self.other_user)
        other_access_token = str(other_refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {other_access_token}')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 