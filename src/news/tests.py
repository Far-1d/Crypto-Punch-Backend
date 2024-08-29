from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from account.models import User
from account.tests import SampleUser
from news.models import News, Category

# Create your tests here.

class PrepSetUpTestCase(APITestCase):
    sample = {
        "title":"test sample title",
        "image":"https://static.vecteezy.com/system/resources/previews/006/638/978/non_2x/tunnel-corridor-hexagon-texture-technology-modern-futuristic-science-fiction-background-3d-illustration-free-photo.jpg",
        "content":"<h1>Hello</h1><p> world</p>",
        "category":"testing",
        "status":"published",
        "writer":""
    }
    sample_user = SampleUser()
    
    def setUp(self):
        sample = self.sample.copy()
        user = self.sample_user.create_single_user()
        sample['writer'] = user

        category , _ = Category.objects.get_or_create(name=sample['category'])
        sample['category'] = category

        for i in range(50):
            data = sample.copy()
            data['title'] = data['title']+f" {i}" 
            News.objects.create(**data)


class NewsCreateTest(APITestCase):
    sample_user = SampleUser()
    url = 'http://127.0.0.1:8000/api/news/create'
    sample = {
        "title":"test sample title",
        "image":"https://static.vecteezy.com/system/resources/previews/006/638/978/non_2x/tunnel-corridor-hexagon-texture-technology-modern-futuristic-science-fiction-background-3d-illustration-free-photo.jpg",
        "content":"<h1>Hello</h1><p> world</p>",
        "category":"testing",
        "status":"published",
        "user_token":""
    }

    def setUp(self):
        sample = self.sample.copy()
        user = self.sample_user.create_single_user()

    def test_create_news_valid(self):
        """
        Validate news creation view with valid data
        """
        sample = self.sample.copy()
        sample['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            News.objects.count(), 1
        ) 
        self.assertEqual(
            News.objects.first().title, sample['title']
        )
    
    def test_create_news_incomplete(self):
        """
        not complete sample 
        """
        sample1 = self.sample.copy()
        sample1['title'] = "  "
        sample1['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample1, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        sample2 = self.sample.copy()
        sample2['content'] = "  "
        sample2['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample2, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
    
        sample3 = self.sample.copy()
        sample3['category'] = "  "
        sample3['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample3, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        sample4 = self.sample.copy()
        sample4['image'] = "  "
        sample4['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample4, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        sample5 = self.sample.copy()
        sample5['status'] = "  "
        sample5['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample5, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_news_bad_status(self):
        """
        bad formatted status field
        """
        sample5 = self.sample.copy()
        sample5['status'] = "x"
        sample5['user_token'] = self.sample_user.get_token()
        response = self.client.post(self.url, sample5, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_news_with_no_token(self):
        """
        no user token provided
        """
        sample = self.sample.copy()
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

# class NewsListTest(PrepSetUpTestCase):
#     url = 'http://127.0.0.1:8000/api/news?page={}&page_size={}'
#     def test_news_list_wrong_format(self):
#         """
#         Ensure news listing with no page and page size
#         """
#         response = self.client.get(self.url.format('',''), format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_200_OK
#         )
#         response = self.client.get(self.url.format('-1',''), format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_404_NOT_FOUND
#         )
#         response = self.client.get(self.url.format('a',''), format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_404_NOT_FOUND
#         )
#         response = self.client.get(self.url.format('1','a'), format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_404_NOT_FOUND
#         )

class NewsPageTest(PrepSetUpTestCase):
    url = 'http://127.0.0.1:8000/api/news/pages/{}'
    
    def test_news_pages_wrong_format(self):
        response = self.client.get(self.url.format(''), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

        response = self.client.get(self.url.format('-2'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

        response = self.client.get(self.url.format('0'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

class NewsGetTest(PrepSetUpTestCase):
    url = 'http://127.0.0.1:8000/api/news/get/{}'

    def test_get_news_wrong_format(self):
        response = self.client.get(self.url.format('a'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        response = self.client.get(self.url.format('-1'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        response = self.client.get(self.url.format('0.5'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
    
    def test_get_news_non_existant(self):
        response = self.client.get(self.url.format('1000'), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_get_news_valid(self):
        """
        test valid get news
        """
        id = News.objects.only('id').first().id
        response = self.client.get(self.url.format(id), format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

class NewLikeTest(PrepSetUpTestCase):
    url  = 'http://127.0.0.1:8000/api/news/like'
    def test_like_no_user(self):
        news_id = News.objects.first().id
        sample = {
            "news_id":news_id,
            "user_id": ''
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        sample = {
            "news_id":news_id,
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_like_non_existant_user(self):
        news_id = News.objects.first().id
        sample = {
            "news_id":news_id,
            "user_id": '1000'
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_like_no_news(self):
        sample = {
            "news_id":'',
            "user_id": '1'
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

        sample = {
            "user_id": '1'
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        
    def test_like_non_existant_news(self):
        sample = {
            "news_id":'1000',
            "user_id": '1'
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_like_and_unlike(self):
        news_id = News.objects.first().id
        user_id = User.objects.first().id
        sample = {
            "news_id":news_id,
            "user_id":user_id
        }
        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["message"], "liked"
        )

        response = self.client.post(self.url, sample, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["message"], "unliked"
        )
