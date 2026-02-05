from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from promocode.models import Promocode, ListModel, MainModel, TestModel
import tempfile
import os


class PromocodeModelTest(TestCase):
    """Тесты для модели Promocode"""

    def setUp(self):
        self.promocode = Promocode.objects.create(
            promocode="TEST2024",
            description="Тестовый промокод"
        )

    def test_promocode_creation(self):
        """Тест создания промокода"""
        self.assertEqual(self.promocode.promocode, "TEST2024")
        self.assertEqual(self.promocode.description, "Тестовый промокод")

    def test_promocode_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.promocode), "TEST2024")

    def test_promocode_verbose_names(self):
        """Тест verbose_name полей"""
        field_labels = {
            'promocode': 'Promocode',
            'description': 'Description'
        }

        for field, expected_label in field_labels.items():
            with self.subTest(field=field):
                field_label = self.promocode._meta.get_field(field).verbose_name
                self.assertEqual(field_label, expected_label)

    def test_promocode_max_length(self):
        """Тест максимальной длины полей"""
        max_length = self.promocode._meta.get_field('promocode').max_length
        self.assertEqual(max_length, 100)

    def test_promocode_meta_verbose_names(self):
        """Тест verbose_name модели"""
        self.assertEqual(Promocode._meta.verbose_name, "Promocode")
        self.assertEqual(Promocode._meta.verbose_name_plural, "Promocodes")


class ListModelTest(TestCase):
    """Тесты для модели ListModel"""

    def setUp(self):
        self.list_model = ListModel.objects.create(title="Test List")

    def test_list_model_creation(self):
        """Тест создания ListModel"""
        self.assertEqual(self.list_model.title, "Test List")

    def test_list_model_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.list_model), "Test List")

    def test_list_model_title_max_length(self):
        """Тест максимальной длины title"""
        max_length = self.list_model._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)


class MainModelTest(TestCase):
    """Тесты для модели MainModel"""

    def setUp(self):
        self.list_model = ListModel.objects.create(title="Main List")
        self.main_model = MainModel.objects.create(
            title="Main Model Test",
            system="Test System",
            created_at="2024-01-01",
            updated_at="2024-01-02",
            active=True,
            list=self.list_model
        )

    def test_main_model_creation(self):
        """Тест создания MainModel"""
        self.assertEqual(self.main_model.title, "Main Model Test")
        self.assertEqual(self.main_model.system, "Test System")
        self.assertEqual(str(self.main_model.created_at), "2024-01-01")
        self.assertEqual(str(self.main_model.updated_at), "2024-01-02")
        self.assertTrue(self.main_model.active)
        self.assertEqual(self.main_model.list, self.list_model)

    def test_main_model_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.main_model), "Main Model Test")

    def test_main_model_foreign_key_relation(self):
        """Тест связи ForeignKey"""
        self.assertEqual(self.main_model.list.title, "Main List")

    def test_main_model_default_values(self):
        """Тест значений по умолчанию"""
        new_main_model = MainModel.objects.create(
            title="New Model",
            system="System"
        )
        self.assertTrue(new_main_model.active)  # default=True
        self.assertIsNone(new_main_model.created_at)  # null=True, blank=True
        self.assertIsNone(new_main_model.updated_at)  # null=True, blank=True
        self.assertIsNone(new_main_model.list)  # null=True

    def test_main_model_meta_verbose_names(self):
        """Тест verbose_name модели"""
        self.assertEqual(MainModel._meta.verbose_name, "Main Model")
        self.assertEqual(MainModel._meta.verbose_name_plural, "Main Model")


class TestModelTest(TestCase):
    """Тесты для модели TestModel"""

    def setUp(self):
        # Создаем временные файлы для тестирования
        self.temp_image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        self.temp_file = SimpleUploadedFile(
            "test_file.txt",
            b"text content",
            content_type="text/plain"
        )

        self.main_model = MainModel.objects.create(
            title="Test Main",
            system="System"
        )

        self.test_model = TestModel.objects.create(
            text="<p>Тестовый текст</p>",
            number=42,
            date="2024-01-01",
            image=self.temp_image,
            file=self.temp_file,
            is_active=True,
            main=self.main_model
        )

    def tearDown(self):
        """Очистка после тестов"""
        if self.test_model.image:
            if os.path.exists(self.test_model.image.path):
                os.remove(self.test_model.image.path)

        if self.test_model.file:
            if os.path.exists(self.test_model.file.path):
                os.remove(self.test_model.file.path)

    def test_test_model_creation(self):
        """Тест создания TestModel"""
        self.assertEqual(self.test_model.text, "<p>Тестовый текст</p>")
        self.assertEqual(self.test_model.number, 42)
        self.assertEqual(str(self.test_model.date), "2024-01-01")
        self.assertTrue(self.test_model.is_active)
        self.assertEqual(self.test_model.main, self.main_model)

    def test_test_model_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.test_model), "<p>Тестовый текст</p>")

    def test_test_model_foreign_key_relation(self):
        """Тест связи с MainModel"""
        self.assertEqual(self.test_model.main.title, "Test Main")

    def test_test_model_optional_fields(self):
        """Тест необязательных полей"""
        test_model_without_files = TestModel.objects.create(
            text="Text without files",
            number=100,
            main=self.main_model
        )

        self.assertIsNone(test_model_without_files.date)
        self.assertIsNone(test_model_without_files.image)
        self.assertIsNone(test_model_without_files.file)

    def test_test_model_related_name(self):
        """Тест related_name связи"""
        # Проверяем, что MainModel имеет доступ к связанным TestModel через 'tests'
        related_tests = self.main_model.tests.all()
        self.assertEqual(related_tests.count(), 1)
        self.assertEqual(related_tests.first(), self.test_model)

    def test_test_model_default_values(self):
        """Тест значений по умолчанию"""
        new_test_model = TestModel.objects.create(
            text="New text",
            number=1,
            main=self.main_model
        )
        self.assertTrue(new_test_model.is_active)  # default=True

    def test_test_model_file_fields(self):
        """Тест полей файлов"""
        self.assertTrue(self.test_model.image.name.endswith("test_image.jpg"))
        self.assertTrue(self.test_model.file.name.endswith("test_file.txt"))

    def test_test_model_meta_verbose_names(self):
        """Тест verbose_name модели"""
        self.assertEqual(TestModel._meta.verbose_name, "Test Model")
        self.assertEqual(TestModel._meta.verbose_name_plural, "Test Model")


class ModelRelationsTest(TestCase):
    """Тесты связей между моделями"""

    def setUp(self):
        self.list_model = ListModel.objects.create(title="List 1")
        self.main_model = MainModel.objects.create(
            title="Main 1",
            system="S1",
            list=self.list_model
        )

        # Создаем несколько TestModel для одного MainModel
        for i in range(3):
            TestModel.objects.create(
                text=f"Test {i}",
                number=i,
                main=self.main_model
            )

    def test_one_to_many_relation(self):
        """Тест связи один-ко-многим (ListModel -> MainModel)"""
        # Один ListModel может иметь несколько MainModel
        main2 = MainModel.objects.create(
            title="Main 2",
            system="S2",
            list=self.list_model
        )

        self.assertEqual(self.list_model.mainmodel_set.count(), 2)

    def test_one_to_many_relation2(self):
        """Тест связи один-ко-многим (MainModel -> TestModel)"""
        # Один MainModel может иметь несколько TestModel
        self.assertEqual(self.main_model.tests.count(), 3)

    def test_cascade_delete(self):
        """Тест каскадного удаления"""
        # При удалении MainModel должны удалиться все связанные TestModel
        test_count_before = TestModel.objects.count()
        self.main_model.delete()
        test_count_after = TestModel.objects.count()

        self.assertEqual(test_count_after, test_count_before - 3)

    def test_related_name_access(self):
        """Тест доступа через related_name"""
        # Проверяем доступ к связанным объектам через related_name
        tests = self.main_model.tests.all()
        self.assertEqual(tests.count(), 3)

        for test in tests:
            self.assertEqual(test.main, self.main_model)