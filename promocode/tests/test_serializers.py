from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from promocode.models import Promocode, ListModel, MainModel, TestModel
from promocode.serializers import (
    PromocodeSerializer,
    TestModelSerializer,
    MainModelSerializer
)
import os


class PromocodeSerializerTest(TestCase):
    """Тесты для сериализатора PromocodeSerializer"""

    def setUp(self):
        self.promocode_data = {
            'promocode': 'SERIAL2024',
            'description': 'Сериализованный промокод'
        }
        self.promocode = Promocode.objects.create(**self.promocode_data)
        self.serializer = PromocodeSerializer(instance=self.promocode)

    def test_serializer_contains_expected_fields(self):
        """Тест наличия всех полей в сериализаторе"""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'promocode', 'description'])

    def test_serializer_field_content(self):
        """Тест содержимого полей сериализатора"""
        data = self.serializer.data
        self.assertEqual(data['promocode'], 'SERIAL2024')
        self.assertEqual(data['description'], 'Сериализованный промокод')

    def test_serializer_create(self):
        """Тест создания объекта через сериализатор"""
        new_data = {
            'promocode': 'NEW2024',
            'description': 'Новый промокод'
        }
        serializer = PromocodeSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())

        promocode = serializer.save()
        self.assertEqual(promocode.promocode, 'NEW2024')
        self.assertEqual(promocode.description, 'Новый промокод')

    def test_serializer_update(self):
        """Тест обновления объекта через сериализатор"""
        update_data = {'description': 'Обновленное описание'}
        serializer = PromocodeSerializer(
            instance=self.promocode,
            data=update_data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())

        updated_promocode = serializer.save()
        self.assertEqual(updated_promocode.description, 'Обновленное описание')

    def test_serializer_validation(self):
        """Тест валидации сериализатора"""
        # Невалидные данные (слишком длинный промокод)
        invalid_data = {
            'promocode': 'A' * 101,  # больше 100 символов
            'description': 'Test'
        }
        serializer = PromocodeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('promocode', serializer.errors)


class TestModelSerializerTest(TestCase):
    """Тесты для сериализатора TestModelSerializer"""

    def setUp(self):
        self.main_model = MainModel.objects.create(
            title="Test Main",
            system="System"
        )

        self.test_model = TestModel.objects.create(
            text="<p>Тестовый текст</p>",
            number=42,
            main=self.main_model
        )

        self.serializer = TestModelSerializer(instance=self.test_model)

    def test_serializer_contains_expected_fields(self):
        """Тест наличия всех полей в сериализаторе"""
        data = self.serializer.data
        expected_fields = [
            'id', 'text', 'number', 'date', 'image', 'file',
            'is_active', 'main', 'file_path'
        ]

        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, data)

    def test_file_path_method_field(self):
        """Тест метода file_path"""
        # Создаем TestModel с файлом
        test_file = SimpleUploadedFile(
            "test.txt",
            b"content",
            content_type="text/plain"
        )

        test_with_file = TestModel.objects.create(
            text="Text with file",
            number=1,
            file=test_file,
            main=self.main_model
        )

        serializer = TestModelSerializer(instance=test_with_file)
        self.assertIsNotNone(serializer.data['file_path'])

        # Удаляем временный файл
        if os.path.exists(test_with_file.file.path):
            os.remove(test_with_file.file.path)

    def test_file_path_without_file(self):
        """Тест file_path когда файла нет"""
        data = self.serializer.data
        self.assertIsNone(data['file_path'])

    def test_serializer_relation_field(self):
        """Тест поля связи с MainModel"""
        data = self.serializer.data
        self.assertEqual(data['main'], self.main_model.id)


class MainModelSerializerTest(TestCase):
    """Тесты для сериализатора MainModelSerializer"""

    def setUp(self):
        self.list_model = ListModel.objects.create(title="List 1")

        self.main_model = MainModel.objects.create(
            title="Main Serializer",
            system="Serializer System",
            list=self.list_model
        )

        # Создаем связанные TestModel
        for i in range(2):
            TestModel.objects.create(
                text=f"Test {i}",
                number=i * 10,
                main=self.main_model
            )

        self.serializer = MainModelSerializer(instance=self.main_model)

    def test_serializer_contains_expected_fields(self):
        """Тест наличия всех полей в сериализаторе"""
        data = self.serializer.data

        # Проверяем основные поля
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('system', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertIn('active', data)
        self.assertIn('list', data)

        # Проверяем вложенные тесты
        self.assertIn('tests', data)

    def test_serializer_nested_tests(self):
        """Тест вложенных TestModel"""
        data = self.serializer.data
        self.assertEqual(len(data['tests']), 2)

        # Проверяем структуру первого вложенного объекта
        first_test = data['tests'][0]
        self.assertIn('id', first_test)
        self.assertIn('text', first_test)
        self.assertIn('number', first_test)
        self.assertIn('file_path', first_test)

    def test_serializer_without_related_tests(self):
        """Тест сериализатора без связанных тестов"""
        new_main = MainModel.objects.create(
            title="Empty Main",
            system="Empty"
        )

        serializer = MainModelSerializer(instance=new_main)
        data = serializer.data
        self.assertEqual(len(data['tests']), 0)  # Пустой список

    def test_serializer_read_only_tests(self):
        """Тест что tests поле read_only"""
        # Пытаемся создать MainModel с tests через сериализатор
        test_data = {
            'title': 'New Main',
            'system': 'New System',
            'tests': [{'text': 'Test', 'number': 1}]
        }

        serializer = MainModelSerializer(data=test_data)
        # tests должно игнорироваться при создании
        self.assertTrue(serializer.is_valid())

        main = serializer.save()
        self.assertEqual(main.tests.count(), 0)  # tests не создались

    def test_serializer_list_field(self):
        """Тест поля связи с ListModel"""
        data = self.serializer.data
        self.assertEqual(data['list'], self.list_model.id)