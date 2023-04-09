from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from ..models import Account, Month, UserSettings
from ..utils import get_month_range

User = get_user_model()


class UserSettingsTest(TestCase):
    def setUp(self):
        self.settings = UserSettings.objects.create(currency="USD")

    def test_default_currency(self):
        self.assertEqual(self.settings.currency, "USD")

    def test_valid_currency(self):
        with self.assertRaises(ValidationError) as cm:
            self.settings.currency = "AUDK"
            self.settings.save()
        self.assertEqual(str(cm.exception), _('"AUDK" is not a valid choice.'))

    def test_valid_start_day_of_month(self):
        self.settings.start_day_of_month = 15
        self.settings.save()
        self.assertEqual(self.settings.start_day_of_month, 15)

    def test_invalid_start_day_of_month(self):
        with self.assertRaises(ValidationError) as cm:
            self.settings.start_day_of_month = 31
            self.settings.save()
        self.assertEqual(str(cm.exception), _("Value must be between 1 and 28."))


class MonthTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.month = Month.objects.create(
            user=cls.user, first_day=datetime.now().date(), override_last_day=False
        )

    def test_month_code(self):
        month_code = datetime.strftime(self.month.first_day, "%y%m")
        self.assertEqual(self.month.month_code, month_code)

    def test_override_last_day(self):
        last_day = datetime.now().date()
        _, expected_last_day = get_month_range(last_day.day, last_day)
        month2 = Month.objects.create(
            user=self.user, first_day=datetime.now().date(), override_last_day=True
        )
        self.assertEqual(month2.last_day, expected_last_day)

    def test_str(self):
        expected_str = (
            f"{self.month.first_day.strftime('%B')} {self.month.first_day.year}"
        )
        self.assertEqual(str(self.month), expected_str)
        self.assertEqual(str(self.month), expected_str)


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )

        # Create an account
        cls.account = Account.objects.create(
            user=cls.user,
            name="Test Account",
            account_type=Account.AccountType.CASH,
            current_balance=0.0,
            balance_can_be_negative=False,
            active=True,
            exclude_from_budget=False,
            show_on_dashboard=True,
            color="#7DD181",
        )

    def setUp(self):
        pass

    def test_created_at_auto_now_add(self):
        self.assertIsNotNone(self.account.created_at)

    def test_updated_at_auto_now(self):
        self.assertIsNotNone(self.account.updated_at)

    def test_ordering(self):
        objs = Account.objects.all()
        self.assertEqual(list(objs), list(objs.order_by("-created_at", "-updated_at")))

    def test_get_bg_color(self):
        expected_color = "bg-green-500"
        self.assertEqual(self.account.get_bg_color(), expected_color)

    def test_str(self):
        expected_name = "Test Account"
        self.assertEqual(str(self.account), expected_name)

    def test_text_color(self):
        expected_color = "black"
        self.assertEqual(self.account.text_color, expected_color)

    def test_absolute_url(self):
        expected_url = f"/wallet/accounts/{self.account.pk}/"
        self.assertEqual(self.account.get_absolute_url(), expected_url)

    def tearDown(self):
        pass
