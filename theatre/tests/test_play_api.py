from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import Play


class PlayViewSetTests(APITestCase):
    def setUp(self):
        self.adminuser = get_user_model().objects.create_user(
            email="admin@example.com",
            password="testpassword",
            is_superuser=True,
            is_staff=True,
        )
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        content_type = ContentType.objects.get_for_model(Play)
        permission, created = Permission.objects.get_or_create(
            codename="can_create_play",
            name="Can Create Play",
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.adminuser.user_permissions.add(permission)

        self.client.force_authenticate(user=self.user)

    def test_list_plays(self):
        url = "/api/theatre/plays/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Play.objects.count())

    def test_create_play(self):
        url = "/api/theatre/plays/"
        data = {
            "title": "Test title",
            "description": ("Title that can...")
        }
        self.client.force_authenticate(user=self.adminuser)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Play.objects.get(title="Test title").title, "Test title"
        )
        self.assertEqual(
            Play.objects.get(description="Title that can...").description,
            "Title that can...",
        )

    def test_retrieve_play(self):
        play = Play.objects.create(
            title="Test Play",
            description="Test Description",
        )
        url = f"/api/theatre/plays/{play.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], play.id)
        self.assertEqual(response.data["title"], play.title)
        self.assertEqual(response.data["description"], play.description)
