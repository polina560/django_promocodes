from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json

from promocode.models import Promocode, MainModel, TestModel, ListModel


class GetPromocodeAPITest(APITestCase):
    """Тесты для API GetPromocode"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('random-promocode')  # Нужно задать name в urls.py

        # Создаем тестовые промокоды
        self.promocodes = [
            Promocode.objects.create(
                promocode=f"CODE{i}",
                description=f"Description {i}"
            )
            for i in range(5)
        ]

    def test_get_promocode_success(self):
        """Тест успешного получения случайного промокода"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем что ответ содержит один из созданных промокодов
        response_data = response.data
        self.assertIsInstance(response_data, str)

        # Получаем список всех возможных промокодов
        all_codes = [p.promocode for p in self.promocodes]
        self.assertIn(response_data, all_codes)

    def test_get_promocode_no_promocodes(self):
        """Тест когда нет промокодов"""
        # Удаляем все промокоды
        Promocode.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "No promocodes available"})

    def test_get_promocode_only_one(self):
        """Тест когда только один промокод"""
        Promocode.objects.exclude(id=self.promocodes[0].id).delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "CODE0")

    def test_get_promocode_randomness(self):
        """Тест случайности выбора промокода"""
        # Запускаем несколько запросов и собираем результаты
        results = []
        for _ in range(20):
            response = self.client.get(self.url)
            results.append(response.data)

        # Проверяем что были разные результаты (с некоторой вероятностью)
        unique_results = set(results)
        self.assertGreater(len(unique_results), 1)

    def test_method_not_allowed(self):
        """Тест что другие методы HTTP не разрешены"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class MainModelDataAPITest(APITestCase):
    """Тесты для API MainModelData"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('mainmodel-data')  # Нужно задать name в urls.py

        # Создаем тестовые данные
        self.list_model = ListModel.objects.create(title="Test List")

        self.main_models = []
        for i in range(3):
            main = MainModel.objects.create(
                title=f"Main Model {i}",
                system=f"System {i}",
                list=self.list_model,
                active=(i % 2 == 0)  # Чередуем активные/неактивные
            )

            # Добавляем связанные TestModel
            for j in range(2):
                TestModel.objects.create(
                    text=f"Test {i}-{j}",
                    number=(i * 10) + j,
                    main=main
                )

            self.main_models.append(main)

    def test_get_mainmodel_list_success(self):
        """Тест успешного получения списка MainModel"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_response_structure(self):
        """Тест структуры ответа"""
        response = self.client.get(self.url)

        # Проверяем первый элемент
        first_item = response.data[0]

        # Основные поля
        self.assertIn('id', first_item)
        self.assertIn('title', first_item)
        self.assertIn('system', first_item)
        self.assertIn('created_at', first_item)
        self.assertIn('updated_at', first_item)
        self.assertIn('active', first_item)
        self.assertIn('list', first_item)

        # Вложенные тесты
        self.assertIn('tests', first_item)
        self.assertEqual(len(first_item['tests']), 2)

    def test_nested_tests_structure(self):
        """Тест структуры вложенных TestModel"""
        response = self.client.get(self.url)
        first_item = response.data[0]

        # Проверяем первый вложенный TestModel
        first_test = first_item['tests'][0]

        self.assertIn('id', first_test)
        self.assertIn('text', first_test)
        self.assertIn('number', first_test)
        self.assertIn('date', first_test)
        self.assertIn('image', first_test)
        self.assertIn('file', first_test)
        self.assertIn('is_active', first_test)
        self.assertIn('main', first_test)
        self.assertIn('file_path', first_test)

    def test_empty_list(self):
        """Тест пустого списка"""
        # Удаляем все MainModel
        MainModel.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_method_not_allowed(self):
        """Тест что другие методы HTTP не разрешены для ListAPIView"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filtering_by_active(self):
        """Тест фильтрации (можно добавить позже)"""
        # Этот тест можно реализовать, если добавите фильтрацию
        pass


class APIIntegrationTest(APITestCase):
    """Интеграционные тесты API"""

    def setUp(self):
        self.client = APIClient()

        # Создаем данные для всех тестов
        for i in range(3):
            Promocode.objects.create(
                promocode=f"INTEGRATION{i}",
                description=f"Integration test {i}"
            )

    def test_multiple_api_calls(self):
        """Тест нескольких последовательных вызовов API"""
        # Тест GetPromocode
        promocode_response = self.client.get(reverse('random-promocode'))
        self.assertEqual(promocode_response.status_code, status.HTTP_200_OK)

        # Тест MainModelData (если есть данные)
        mainmodel_response = self.client.get(reverse('mainmodel-data'))
        self.assertEqual(mainmodel_response.status_code, status.HTTP_200_OK)

    def test_api_response_format(self):
        """Тест формата ответа API"""
        response = self.client.get(reverse('random-promocode'))

        # Проверяем что ответ в правильном формате
        self.assertIsInstance(response.data, str)

        # Для MainModelData
        if MainModel.objects.exists():
            response = self.client.get(reverse('mainmodel-data'))
            self.assertIsInstance(response.data, list)

    def test_api_performance(self):
        """Тест производительности API (базовый)"""
        import time

        start_time = time.time()

        # Делаем несколько запросов
        for _ in range(10):
            self.client.get(reverse('random-promocode'))

        end_time = time.time()
        execution_time = end_time - start_time

        # Проверяем что выполнение не занимает слишком много времени
        self.assertLess(execution_time, 5.0)  # 5 секунд максимум


class APIErrorHandlingTest(APITestCase):
    """Тесты обработки ошибок API"""

    def test_invalid_url(self):
        """Тест обращения к несуществующему URL"""
        response = self.client.get('/api/nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_database_error_simulation(self):
        """Тест симуляции ошибки базы данных"""
        # Можно добавить тесты для ошибок БД
        pass