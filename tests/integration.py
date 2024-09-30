from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Techniques

class IntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_get_technique(self):
        data = {
            "technique": "Integration Technique",
            "description": "Integration Description",
            "scope_global": True,
            "scope_local": False,
            "model_dependency": "Integration Dependency",
            "example_use_case": "Integration Use Case"
        }
        create_response = self.client.post('/api/techniques/', data, format='json')
        self.assertEqual(create_response.status_code, 201)

        get_response = self.client.get(f'/api/techniques/{create_response.data["id"]}/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.data['technique'], "Integration Technique")