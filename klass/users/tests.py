from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


# TODO - add tests for the custom user model


class UsersManagersTests(TransactionTestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            password="foo",
            clg_number="123456789",
            first_name="Your",
            last_name="Dad",
        )
        self.assertEqual(user.username, "your.d.89")
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.clg_number, "123456789")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="normal@user.com",
                password="466",
                clg_number="5454551",
                first_name="Your",
                last_name="Uncle",
            )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="another@user.com",
                password="meow",
                clg_number="888856789",
                first_name="Your",
                last_name="Dad",
            )
        user2 = User.objects.create_user(
            email="another@user.com",
            password="meow",
            clg_number="888856789",
            first_name="Your",
            last_name="Dad",
            random_suffix="0",
        )
        self.assertEqual(user2.username, "your.d.89.0")
        user3 = User.objects.create_user(
            email="extra@user.com",
            password="justcool",
            clg_number="59851574",
            first_name="FrIEdricieManYes",
            last_name="Dad",
        )
        self.assertEqual(user3.username, "friedriciema.d.74")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com",
            password="foo",
            clg_number="5556688777",
            first_name="Papa",
            last_name="Bear",
        )  # type: ignore[arg-type]
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.username, "papa.b.77")
        self.assertEqual(admin_user.clg_number, "5556688777")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_superuser()
            with self.assertRaises(IntegrityError):
                User.objects.create_superuser(
                    email="super@user.com",
                    password="466",
                    clg_number="5454551",
                    first_name="Your",
                    last_name="Uncle",
                )
            with self.assertRaises(IntegrityError):
                User.objects.create_superuser(
                    email="anothersuper@user.com",
                    password="meow",
                    clg_number="4446688777",
                    first_name="Your",
                    last_name="Uncle",
                )
        admin_user2 = User.objects.create_superuser(
            email="anothersuper@user.com",
            password="meow",
            clg_number="4446688777",
            first_name="Your",
            last_name="Uncle",
            random_suffix="8",
        )
        self.assertEqual(admin_user2.username, "your.u.77.8")
        admin_user3 = User.objects.create_superuser(
            email="extrasuper@user.com",
            password="omg",
            clg_number="852212167",
            first_name="BakedIEdricieManYes",
            last_name="Uncle",
        )
        self.assertEqual(admin_user3.username, "bakediedrici.u.67")
