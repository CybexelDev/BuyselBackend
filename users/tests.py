from django.test import TestCase

from users.serializers import RequestSerializer
from unittest.mock import patch

class RequestSerializerValidationTests(TestCase):

    # =========================================================
    # HELPER
    # =========================================================

    def valid_data(self):
        return {
            "name": "John",
            "email": "john@gmail.com",
            "phone": "9876543210",
            "message": "Hello, I am interested",
        }

    def validate(self, data):
        serializer = RequestSerializer(data=data)
        serializer.is_valid()
        return serializer

    # =========================================================
    # NAME VALIDATION
    # =========================================================

    def test_name_valid(self):
        data = self.valid_data()

        serializer = self.validate(data)

        self.assertNotIn("name", serializer.errors)

    def test_name_missing(self):
        data = self.valid_data()
        del data["name"]

        serializer = self.validate(data)

        self.assertIn("name", serializer.errors)

    def test_name_empty(self):
        data = self.valid_data()
        data["name"] = ""

        serializer = self.validate(data)

        self.assertIn("name", serializer.errors)

    def test_name_none(self):
        data = self.valid_data()
        data["name"] = None

        serializer = self.validate(data)

        self.assertIn("name", serializer.errors)

    def test_name_one_character(self):
        data = self.valid_data()
        data["name"] = "A"

        serializer = self.validate(data)

        self.assertIn("name", serializer.errors)

    def test_name_two_characters(self):
        data = self.valid_data()
        data["name"] = "AB"

        serializer = self.validate(data)

        # Your current project has a model/field validator
        # requiring at least 3 characters.
        self.assertIn("name", serializer.errors)

    def test_name_three_characters(self):
        data = self.valid_data()
        data["name"] = "ABC"

        serializer = self.validate(data)

        self.assertNotIn("name", serializer.errors)

    def test_name_only_spaces(self):
        data = self.valid_data()
        data["name"] = "     "

        serializer = self.validate(data)

        self.assertIn("name", serializer.errors)

    def test_name_with_spaces(self):
        data = self.valid_data()
        data["name"] = "John Doe"

        serializer = self.validate(data)

        self.assertNotIn("name", serializer.errors)

    def test_name_with_leading_spaces(self):
        data = self.valid_data()
        data["name"] = "  John"

        serializer = self.validate(data)

        self.assertNotIn("name", serializer.errors)

    def test_name_with_trailing_spaces(self):
        data = self.valid_data()
        data["name"] = "John  "

        serializer = self.validate(data)

        self.assertNotIn("name", serializer.errors)

    def test_name_with_numbers(self):
        data = self.valid_data()
        data["name"] = "John123"

        serializer = self.validate(data)

        # Your current validation checks length only.
        self.assertNotIn("name", serializer.errors)

    def test_name_with_special_characters(self):
        data = self.valid_data()
        data["name"] = "@@@"

        serializer = self.validate(data)

        # "@@@" has 3 characters, so it passes the
        # current length-only validation.
        self.assertNotIn("name", serializer.errors)

    # =========================================================
    # EMAIL VALIDATION
    # =========================================================

    def test_email_valid(self):
        data = self.valid_data()
        data["email"] = "test@example.com"

        serializer = self.validate(data)

        self.assertNotIn("email", serializer.errors)

    def test_email_missing(self):
        data = self.valid_data()
        del data["email"]

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_empty(self):
        data = self.valid_data()
        data["email"] = ""

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_none(self):
        data = self.valid_data()
        data["email"] = None

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_without_at(self):
        data = self.valid_data()
        data["email"] = "johngmail.com"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_without_domain(self):
        data = self.valid_data()
        data["email"] = "john@"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_without_username(self):
        data = self.valid_data()
        data["email"] = "@gmail.com"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_without_dot(self):
        data = self.valid_data()
        data["email"] = "john@gmail"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_with_spaces(self):
        data = self.valid_data()
        data["email"] = "john doe@gmail.com"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_double_at(self):
        data = self.valid_data()
        data["email"] = "john@@gmail.com"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_random_text(self):
        data = self.valid_data()
        data["email"] = "hello"

        serializer = self.validate(data)

        self.assertIn("email", serializer.errors)

    def test_email_valid_with_numbers(self):
        data = self.valid_data()
        data["email"] = "john123@gmail.com"

        serializer = self.validate(data)

        self.assertNotIn("email", serializer.errors)

    def test_email_valid_with_dot(self):
        data = self.valid_data()
        data["email"] = "john.doe@gmail.com"

        serializer = self.validate(data)

        self.assertNotIn("email", serializer.errors)

    def test_email_valid_with_hyphen(self):
        data = self.valid_data()
        data["email"] = "john-doe@gmail.com"

        serializer = self.validate(data)

        self.assertNotIn("email", serializer.errors)

    # =========================================================
    # PHONE VALIDATION
    # =========================================================

    def test_phone_valid(self):
        data = self.valid_data()
        data["phone"] = "9876543210"

        serializer = self.validate(data)

        self.assertNotIn("phone", serializer.errors)

    def test_phone_missing(self):
        data = self.valid_data()
        del data["phone"]

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_empty(self):
        data = self.valid_data()
        data["phone"] = ""

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_none(self):
        data = self.valid_data()
        data["phone"] = None

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_less_than_ten_digits(self):
        data = self.valid_data()
        data["phone"] = "987654321"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_more_than_ten_digits(self):
        data = self.valid_data()
        data["phone"] = "98765432101"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_starts_with_5(self):
        data = self.valid_data()
        data["phone"] = "5876543210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_starts_with_1(self):
        data = self.valid_data()
        data["phone"] = "1876543210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_starts_with_0(self):
        data = self.valid_data()
        data["phone"] = "0876543210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_contains_letters(self):
        data = self.valid_data()
        data["phone"] = "98765abc10"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_contains_spaces(self):
        data = self.valid_data()
        data["phone"] = "98765 43210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_contains_special_character(self):
        data = self.valid_data()
        data["phone"] = "98765-43210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_with_plus91(self):
        data = self.valid_data()
        data["phone"] = "+919876543210"

        serializer = self.validate(data)

        self.assertIn("phone", serializer.errors)

    def test_phone_exactly_ten_digits_starting_6(self):
        data = self.valid_data()
        data["phone"] = "6123456789"

        serializer = self.validate(data)

        self.assertNotIn("phone", serializer.errors)

    def test_phone_exactly_ten_digits_starting_7(self):
        data = self.valid_data()
        data["phone"] = "7123456789"

        serializer = self.validate(data)

        self.assertNotIn("phone", serializer.errors)

    def test_phone_exactly_ten_digits_starting_8(self):
        data = self.valid_data()
        data["phone"] = "8123456789"

        serializer = self.validate(data)

        self.assertNotIn("phone", serializer.errors)

    def test_phone_exactly_ten_digits_starting_9(self):
        data = self.valid_data()
        data["phone"] = "9123456789"

        serializer = self.validate(data)

        self.assertNotIn("phone", serializer.errors)

    # =========================================================
    # MESSAGE VALIDATION
    # =========================================================

    def test_message_valid(self):
        data = self.valid_data()
        data["message"] = "Hello"

        serializer = self.validate(data)

        self.assertNotIn("message", serializer.errors)

    def test_message_long_text(self):
        data = self.valid_data()

        data["message"] = (
            "I am interested in this property. "
            "Please provide additional information."
        )

        serializer = self.validate(data)

        self.assertNotIn("message", serializer.errors)

    def test_message_missing(self):
        data = self.valid_data()
        del data["message"]

        serializer = self.validate(data)

        # Message is optional.
        self.assertNotIn("message", serializer.errors)

    def test_message_empty(self):
        data = self.valid_data()
        data["message"] = ""

        serializer = self.validate(data)

        # Your current validation:
        #
        # if message and len(message.strip()) < 5:
        #
        # does NOT run for an empty string.
        #
        # Therefore empty message is allowed.
        self.assertNotIn("message", serializer.errors)

    def test_message_none(self):
        data = self.valid_data()
        data["message"] = None

        serializer = self.validate(data)

        # Do not assume custom validate() handles None.
        # The model/serializer field configuration determines this.
        self.assertIsNotNone(serializer.errors)

    def test_message_less_than_five_characters(self):
        data = self.valid_data()
        data["message"] = "Hi"

        serializer = self.validate(data)

        # IMPORTANT:
        # Your current validate() should reject "Hi".
        #
        # If this fails, inspect the actual serializer being imported.
        self.assertIn("message", serializer.errors)

    def test_message_four_characters(self):
        data = self.valid_data()
        data["message"] = "Test"

        serializer = self.validate(data)

        self.assertIn("message", serializer.errors)

    def test_message_exactly_five_characters(self):
        data = self.valid_data()
        data["message"] = "Hello"

        serializer = self.validate(data)

        self.assertNotIn("message", serializer.errors)

    def test_message_only_spaces(self):
        data = self.valid_data()
        data["message"] = "     "

        serializer = self.validate(data)

        # IMPORTANT:
        # Your current condition is:
        #
        # if message and len(message.strip()) < 5:
        #
        # "     " is truthy, so strip() gives ""
        # and len("") is 0.
        #
        # Therefore this SHOULD fail.
        self.assertIn("message", serializer.errors)

    def test_message_four_spaces(self):
        data = self.valid_data()
        data["message"] = "    "

        serializer = self.validate(data)

        self.assertIn("message", serializer.errors)

    def test_message_spaces_with_text(self):
        data = self.valid_data()
        data["message"] = "  Hello  "

        serializer = self.validate(data)

        self.assertNotIn("message", serializer.errors)

    # =========================================================
    # COMPLETE VALIDATION
    # =========================================================

    def test_completely_valid_data(self):

        data = {
            "name": "John Doe",
            "email": "john.doe@gmail.com",
            "phone": "9876543210",
            "message": "I am interested in this property",
        }

        serializer = self.validate(data)

        self.assertTrue(serializer.is_valid())

        self.assertEqual(serializer.errors, {})

    # =========================================================
    # COMPLETELY INVALID DATA
    # =========================================================

    def test_completely_invalid_data(self):

        data = {
            "name": "",
            "email": "wrong-email",
            "phone": "123",
            "message": "Hi",
        }

        serializer = self.validate(data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("name", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("phone", serializer.errors)

        # "Hi" should be rejected by your validate() method.
        self.assertIn("message", serializer.errors)

    # =========================================================
    # MULTIPLE INVALID FIELDS
    # =========================================================

    def test_multiple_invalid_fields(self):

        data = {
            "name": "A",
            "email": "invalid",
            "phone": "123",
            "message": "Hi",
        }

        serializer = self.validate(data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("name", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("phone", serializer.errors)

        # "Hi" should fail message validation.
        self.assertIn("message", serializer.errors)





from django.test import TestCase
from django.contrib.auth.hashers import check_password

from users.models import UserCreate
from users.serializers import RegisterSerializer


class RegisterSerializerValidationTests(TestCase):

    def valid_data(self):
        return {
            "name": "John Doe",
            "email": "john@gmail.com",
            "mobile": "9876543210",
            "password": "password123",
            "confirm_password": "password123",
        }

    # ==================================================
    # VALID DATA
    # ==================================================

    def test_valid_registration_data(self):

        serializer = RegisterSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # PASSWORD MATCH
    # ==================================================

    def test_password_mismatch(self):

        data = self.valid_data()

        data["confirm_password"] = "different123"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "confirm_password",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["confirm_password"][0]),
            "Passwords do not match"
        )

    # ==================================================
    # EMPTY PASSWORD
    # ==================================================

    def test_empty_password(self):

        data = self.valid_data()

        data["password"] = ""
        data["confirm_password"] = ""

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "password",
            serializer.errors
        )

    # ==================================================
    # SHORT PASSWORD
    # ==================================================

    def test_password_less_than_six_characters(self):

        data = self.valid_data()

        data["password"] = "12345"
        data["confirm_password"] = "12345"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "password",
            serializer.errors
        )

        self.assertIn(
            "Password must be at least 6 characters long",
            str(serializer.errors["password"][0])
        )

    # ==================================================
    # EXACTLY SIX CHARACTERS
    # ==================================================

    def test_password_exactly_six_characters(self):

        data = self.valid_data()

        # Must contain both letters and numbers
        data["password"] = "abc123"
        data["confirm_password"] = "abc123"

        serializer = RegisterSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMAIL UNIQUENESS
    # ==================================================

    def test_duplicate_email(self):

        UserCreate.objects.create(
            name="Existing User",
            email="existing@gmail.com",
            mobile="9876543210",
            password="hashed123"
        )

        data = self.valid_data()

        data["email"] = "existing@gmail.com"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "email",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["email"][0]),
            "Email already registered"
        )

    # ==================================================
    # CASE-INSENSITIVE EMAIL UNIQUENESS
    # ==================================================

    def test_duplicate_email_case_insensitive(self):

        UserCreate.objects.create(
            name="Existing User",
            email="existing@gmail.com",
            mobile="9876543210",
            password="hashed123"
        )

        data = self.valid_data()

        data["email"] = "EXISTING@GMAIL.COM"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "email",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["email"][0]),
            "Email already registered"
        )

    # ==================================================
    # UNIQUE EMAIL SHOULD PASS
    # ==================================================

    def test_unique_email(self):

        UserCreate.objects.create(
            name="Existing User",
            email="existing@gmail.com",
            mobile="9876543210",
            password="hashed123"
        )

        data = self.valid_data()

        data["email"] = "newuser@gmail.com"

        serializer = RegisterSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # MISSING CONFIRM PASSWORD
    # ==================================================

    def test_missing_confirm_password(self):

        data = self.valid_data()

        del data["confirm_password"]

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "confirm_password",
            serializer.errors
        )

    # ==================================================
    # MISSING PASSWORD
    # ==================================================

    def test_missing_password(self):

        data = self.valid_data()

        del data["password"]

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password",
            serializer.errors
        )

    # ==================================================
    # MISSING EMAIL
    # ==================================================

    def test_missing_email(self):

        data = self.valid_data()

        del data["email"]

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # MISSING NAME
    # ==================================================

    def test_missing_name(self):

        data = self.valid_data()

        del data["name"]

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # ==================================================
    # MISSING MOBILE
    # ==================================================

    def test_missing_mobile(self):

        data = self.valid_data()

        del data["mobile"]

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    # ==================================================
    # CREATE USER
    # ==================================================

    def test_create_user(self):

        data = self.valid_data()

        serializer = RegisterSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertIsNotNone(user)

        self.assertEqual(
            user.email,
            "john@gmail.com"
        )

        self.assertEqual(
            user.name,
            "John Doe"
        )

        self.assertEqual(
            user.mobile,
            "9876543210"
        )

        # confirm_password must not be stored
        self.assertNotIn(
            "confirm_password",
            user.__dict__
        )

    # ==================================================
    # PASSWORD MUST BE HASHED
    # ==================================================

    def test_password_is_hashed(self):

        data = self.valid_data()

        serializer = RegisterSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        # Password should not be stored as plain text
        self.assertNotEqual(
            user.password,
            "password123"
        )

        # Original password must successfully verify
        self.assertTrue(
            check_password(
                "password123",
                user.password
            )
        )

    # ==================================================
    # CONFIRM PASSWORD IS NOT SAVED
    # ==================================================

    def test_confirm_password_not_saved(self):

        data = self.valid_data()

        serializer = RegisterSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertNotIn(
            "confirm_password",
            user.__dict__
        )

    # ==================================================
    # DIFFERENT PASSWORDS SHOULD NOT CREATE USER
    # ==================================================

    def test_mismatched_password_does_not_create_user(self):

        data = self.valid_data()

        data["confirm_password"] = "wrongpassword"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        # No user should be created
        self.assertEqual(
            UserCreate.objects.count(),
            0
        )



from django.test import TestCase

from users.serializers import VerifyOTPSerializer


class VerifyOTPSerializerTests(TestCase):

    # ==================================================
    # VALID DATA
    # ==================================================

    def valid_data(self):
        return {
            "email": "john@gmail.com",
            "otp": "123456",
        }

    # ==================================================
    # VALID OTP
    # ==================================================

    def test_valid_otp(self):

        serializer = VerifyOTPSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # OTP MUST CONTAIN ONLY NUMBERS
    # ==================================================

    def test_otp_with_letters(self):

        data = self.valid_data()

        data["otp"] = "12345A"

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["otp"][0]),
            "OTP must contain only numbers."
        )

    # ==================================================
    # OTP WITH SPECIAL CHARACTERS
    # ==================================================

    def test_otp_with_special_characters(self):

        data = self.valid_data()

        data["otp"] = "123@56"

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["otp"][0]),
            "OTP must contain only numbers."
        )

    # ==================================================
    # OTP WITH SPACES
    # ==================================================

    def test_otp_with_spaces(self):

        data = self.valid_data()

        data["otp"] = "123 56"

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["otp"][0]),
            "OTP must contain only numbers."
        )

    # ==================================================
    # OTP LONGER THAN 6 CHARACTERS
    # ==================================================

    def test_otp_longer_than_six_characters(self):

        data = self.valid_data()

        data["otp"] = "1234567"

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

    # ==================================================
    # OTP SHORTER THAN 6 CHARACTERS
    # ==================================================

    def test_otp_shorter_than_six_characters(self):

        data = self.valid_data()

        data["otp"] = "12345"

        serializer = VerifyOTPSerializer(data=data)

        # This should be valid because the serializer
        # only specifies max_length=6, not min_length=6.
        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # OTP WITH ONLY ONE DIGIT
    # ==================================================

    def test_single_digit_otp(self):

        data = self.valid_data()

        data["otp"] = "1"

        serializer = VerifyOTPSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # OTP WITH LEADING ZEROS
    # ==================================================

    def test_otp_with_leading_zeros(self):

        data = self.valid_data()

        data["otp"] = "001234"

        serializer = VerifyOTPSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMPTY OTP
    # ==================================================

    def test_empty_otp(self):

        data = self.valid_data()

        data["otp"] = ""

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

    # ==================================================
    # MISSING OTP
    # ==================================================

    def test_missing_otp(self):

        data = self.valid_data()

        del data["otp"]

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "otp",
            serializer.errors
        )

    # ==================================================
    # MISSING EMAIL
    # ==================================================

    def test_missing_email(self):

        data = self.valid_data()

        del data["email"]

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # INVALID EMAIL
    # ==================================================

    def test_invalid_email(self):

        data = self.valid_data()

        data["email"] = "invalid-email"

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMPTY EMAIL
    # ==================================================

    def test_empty_email(self):

        data = self.valid_data()

        data["email"] = ""

        serializer = VerifyOTPSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # VERIFY VALIDATED DATA
    # ==================================================

    def test_validated_data(self):

        data = self.valid_data()

        serializer = VerifyOTPSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "john@gmail.com"
        )

        self.assertEqual(
            serializer.validated_data["otp"],
            "123456"
        )


from django.test import TestCase

from users.serializers import ForgotPasswordSerializer


class ForgotPasswordSerializerTests(TestCase):

    # ==================================================
    # VALID DATA
    # ==================================================

    def valid_data(self):
        return {
            "email": "john@gmail.com"
        }

    # ==================================================
    # VALID EMAIL
    # ==================================================

    def test_valid_email(self):

        serializer = ForgotPasswordSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # VALIDATED EMAIL
    # ==================================================

    def test_validated_email(self):

        serializer = ForgotPasswordSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "john@gmail.com"
        )

    # ==================================================
    # EMAIL IS NORMALIZED TO LOWERCASE
    # ==================================================

    def test_email_converted_to_lowercase(self):

        data = {
            "email": "JOHN@GMAIL.COM"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "john@gmail.com"
        )

    # ==================================================
    # EMAIL WITH SPACES
    # ==================================================

    def test_email_with_leading_and_trailing_spaces(self):

        data = {
            "email": "  john@gmail.com  "
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "john@gmail.com"
        )

    # ==================================================
    # INVALID EMAIL
    # ==================================================

    def test_invalid_email(self):

        data = {
            "email": "invalid-email"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMAIL WITHOUT @
    # ==================================================

    def test_email_without_at_symbol(self):

        data = {
            "email": "johngmail.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMAIL WITHOUT DOMAIN
    # ==================================================

    def test_email_without_domain(self):

        data = {
            "email": "john@"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMAIL WITHOUT USERNAME
    # ==================================================

    def test_email_without_username(self):

        data = {
            "email": "@gmail.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMPTY EMAIL
    # ==================================================

    def test_empty_email(self):

        data = {
            "email": ""
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # MISSING EMAIL
    # ==================================================

    def test_missing_email(self):

        serializer = ForgotPasswordSerializer(
            data={}
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # NULL EMAIL
    # ==================================================

    def test_null_email(self):

        data = {
            "email": None
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH ONLY SPACES
    # ==================================================

    def test_email_with_only_spaces(self):

        data = {
            "email": "     "
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH NUMERIC DOMAIN
    # ==================================================

    def test_email_with_numeric_domain(self):

        data = {
            "email": "john@123.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH SUBDOMAIN
    # ==================================================

    def test_email_with_subdomain(self):

        data = {
            "email": "john@mail.example.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH PLUS
    # ==================================================

    def test_email_with_plus(self):

        data = {
            "email": "john+test@gmail.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH DOT
    # ==================================================

    def test_email_with_dot(self):

        data = {
            "email": "john.doe@gmail.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # ==================================================
    # EMAIL WITH NUMBER
    # ==================================================

    def test_email_with_number(self):

        data = {
            "email": "john123@gmail.com"
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


from rest_framework.test import APITestCase

from users.serializers import ForgotPasswordSerializer


class ForgotPasswordSerializerTest(APITestCase):

    def test_valid_email(self):

        data = {
            "email": "  TEST@EXAMPLE.COM  "
        }

        serializer = ForgotPasswordSerializer(
            data=data
        )

        print("\nIS VALID:")
        print(serializer.is_valid())

        print("\nVALIDATED DATA:")
        print(serializer.validated_data)

        print("\nERRORS:")
        print(serializer.errors)

        self.assertTrue(
            serializer.is_valid()
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "test@example.com"
        )


from django.test import TestCase

from users.serializers import VerifyForgotOTPSerializer


class VerifyForgotOTPSerializerTest(TestCase):

    # =====================================================
    # 1. VALID EMAIL + VALID OTP
    # =====================================================

    def test_valid_email_and_otp(self):

        data = {
            "email": "test@example.com",
            "otp": "123456"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid()
        )

        print("\n==============================")
        print("VALID EMAIL + OTP")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Validated:", serializer.validated_data)
        print("Errors:", serializer.errors)

    # =====================================================
    # 2. INVALID EMAIL
    # =====================================================

    def test_invalid_email(self):

        data = {
            "email": "invalid-email",
            "otp": "123456"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("INVALID EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 3. MISSING EMAIL
    # =====================================================

    def test_missing_email(self):

        data = {
            "otp": "123456"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("MISSING EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 4. MISSING OTP
    # =====================================================

    def test_missing_otp(self):

        data = {
            "email": "test@example.com"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("MISSING OTP")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 5. OTP WITH LETTERS
    # =====================================================

    def test_otp_with_letters(self):

        data = {
            "email": "test@example.com",
            "otp": "12AB56"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("OTP WITH LETTERS")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 6. OTP MORE THAN 6 DIGITS
    # =====================================================

    def test_otp_more_than_6_digits(self):

        data = {
            "email": "test@example.com",
            "otp": "1234567"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("OTP MORE THAN 6 DIGITS")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 7. EMPTY OTP
    # =====================================================

    def test_empty_otp(self):

        data = {
            "email": "test@example.com",
            "otp": ""
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("EMPTY OTP")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 8. EMPTY EMAIL
    # =====================================================

    def test_empty_email(self):

        data = {
            "email": "",
            "otp": "123456"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("EMPTY EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 9. OTP WITH SPECIAL CHARACTERS
    # =====================================================

    def test_otp_with_special_characters(self):

        data = {
            "email": "test@example.com",
            "otp": "123@56"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("OTP WITH SPECIAL CHARACTERS")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =====================================================
    # 10. OTP WITH SPACES
    # =====================================================

    def test_otp_with_spaces(self):

        data = {
            "email": "test@example.com",
            "otp": "123 56"
        }

        serializer = VerifyForgotOTPSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("OTP WITH SPACES")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

from rest_framework.test import APIClient


class ChangePasswordAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/agent/change_password/"

    def test_change_password(self):

        data = {
            "current_password": "oldpass123",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )

        print("\n==============================")
        print("CHANGE PASSWORD API")
        print("==============================")
        print("POST URL:", self.url)
        print("Input:", data)
        print("Status Code:", response.status_code)

        if hasattr(response, "data"):
            print("Response:", response.data)
        else:
            print("Response:", response.content.decode())

        self.assertEqual(response.status_code, 401)


from django.test import TestCase
from users.serializers import UserLoginSerializer


class UserLoginSerializerTest(TestCase):

    def test_valid_login_input(self):

        data = {
            "email": "test@example.com",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        print("\n==============================")
        print("VALID LOGIN INPUT")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Validated Data:", serializer.validated_data)
        print("Errors:", serializer.errors)

    def test_invalid_email(self):

        data = {
            "email": "invalid-email",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("INVALID EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_missing_email(self):

        data = {
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("MISSING EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_empty_email(self):

        data = {
            "email": "",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("EMPTY EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_missing_password(self):

        data = {
            "email": "test@example.com"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("MISSING PASSWORD")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_empty_password(self):

        data = {
            "email": "test@example.com",
            "password": ""
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("EMPTY PASSWORD")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_password_only_spaces(self):

        data = {
            "email": "test@example.com",
            "password": "      "
        }

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("PASSWORD ONLY SPACES")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    def test_uppercase_email(self):

        data = {
            "email": "TEST@EXAMPLE.COM",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        print("\n==============================")
        print("UPPERCASE EMAIL")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Validated Data:", serializer.validated_data)
        print("Errors:", serializer.errors)

    def test_email_with_spaces(self):

        data = {
            "email": "  test@example.com  ",
            "password": "password123"
        }

        serializer = UserLoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        print("\n==============================")
        print("EMAIL WITH SPACES")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Validated Data:", serializer.validated_data)
        print("Errors:", serializer.errors)

    def test_both_fields_missing(self):

        data = {}

        serializer = UserLoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        print("\n==============================")
        print("BOTH FIELDS MISSING")
        print("==============================")
        print("Input:", data)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)


from django.test import TestCase

from users.serializers import UserProfileSerializer


class UserProfileSerializerValidationTest(TestCase):

    # =========================================================
    # FULL NAME - VALID INPUT
    # =========================================================

    def test_full_name_valid(self):

        values = [
            "John",
            "John Smith",
            "Test User",
            "A",
            "John Kumar"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "full_name": value
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

            print("\n==============================")
            print("FULL NAME - VALID")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # FULL NAME - EMPTY
    # =========================================================

    def test_full_name_empty(self):

        value = ""

        serializer = UserProfileSerializer(
            data={
                "full_name": value
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("FULL NAME - EMPTY")
        print("==============================")
        print("Input:", value)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # FULL NAME - ONLY SPACES
    # =========================================================

    def test_full_name_only_spaces(self):

        value = "     "

        serializer = UserProfileSerializer(
            data={
                "full_name": value
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("FULL NAME - ONLY SPACES")
        print("==============================")
        print("Input:", repr(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # FULL NAME - MORE THAN 150 CHARACTERS
    # =========================================================

    def test_full_name_more_than_150(self):

        value = "A" * 151

        serializer = UserProfileSerializer(
            data={
                "full_name": value
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("FULL NAME - MORE THAN 150")
        print("==============================")
        print("Input Length:", len(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # FULL NAME - EXACTLY 150 CHARACTERS
    # =========================================================

    def test_full_name_exactly_150(self):

        value = "A" * 150

        serializer = UserProfileSerializer(
            data={
                "full_name": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("FULL NAME - EXACTLY 150")
        print("==============================")
        print("Input Length:", len(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # FULL NAME - SPACES AROUND VALUE
    # =========================================================

    def test_full_name_spaces_around(self):

        value = "   John Smith   "

        serializer = UserProfileSerializer(
            data={
                "full_name": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["full_name"],
            "John Smith"
        )

        print("\n==============================")
        print("FULL NAME - SPACES AROUND")
        print("==============================")
        print("Input:", repr(value))
        print("Validated:", serializer.validated_data)
        print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - VALID INPUT
    # =========================================================

    def test_mobile_valid(self):

        values = [
            "9876543210",
            "9876543211",
            "9000000000",
            "9999999999"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "mobile": value
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

            print("\n==============================")
            print("MOBILE - VALID")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - LESS THAN 10 DIGITS
    # =========================================================

    def test_mobile_less_than_10_digits(self):

        values = [
            "1",
            "12",
            "12345",
            "123456789"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("MOBILE - LESS THAN 10")
            print("==============================")
            print("Input:", value)
            print("Length:", len(value))
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - MORE THAN 10 DIGITS
    # =========================================================

    def test_mobile_more_than_10_digits(self):

        values = [
            "12345678901",
            "123456789012",
            "99999999999"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("MOBILE - MORE THAN 10")
            print("==============================")
            print("Input:", value)
            print("Length:", len(value))
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - LETTERS
    # =========================================================

    def test_mobile_letters(self):

        values = [
            "98765abc10",
            "abcdefghij",
            "98765A3210"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("MOBILE - LETTERS")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - SPECIAL CHARACTERS
    # =========================================================

    def test_mobile_special_characters(self):

        values = [
            "98765@3210",
            "98765-3210",
            "98765.3210",
            "+919876543210"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("MOBILE - SPECIAL CHARACTERS")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # MOBILE - EMPTY
    # =========================================================

    def test_mobile_empty(self):

        value = ""

        serializer = UserProfileSerializer(
            data={
                "mobile": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("MOBILE - EMPTY")
        print("==============================")
        print("Input:", repr(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - VALID
    # =========================================================

    def test_alternate_mobile_valid(self):

        values = [
            "9876543210",
            "9876543211",
            "9000000000",
            "9999999999"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "alternate_mobile": value
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

            print("\n==============================")
            print("ALTERNATE MOBILE - VALID")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - LESS THAN 10
    # =========================================================

    def test_alternate_mobile_less_than_10(self):

        values = [
            "1",
            "12345",
            "123456789"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "alternate_mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("ALTERNATE MOBILE - LESS THAN 10")
            print("==============================")
            print("Input:", value)
            print("Length:", len(value))
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - MORE THAN 10
    # =========================================================

    def test_alternate_mobile_more_than_10(self):

        values = [
            "12345678901",
            "123456789012",
            "99999999999"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "alternate_mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("ALTERNATE MOBILE - MORE THAN 10")
            print("==============================")
            print("Input:", value)
            print("Length:", len(value))
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - LETTERS
    # =========================================================

    def test_alternate_mobile_letters(self):

        values = [
            "98765abc10",
            "abcdefghij",
            "98765A3210"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "alternate_mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("ALTERNATE MOBILE - LETTERS")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - SPECIAL CHARACTERS
    # =========================================================

    def test_alternate_mobile_special_characters(self):

        values = [
            "98765@3210",
            "98765-3210",
            "98765.3210",
            "+919876543210"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "alternate_mobile": value
                },
                partial=True
            )

            self.assertFalse(
                serializer.is_valid()
            )

            print("\n==============================")
            print("ALTERNATE MOBILE - SPECIAL")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # ALTERNATE MOBILE - EMPTY
    # =========================================================

    def test_alternate_mobile_empty(self):

        value = ""

        serializer = UserProfileSerializer(
            data={
                "alternate_mobile": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("ALTERNATE MOBILE - EMPTY")
        print("==============================")
        print("Input:", repr(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # CITY - VALID
    # =========================================================

    def test_city_valid(self):

        values = [
            "Coimbatore",
            "Chennai",
            "Bangalore",
            "Mumbai",
            "New Delhi"
        ]

        for value in values:

            serializer = UserProfileSerializer(
                data={
                    "city": value
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

            print("\n==============================")
            print("CITY - VALID")
            print("==============================")
            print("Input:", value)
            print("Valid:", serializer.is_valid())
            print("Errors:", serializer.errors)

    # =========================================================
    # CITY - SPACES
    # =========================================================

    def test_city_spaces(self):

        value = "   Coimbatore   "

        serializer = UserProfileSerializer(
            data={
                "city": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["city"],
            "Coimbatore"
        )

        print("\n==============================")
        print("CITY - SPACES")
        print("==============================")
        print("Input:", repr(value))
        print("Validated:", serializer.validated_data)
        print("Errors:", serializer.errors)

    # =========================================================
    # CITY - EMPTY
    # =========================================================

    def test_city_empty(self):

        value = ""

        serializer = UserProfileSerializer(
            data={
                "city": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("CITY - EMPTY")
        print("==============================")
        print("Input:", repr(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # CITY - NULL
    # =========================================================

    def test_city_null(self):

        value = None

        serializer = UserProfileSerializer(
            data={
                "city": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("CITY - NULL")
        print("==============================")
        print("Input:", value)
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # CITY - MORE THAN 100 CHARACTERS
    # =========================================================

    def test_city_more_than_100(self):

        value = "A" * 101

        serializer = UserProfileSerializer(
            data={
                "city": value
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        print("\n==============================")
        print("CITY - MORE THAN 100")
        print("==============================")
        print("Input Length:", len(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # CITY - EXACTLY 100 CHARACTERS
    # =========================================================

    def test_city_exactly_100(self):

        value = "A" * 100

        serializer = UserProfileSerializer(
            data={
                "city": value
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("CITY - EXACTLY 100")
        print("==============================")
        print("Input Length:", len(value))
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

    # =========================================================
    # EMPTY INPUT
    # =========================================================

    def test_empty_input(self):

        serializer = UserProfileSerializer(
            data={},
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        print("\n==============================")
        print("EMPTY INPUT")
        print("==============================")
        print("Input:", {})
        print("Valid:", serializer.is_valid())
        print("Errors:", serializer.errors)

from django.test import TestCase
from users.serializers import InboxSerializer


class InboxSerializerValidationTest(TestCase):

    # =========================================================
    # NAME VALIDATION
    # =========================================================

    def test_name_valid(self):
        valid_names = [
            "John",
            "John Smith",
            "ABC",
            "Test User",
            "A" * 50,
        ]

        for name in valid_names:
            serializer = InboxSerializer(
                data={
                    "name": name,
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

    def test_name_empty(self):
        serializer = InboxSerializer(
            data={
                "name": "",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_spaces_only(self):
        serializer = InboxSerializer(
            data={
                "name": "     ",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_trim_spaces(self):
        serializer = InboxSerializer(
            data={
                "name": "  John Smith  ",
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "John Smith"
        )

    def test_name_exactly_50_characters(self):
        serializer = InboxSerializer(
            data={
                "name": "A" * 50,
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_name_more_than_50_characters(self):
        serializer = InboxSerializer(
            data={
                "name": "A" * 51,
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


    # =========================================================
    # PIN CODE VALIDATION
    # =========================================================

    def test_pin_code_valid(self):
        valid_pin_codes = [
            "641001",
            "600001",
            "110001",
            "400001",
            "123456",
        ]

        for pin_code in valid_pin_codes:
            serializer = InboxSerializer(
                data={
                    "pin_code": pin_code,
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

    def test_pin_code_empty(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_spaces_only(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "     ",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_less_than_6_digits(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "64100",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_more_than_6_digits(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "6410012",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_contains_letters(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "6410AB",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_contains_special_characters(self):
        serializer = InboxSerializer(
            data={
                "pin_code": "641-01",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("pin_code", serializer.errors)

    def test_pin_code_trim_spaces(self):
        serializer = InboxSerializer(
            data={
                "pin_code": " 641001 ",
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["pin_code"],
            "641001"
        )


    # =========================================================
    # CONTACT VALIDATION
    # =========================================================

    def test_contact_valid(self):
        valid_contacts = [
            "9876543210",
            "9123456789",
            "9000000000",
            "1234567890",
        ]

        for contact in valid_contacts:
            serializer = InboxSerializer(
                data={
                    "contact": contact,
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

    def test_contact_empty(self):
        serializer = InboxSerializer(
            data={
                "contact": "",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_spaces_only(self):
        serializer = InboxSerializer(
            data={
                "contact": "     ",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_less_than_10_digits(self):
        serializer = InboxSerializer(
            data={
                "contact": "987654321",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_more_than_10_digits(self):
        serializer = InboxSerializer(
            data={
                "contact": "98765432101",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_contains_letters(self):
        serializer = InboxSerializer(
            data={
                "contact": "98765ABCDE",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_contains_special_characters(self):
        serializer = InboxSerializer(
            data={
                "contact": "98765-3210",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact", serializer.errors)

    def test_contact_trim_spaces(self):
        serializer = InboxSerializer(
            data={
                "contact": " 9876543210 ",
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["contact"],
            "9876543210"
        )


    # =========================================================
    # MESSAGE VALIDATION
    # =========================================================

    def test_messages_text_valid(self):
        valid_messages = [
            "Hello",
            "I am interested in this property.",
            "Please contact me.",
            "Need more information about the property.",
            "A" * 10000,
        ]

        for message in valid_messages:
            serializer = InboxSerializer(
                data={
                    "messages_text": message,
                },
                partial=True
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

    def test_messages_text_empty(self):
        serializer = InboxSerializer(
            data={
                "messages_text": "",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "messages_text",
            serializer.errors
        )

    def test_messages_text_spaces_only(self):
        serializer = InboxSerializer(
            data={
                "messages_text": "     ",
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "messages_text",
            serializer.errors
        )

    def test_messages_text_trim_spaces(self):
        serializer = InboxSerializer(
            data={
                "messages_text": "  Hello World  ",
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["messages_text"],
            "Hello World"
        )

    def test_messages_text_more_than_10000_characters(self):
        serializer = InboxSerializer(
            data={
                "messages_text": "A" * 10001,
            },
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "messages_text",
            serializer.errors
        )


    # =========================================================
    # OPTIONAL FIELD / PARTIAL VALIDATION
    # =========================================================

    def test_empty_input_with_partial_true(self):
        serializer = InboxSerializer(
            data={},
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


from django.test import TestCase
from unittest.mock import Mock
from users.serializers import AgentReviewSerializer


class AgentReviewSerializerTest(TestCase):

    # =========================================================
    # RATING VALIDATION
    # =========================================================

    def test_rating_zero(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 0,
                "review": "Good agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_one(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 1,
                "review": "Good agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_two_point_five(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 2.5,
                "review": "Average experience"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_four(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 4,
                "review": "Very good agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_five(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "Excellent agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_negative(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": -1,
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_greater_than_five(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5.1,
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_six(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 6,
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_ten(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 10,
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_string_number(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": "4",
                "review": "Good agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_string_decimal(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": "4.5",
                "review": "Good agent"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_rating_invalid_text(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": "abc",
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_special_characters(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": "@#$",
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_empty(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": "",
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_rating_null(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": None,
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )


    # =========================================================
    # REVIEW VALIDATION
    # =========================================================

    def test_review_valid(self):

        valid_reviews = [
            "Good agent",
            "Very helpful agent",
            "Excellent service",
            "Average experience",
            "The agent was very professional.",
            "A",
        ]

        for review in valid_reviews:

            serializer = AgentReviewSerializer(
                data={
                    "rating": 5,
                    "review": review
                }
            )

            self.assertTrue(
                serializer.is_valid(),
                serializer.errors
            )

    def test_review_empty(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": ""
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "review",
            serializer.errors
        )

    def test_review_spaces_only(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "     "
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "review",
            serializer.errors
        )

    def test_review_tabs_and_spaces_only(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "\t   "
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "review",
            serializer.errors
        )

    def test_review_trim_spaces(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "  Very good agent  "
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["review"],
            "Very good agent"
        )

    def test_review_single_character(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "A"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_review_numbers(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "123456"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_review_special_characters(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "@#$%^&*!"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_review_unicode(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "Very good service 👍"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_review_multiline(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5,
                "review": "Very good agent.\nHelpful and professional."
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


    # =========================================================
    # REQUIRED FIELD TESTS
    # =========================================================

    def test_rating_missing(self):

        serializer = AgentReviewSerializer(
            data={
                "review": "Good agent"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

    def test_review_missing(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 5
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "review",
            serializer.errors
        )

    def test_rating_and_review_missing(self):

        serializer = AgentReviewSerializer(
            data={}
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "rating",
            serializer.errors
        )

        self.assertIn(
            "review",
            serializer.errors
        )


    # =========================================================
    # COMPLETE VALID INPUT
    # =========================================================

    def test_complete_valid_data(self):

        serializer = AgentReviewSerializer(
            data={
                "rating": 4.5,
                "review": "Very good agent and excellent service."
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["rating"],
            4.5
        )

        self.assertEqual(
            serializer.validated_data["review"],
            "Very good agent and excellent service."
        )


    # =========================================================
    # READ-ONLY / METHOD FIELD TESTS
    # =========================================================

    def test_method_fields_are_present(self):

        serializer = AgentReviewSerializer()

        self.assertIn(
            "user_name",
            serializer.fields
        )

        self.assertIn(
            "user_image",
            serializer.fields
        )

        self.assertIn(
            "total_likes",
            serializer.fields
        )

        self.assertIn(
            "created_at",
            serializer.fields
        )

        self.assertIn(
            "is_owner",
            serializer.fields
        )


    # =========================================================
    # GET USER NAME
    # =========================================================

    def test_get_user_name_with_user(self):

        serializer = AgentReviewSerializer()

        user = Mock()
        user.name = "John"

        obj = Mock()
        obj.user = user

        result = serializer.get_user_name(obj)

        self.assertEqual(
            result,
            "John"
        )

    def test_get_user_name_without_user(self):

        serializer = AgentReviewSerializer()

        obj = Mock()
        obj.user = None

        result = serializer.get_user_name(obj)

        self.assertEqual(
            result,
            "Anonymous"
        )


    # =========================================================
    # GET USER IMAGE
    # =========================================================

    def test_get_user_image_without_user(self):

        serializer = AgentReviewSerializer()

        obj = Mock()
        obj.user = None

        result = serializer.get_user_image(obj)

        self.assertIn(
            "ui-avatars.com/api/",
            result
        )

        self.assertIn(
            "Anonymous",
            result
        )


    # =========================================================
    # GET TOTAL LIKES
    # =========================================================

    def test_get_total_likes(self):

        serializer = AgentReviewSerializer()

        likes = Mock()

        likes.count.return_value = 5

        obj = Mock()
        obj.likes = likes

        result = serializer.get_total_likes(obj)

        self.assertEqual(
            result,
            5
        )

    def test_get_total_likes_zero(self):

        serializer = AgentReviewSerializer()

        likes = Mock()

        likes.count.return_value = 0

        obj = Mock()
        obj.likes = likes

        result = serializer.get_total_likes(obj)

        self.assertEqual(
            result,
            0
        )


    # =========================================================
    # GET CREATED AT
    # =========================================================

    def test_get_created_at(self):

        serializer = AgentReviewSerializer()

        from datetime import datetime

        obj = Mock()

        obj.created_at = datetime(
            2026,
            9,
            16
        )

        result = serializer.get_created_at(obj)

        self.assertEqual(
            result,
            "16-09-2026"
        )


    # =========================================================
    # GET IS OWNER - NO REQUEST
    # =========================================================

    def test_get_is_owner_without_request(self):

        serializer = AgentReviewSerializer(
            context={}
        )

        obj = Mock()

        result = serializer.get_is_owner(obj)

        self.assertFalse(
            result
        )


    # =========================================================
    # GET IS OWNER - UNAUTHENTICATED USER
    # =========================================================

    def test_get_is_owner_unauthenticated(self):

        request = Mock()

        request.user = Mock()
        request.user.is_authenticated = False

        serializer = AgentReviewSerializer(
            context={
                "request": request
            }
        )

        obj = Mock()

        result = serializer.get_is_owner(obj)

        self.assertFalse(
            result
        )


    # =========================================================
    # GET IS OWNER - AUTHENTICATED OWNER
    # =========================================================

    def test_get_is_owner_authenticated_owner(self):

        request = Mock()

        request.user = Mock()
        request.user.is_authenticated = True
        request.user.id = "user-123"

        serializer = AgentReviewSerializer(
            context={
                "request": request
            }
        )

        obj = Mock()

        obj.user_id = "user-123"

        result = serializer.get_is_owner(obj)

        self.assertTrue(
            result
        )


    # =========================================================
    # GET IS OWNER - AUTHENTICATED DIFFERENT USER
    # =========================================================

    def test_get_is_owner_different_user(self):

        request = Mock()

        request.user = Mock()
        request.user.is_authenticated = True
        request.user.id = "user-123"

        serializer = AgentReviewSerializer(
            context={
                "request": request
            }
        )

        obj = Mock()

        obj.user_id = "user-456"

        result = serializer.get_is_owner(obj)

        self.assertFalse(
            result
        )

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from agents.models import AgentUserProfile
from users.serializers import AgentLoginSerializer
from users.views import AgentLoginAPIView


class AgentLoginSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.email = "agent@test.com"
        cls.password = "TestPassword123"

        cls.agent = AgentUserProfile(
            username="testagent",
            email=cls.email,
            phone_number="9876543210",
            address="Test Address",
            pin_code="641001",
            city="Coimbatore",
            agent_type="basic",
            agent_code="AGT001",
        )

        cls.agent.set_password(cls.password)

        cls.agent.save()

    # =========================================================
    # VALID LOGIN
    # =========================================================

    def test_valid_login(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email,
                "password": self.password,
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertIn(
            "user",
            serializer.validated_data
        )

        self.assertEqual(
            serializer.validated_data["user"].id,
            self.agent.id
        )

    # =========================================================
    # INVALID EMAIL
    # =========================================================

    def test_invalid_email(self):

        serializer = AgentLoginSerializer(
            data={
                "email": "wrong@test.com",
                "password": self.password,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "error",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["error"][0]),
            "Invalid email"
        )

    # =========================================================
    # INVALID PASSWORD
    # =========================================================

    def test_invalid_password(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email,
                "password": "WrongPassword123",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "error",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["error"][0]),
            "Invalid password"
        )

    # =========================================================
    # MISSING EMAIL
    # =========================================================

    def test_missing_email(self):

        serializer = AgentLoginSerializer(
            data={
                "password": self.password,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # MISSING PASSWORD
    # =========================================================

    def test_missing_password(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password",
            serializer.errors
        )

    # =========================================================
    # BOTH FIELDS MISSING
    # =========================================================

    def test_missing_email_and_password(self):

        serializer = AgentLoginSerializer(
            data={}
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

        self.assertIn(
            "password",
            serializer.errors
        )

    # =========================================================
    # EMPTY EMAIL
    # =========================================================

    def test_empty_email(self):

        serializer = AgentLoginSerializer(
            data={
                "email": "",
                "password": self.password,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # INVALID EMAIL FORMAT
    # =========================================================

    def test_invalid_email_format(self):

        serializer = AgentLoginSerializer(
            data={
                "email": "agent",
                "password": self.password,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # EMPTY PASSWORD
    # =========================================================

    def test_empty_password(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email,
                "password": "",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password",
            serializer.errors
        )

    # =========================================================
    # PASSWORD IS WRITE ONLY
    # =========================================================

    def test_password_is_write_only(self):

        serializer = AgentLoginSerializer()

        self.assertTrue(
            serializer.fields["password"].write_only
        )

    # =========================================================
    # USER ADDED TO VALIDATED DATA
    # =========================================================

    def test_user_added_to_validated_data(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email,
                "password": self.password,
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.validated_data["user"]

        self.assertEqual(
            user.id,
            self.agent.id
        )

    # =========================================================
    # EMAIL CASE SENSITIVITY
    # =========================================================

    def test_email_uppercase(self):

        serializer = AgentLoginSerializer(
            data={
                "email": self.email.upper(),
                "password": self.password,
            }
        )

        # The serializer does not normalize email.
        # AgentUserProfile.objects.get(email=email)
        # therefore uses the exact value.
        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "error",
            serializer.errors
        )

    # =========================================================
    # EMAIL WITH SPACES
    # =========================================================

    def test_email_with_spaces(self):
        serializer = AgentLoginSerializer(data={
            "email": f" {self.email} ",
            "password": self.password
        })

        self.assertFalse(serializer.is_valid())

        self.assertIn("email", serializer.errors)

        self.assertIn(
            "Email cannot contain leading or trailing spaces.",
            str(serializer.errors["email"])
        )


class AgentLoginAPIViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.email = "agentapi@test.com"
        cls.password = "TestPassword123"

        cls.agent = AgentUserProfile(
            username="apiagent",
            email=cls.email,
            phone_number="9876543210",
            address="Test Address",
            pin_code="641001",
            city="Coimbatore",
            agent_type="basic",
            agent_code="AGT002",
        )

        cls.agent.set_password(cls.password)
        cls.agent.save()

    # =========================================================
    # SUCCESSFUL API LOGIN
    # =========================================================

    def test_login_api_success(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": self.email,
                "password": self.password,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.data["message"],
            "Agent login successful"
        )

        self.assertIn(
            "access",
            response.data
        )

        self.assertIn(
            "refresh",
            response.data
        )

        self.assertIn(
            "agent_details",
            response.data
        )

        self.assertEqual(
            response.data["login_as"],
            "agent"
        )

    # =========================================================
    # AGENT DETAILS
    # =========================================================

    def test_login_api_agent_details(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": self.email,
                "password": self.password,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            200
        )

        details = response.data["agent_details"]

        self.assertEqual(
            details["agent_id"],
            self.agent.agent_code
        )

        self.assertEqual(
            details["username"],
            self.agent.username
        )

        self.assertEqual(
            details["email"],
            self.agent.email
        )

        self.assertEqual(
            details["phone_number"],
            self.agent.phone_number
        )

        self.assertEqual(
            details["agent_type"],
            self.agent.agent_type
        )

    # =========================================================
    # INVALID EMAIL API
    # =========================================================

    def test_login_api_invalid_email(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": "wrong@test.com",
                "password": self.password,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "error",
            response.data
        )

        self.assertEqual(
            str(response.data["error"][0]),
            "Invalid email"
        )

    # =========================================================
    # INVALID PASSWORD API
    # =========================================================

    def test_login_api_invalid_password(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": self.email,
                "password": "WrongPassword123",
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "error",
            response.data
        )

        self.assertEqual(
            str(response.data["error"][0]),
            "Invalid password"
        )

    # =========================================================
    # MISSING EMAIL API
    # =========================================================

    def test_login_api_missing_email(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "password": self.password,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "email",
            response.data
        )

    # =========================================================
    # MISSING PASSWORD API
    # =========================================================

    def test_login_api_missing_password(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": self.email,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "password",
            response.data
        )

    # =========================================================
    # INVALID EMAIL FORMAT API
    # =========================================================

    def test_login_api_invalid_email_format(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": "invalid-email",
                "password": self.password,
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "email",
            response.data
        )

    # =========================================================
    # EMPTY PASSWORD API
    # =========================================================

    def test_login_api_empty_password(self):

        factory = APIRequestFactory()

        request = factory.post(
            "/agent/login/",
            {
                "email": self.email,
                "password": "",
            },
            format="json"
        )

        response = AgentLoginAPIView.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertIn(
            "password",
            response.data
        )


from django.test import TestCase

from users.serializers import PendingAgentRegistrationSerializer

from agents.models import (
    PendingAgentRegistration,
    AgentUserProfile,
)

from developer.models import (
    AgentPlan,
    PremiumPlan,
    ElitePlan,
)


class PendingAgentRegistrationSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # =====================================================
        # CREATE TEST PLANS
        # =====================================================

        cls.basic_plan = AgentPlan.objects.create(
            name="Test Basic Plan",
            validity=90,
            price=1000,
        )

        cls.premium_plan = PremiumPlan.objects.create(
            name="Test Premium Plan",
            validity=90,
            price=2000,
            total_listing=50,
        )

        cls.elite_plan = ElitePlan.objects.create(
            name="Test Elite Plan",
            plan_validity_days=90,
            price=3000,
            total_property_listings=100,
        )

        # =====================================================
        # IMPORTANT:
        # DRF expects UUID PRIMARY KEYS for FK fields
        # =====================================================

        cls.basic_plan_id = str(cls.basic_plan.pk)
        cls.premium_plan_id = str(cls.premium_plan.pk)
        cls.elite_plan_id = str(cls.elite_plan.pk)

        # =====================================================
        # VALID BASIC REGISTRATION DATA
        # =====================================================

        cls.valid_data = {
            "full_name": "John Agent",
            "email": "johnagent@example.com",
            "phone_number": "9876543210",
            "password": "Strong@123",
            "city": "Coimbatore",
            "pin_code": "641001",
            "address": "123 Test Street",
            "agent_type": "basic",

            # IMPORTANT:
            # Use UUID strings, NOT model objects
            "basic_plan": cls.basic_plan_id,
            "premium_plan": None,
            "elite_plan": None,

            "years_of_experience": 5,
            "deals_closed": 10,
        }

    # =========================================================
    # HELPER
    # =========================================================

    def get_valid_data(self, **overrides):

        data = self.valid_data.copy()
        data.update(overrides)

        return data

    # =========================================================
    # VALID REGISTRATION
    # =========================================================

    def test_valid_basic_registration(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # FULL NAME
    # =========================================================

    def test_full_name_is_trimmed(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                full_name="  John Agent  "
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["full_name"],
            "John Agent"
        )

    def test_full_name_empty(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                full_name=""
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "full_name",
            serializer.errors
        )

    def test_full_name_too_short(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                full_name="A"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "full_name",
            serializer.errors
        )

    def test_full_name_too_long(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                full_name="A" * 151
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "full_name",
            serializer.errors
        )

    # =========================================================
    # EMAIL
    # =========================================================

    def test_email_is_lowercase(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                email="JOHNAGENT@EXAMPLE.COM"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "johnagent@example.com"
        )

    def test_email_is_trimmed(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                email="  johnagent@example.com  "
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "johnagent@example.com"
        )

    def test_duplicate_pending_email(self):

        PendingAgentRegistration.objects.create(
            full_name="Existing Agent",
            email="johnagent@example.com",
            phone_number="9876543211",
            password="Strong@123",
            city="Coimbatore",
            pin_code="641001",
            address="Existing Address",
            agent_type="basic",
            basic_plan=self.basic_plan,
            years_of_experience=5,
            deals_closed=10,
            status="pending",
        )

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data()
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

        self.assertIn(
            "already exists",
            str(serializer.errors["email"])
        )

    def test_existing_agent_email(self):

        agent = AgentUserProfile(
            username="existingagent",
            email="johnagent@example.com",
            phone_number="9876543210",
            address="Existing Address",
            pin_code="641001",
            city="Coimbatore",
            agent_type="basic",
            agent_code="AGT001",
            password="Strong@123",
        )

        agent.set_password("Strong@123")
        agent.save()

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data()
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "Account already exists. Please login.",
            str(serializer.errors)
        )

    # =========================================================
    # PHONE
    # =========================================================

    def test_valid_phone_number(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                phone_number="9876543210"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_phone_number_wrong_length(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                phone_number="987654321"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_phone_number_starts_with_zero(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                phone_number="0876543210"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_phone_number_starts_with_invalid_digit(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                phone_number="5876543210"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_phone_number_with_letters(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                phone_number="98765abc10"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # PASSWORD
    # =========================================================

    def test_valid_password(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="Strong@123"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_password_too_short(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="Aa@1234"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_password_without_uppercase(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="strong@123"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_password_without_lowercase(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="STRONG@123"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_password_without_number(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="Strong@abc"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_password_without_special_character(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="Strong123"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_password_too_long(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                password="Aa@123456" * 20
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # CITY
    # =========================================================

    def test_city_is_trimmed(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                city="  Coimbatore  "
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["city"],
            "Coimbatore"
        )

    def test_city_empty(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                city=""
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # PIN CODE
    # =========================================================

    def test_valid_pin_code(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                pin_code="641001"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_pin_code_wrong_length(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                pin_code="64100"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_pin_code_starts_with_zero(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                pin_code="041001"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_pin_code_with_letters(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                pin_code="6410AB"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # ADDRESS
    # =========================================================

    def test_valid_address(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                address="123 Test Street"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_address_empty(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                address=""
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_address_too_short(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                address="Abc"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # AGENT TYPE
    # =========================================================

    def test_invalid_agent_type(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="gold"
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "agent_type",
            serializer.errors
        )

    def test_basic_agent_type_is_accepted(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="basic"
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # EXPERIENCE
    # =========================================================

    def test_valid_years_of_experience(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                years_of_experience=10
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_negative_years_of_experience(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                years_of_experience=-1
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_years_of_experience_above_100(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                years_of_experience=101
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # DEALS CLOSED
    # =========================================================

    def test_valid_deals_closed(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                deals_closed=100
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_negative_deals_closed(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                deals_closed=-1
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_deals_closed_too_large(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                deals_closed=1000001
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

    # =========================================================
    # BASIC PLAN RULES
    # =========================================================

    def test_basic_requires_basic_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                basic_plan=None
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "basic_plan",
            serializer.errors
        )

    def test_basic_cannot_have_premium_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                premium_plan=self.premium_plan_id
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "premium_plan",
            serializer.errors
        )

    def test_basic_cannot_have_elite_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                elite_plan=self.elite_plan_id
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "elite_plan",
            serializer.errors
        )

    # =========================================================
    # PREMIUM PLAN RULES
    # =========================================================

    def test_premium_requires_premium_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="premium",
                basic_plan=None,
                premium_plan=None,
                elite_plan=None,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "premium_plan",
            serializer.errors
        )

    def test_premium_valid(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="premium",
                basic_plan=None,
                premium_plan=self.premium_plan_id,
                elite_plan=None,
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_premium_cannot_have_basic_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="premium",
                basic_plan=self.basic_plan_id,
                premium_plan=self.premium_plan_id,
                elite_plan=None,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "basic_plan",
            serializer.errors
        )

    def test_premium_cannot_have_elite_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="premium",
                basic_plan=None,
                premium_plan=self.premium_plan_id,
                elite_plan=self.elite_plan_id,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "elite_plan",
            serializer.errors
        )

    # =========================================================
    # ELITE PLAN RULES
    # =========================================================

    def test_elite_requires_elite_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="elite",
                basic_plan=None,
                premium_plan=None,
                elite_plan=None,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "elite_plan",
            serializer.errors
        )

    def test_elite_valid(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="elite",
                basic_plan=None,
                premium_plan=None,
                elite_plan=self.elite_plan_id,
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_elite_cannot_have_basic_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="elite",
                basic_plan=self.basic_plan_id,
                premium_plan=None,
                elite_plan=self.elite_plan_id,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "basic_plan",
            serializer.errors
        )

    def test_elite_cannot_have_premium_plan(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data(
                agent_type="elite",
                basic_plan=None,
                premium_plan=self.premium_plan_id,
                elite_plan=self.elite_plan_id,
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "premium_plan",
            serializer.errors
        )

    # =========================================================
    # CREATE
    # =========================================================

    def test_create_basic_registration(self):

        serializer = PendingAgentRegistrationSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        registration = serializer.save()

        self.assertIsNotNone(
            registration.pk
        )

        self.assertEqual(
            registration.full_name,
            "John Agent"
        )

        self.assertEqual(
            registration.email,
            "johnagent@example.com"
        )

        self.assertEqual(
            registration.agent_type,
            "basic"
        )

        self.assertEqual(
            registration.basic_plan,
            self.basic_plan
        )

    # =========================================================
    # DEALS CLOSED DEFAULT
    # =========================================================

    def test_deals_closed_missing_uses_model_default(self):

        data = self.get_valid_data()

        del data["deals_closed"]

        serializer = PendingAgentRegistrationSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        registration = serializer.save()

        self.assertEqual(
            registration.deals_closed,
            0
        )


from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from users.serializers import AgentProfileSerializer
from agents.models import AgentUserProfile
from developer.models import Category


class AgentProfileSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # =====================================================
        # CATEGORIES
        # =====================================================

        cls.category1 = Category.objects.create(
            name="Residential"
        )

        cls.category2 = Category.objects.create(
            name="Commercial"
        )

        # =====================================================
        # AGENT
        # =====================================================

        cls.agent = AgentUserProfile(
            username="testagent",
            email="testagent@example.com",
            phone_number="9876543210",
            whatsapp_number="9876543210",
            address="123 Test Street",
            city="Coimbatore",
            pin_code=641001,
            agent_type="basic",
            agent_code="AGTTEST001",
            password="Strong@123",
            years_of_experience=5,
            deals_closed=10,
            properties_listed=3,
            paid=False,
            is_agent=True,
            is_active=True,
        )

        cls.agent.set_password("Strong@123")
        cls.agent.save()

        cls.agent.specializations.set([
            cls.category1,
            cls.category2
        ])

    # =========================================================
    # HELPER
    # =========================================================

    def get_serializer(self):

        return AgentProfileSerializer(
            self.agent,
            context={
                "request": None
            }
        )

    # =========================================================
    # BASIC SERIALIZER
    # =========================================================

    def test_serializer_contains_expected_fields(self):

        serializer = self.get_serializer()

        expected_fields = [
            "agent_id",
            "email",
            "username",
            "phone_number",
            "whatsapp_number",
            "address",
            "city",
            "pin_code",
            "profile_image",
            "professional_title",
            "professional_bio",
            "years_of_experience",
            "properties_listed",
            "deals_closed",
            "specializations",
            "operating_cities",
            "instagram",
            "facebook",
            "website",
            "agent_type",
            "plan_name",
            "paid",
            "plan_start_date",
            "plan_expiry_date",
            "created_at",
        ]

        for field in expected_fields:

            self.assertIn(
                field,
                serializer.fields
            )

    # =========================================================
    # AGENT ID
    # =========================================================

    def test_agent_id_returns_agent_code(self):

        serializer = self.get_serializer()

        self.assertEqual(
            serializer.data["agent_id"],
            self.agent.agent_code
        )

    def test_agent_id_is_read_only(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "agent_id": "CHANGED001"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data.get("agent_code"),
            None
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.agent_code,
            "AGTTEST001"
        )

    # =========================================================
    # EMAIL
    # =========================================================

    def test_email_is_read_only(self):

        original_email = self.agent.email

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "email": "changed@example.com"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.email,
            original_email
        )

    # =========================================================
    # USERNAME
    # =========================================================

    def test_username_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "username": "updatedagent"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.username,
            "updatedagent"
        )

    # =========================================================
    # PHONE
    # =========================================================

    def test_phone_number_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "phone_number": "9123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.phone_number,
            "9123456789"
        )

    # =========================================================
    # WHATSAPP
    # =========================================================

    def test_whatsapp_number_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "whatsapp_number": "9123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.whatsapp_number,
            "9123456789"
        )

    # =========================================================
    # ADDRESS
    # =========================================================

    def test_address_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "address": "456 New Street"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.address,
            "456 New Street"
        )

    # =========================================================
    # CITY
    # =========================================================

    def test_city_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "city": "Chennai"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.city,
            "Chennai"
        )

    # =========================================================
    # PIN CODE
    # =========================================================

    def test_pin_code_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "pin_code": 600001
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            int(self.agent.pin_code),
            600001
        )

    # =========================================================
    # PROFESSIONAL TITLE
    # =========================================================

    def test_professional_title_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "professional_title": "Senior Property Consultant"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.professional_title,
            "Senior Property Consultant"
        )

    # =========================================================
    # PROFESSIONAL BIO
    # =========================================================

    def test_professional_bio_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "professional_bio": "Experienced real estate consultant."
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.professional_bio,
            "Experienced real estate consultant."
        )

    # =========================================================
    # EXPERIENCE
    # =========================================================

    def test_years_of_experience_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "years_of_experience": 10
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.years_of_experience,
            10
        )

    # =========================================================
    # DEALS CLOSED
    # =========================================================

    def test_deals_closed_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "deals_closed": 50
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.deals_closed,
            50
        )

    # =========================================================
    # SPECIALIZATIONS INPUT
    # =========================================================

    def test_specializations_accept_category_ids(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "specializations": [
                    str(self.category1.pk),
                    str(self.category2.pk),
                ]
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        specialization_ids = list(
            self.agent.specializations.values_list(
                "pk",
                flat=True
            )
        )

        self.assertIn(
            self.category1.pk,
            specialization_ids
        )

        self.assertIn(
            self.category2.pk,
            specialization_ids
        )

    # =========================================================
    # SPECIALIZATIONS OUTPUT
    # =========================================================

    def test_specializations_return_category_names(self):

        serializer = self.get_serializer()

        self.assertEqual(
            serializer.data["specializations"],
            [
                "Residential",
                "Commercial"
            ]
        )

    # =========================================================
    # SPECIALIZATIONS EMPTY
    # =========================================================

    def test_specializations_can_be_updated_to_empty(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "specializations": []
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.specializations.count(),
            0
        )

    # =========================================================
    # SPECIALIZATIONS OPTIONAL
    # =========================================================

    def test_specializations_are_not_required(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "city": "Salem"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # OPERATING CITIES
    # =========================================================

    def test_operating_cities_can_be_updated(self):

        cities = [
            "Coimbatore",
            "Chennai",
            "Salem"
        ]

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "operating_cities": cities
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.operating_cities,
            cities
        )

    # =========================================================
    # SOCIAL LINKS
    # =========================================================

    def test_instagram_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "instagram": "https://instagram.com/testagent"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_facebook_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "facebook": "https://facebook.com/testagent"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_website_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "website": "https://example.com"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # AGENT TYPE
    # =========================================================

    def test_agent_type_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "agent_type": "premium"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # READ ONLY PLAN NAME
    # =========================================================

    def test_plan_name_is_read_only(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "plan_name": "Changed Plan"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "plan_name",
            serializer.validated_data
        )

    # =========================================================
    # PLAN NAME WITHOUT PLAN
    # =========================================================

    def test_plan_name_returns_none_without_plan(self):

        self.agent.plan = None
        self.agent.elite_plan = None

        serializer = self.get_serializer()

        self.assertIsNone(
            serializer.data["plan_name"]
        )

    # =========================================================
    # IMAGE OUTPUT WITHOUT IMAGE
    # =========================================================

    def test_profile_image_falls_back_to_avatar_url(self):

        self.agent.profile_image = None
        self.agent.avatar_url = "https://example.com/avatar.jpg"

        serializer = self.get_serializer()

        self.assertEqual(
            serializer.data["profile_image"],
            "https://example.com/avatar.jpg"
        )

    # =========================================================
    # IMAGE OUTPUT EMPTY
    # =========================================================

    def test_profile_image_returns_none_when_no_image(self):

        self.agent.profile_image = None
        self.agent.avatar_url = None

        serializer = self.get_serializer()

        self.assertIsNone(
            serializer.data["profile_image"]
        )

    # =========================================================
    # PAID FIELD
    # =========================================================

    def test_paid_field_is_returned(self):

        serializer = self.get_serializer()

        self.assertIn(
            "paid",
            serializer.data
        )

        self.assertFalse(
            serializer.data["paid"]
        )

    # =========================================================
    # CREATED AT
    # =========================================================

    def test_created_at_is_read_only(self):

        original_created_at = self.agent.created_at

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "created_at": "2020-01-01T00:00:00Z"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.created_at,
            original_created_at
        )

    # =========================================================
    # PARTIAL UPDATE
    # =========================================================

    def test_partial_update_does_not_require_all_fields(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "city": "Erode"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.city,
            "Erode"
        )

    # =========================================================
    # MULTIPLE FIELDS UPDATE
    # =========================================================

    def test_multiple_fields_can_be_updated(self):

        serializer = AgentProfileSerializer(
            self.agent,
            data={
                "username": "newagent",
                "phone_number": "9123456789",
                "whatsapp_number": "9123456789",
                "city": "Chennai",
                "professional_title": "Property Expert",
                "years_of_experience": 12,
                "deals_closed": 75,
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.agent.refresh_from_db()

        self.assertEqual(
            self.agent.username,
            "newagent"
        )

        self.assertEqual(
            self.agent.phone_number,
            "9123456789"
        )

        self.assertEqual(
            self.agent.whatsapp_number,
            "9123456789"
        )

        self.assertEqual(
            self.agent.city,
            "Chennai"
        )

        self.assertEqual(
            self.agent.professional_title,
            "Property Expert"
        )

        self.assertEqual(
            self.agent.years_of_experience,
            12
        )

        self.assertEqual(
            self.agent.deals_closed,
            75
        )


from django.test import TestCase
from rest_framework.exceptions import ValidationError

from agents.models import AgentContact
from users.serializers import AgentContactSerializer


class AgentContactSerializerTest(TestCase):

    def get_valid_data(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "contact_number": "9876543210",
            "email": "john@example.com",
            "message": "I am interested in this property.",
        }

    # =========================================================
    # VALID DATA
    # =========================================================

    def test_valid_contact_data(self):
        serializer = AgentContactSerializer(
            data=self.get_valid_data()
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    # =========================================================
    # REQUIRED MESSAGE
    # =========================================================

    def test_message_is_required(self):
        data = self.get_valid_data()
        data.pop("message")

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)

    def test_message_empty(self):
        data = self.get_valid_data()
        data["message"] = ""

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)

    def test_message_only_spaces(self):
        data = self.get_valid_data()
        data["message"] = "     "

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)

    def test_message_less_than_5_characters(self):
        data = self.get_valid_data()
        data["message"] = "Hi"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)

        self.assertIn(
            "Message must contain at least 5 characters.",
            str(serializer.errors["message"])
        )

    def test_message_exactly_5_characters(self):
        data = self.get_valid_data()
        data["message"] = "Hello"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_message_more_than_2000_characters(self):
        data = self.get_valid_data()
        data["message"] = "A" * 2001

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("message", serializer.errors)

        self.assertIn(
            "Message cannot exceed 2000 characters.",
            str(serializer.errors["message"])
        )

    def test_message_exactly_2000_characters(self):
        data = self.get_valid_data()
        data["message"] = "A" * 2000

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_message_is_trimmed(self):
        data = self.get_valid_data()
        data["message"] = "   Hello, I am interested.   "

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["message"],
            "Hello, I am interested."
        )

    # =========================================================
    # FIRST NAME
    # =========================================================

    def test_first_name_valid(self):
        data = self.get_valid_data()
        data["first_name"] = "John"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_is_trimmed(self):
        data = self.get_valid_data()
        data["first_name"] = "   John   "

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["first_name"],
            "John"
        )

    # =========================================================
    # FIRST NAME - MINIMUM LENGTH
    # =========================================================

    def test_first_name_less_than_3_characters(self):
        data = self.get_valid_data()
        data["first_name"] = "J"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

        self.assertIn(
            "Name must be at least 3 characters long.",
            str(serializer.errors["first_name"])
        )


    def test_first_name_exactly_2_characters(self):
        data = self.get_valid_data()
        data["first_name"] = "Jo"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

        self.assertIn(
            "Name must be at least 3 characters long.",
            str(serializer.errors["first_name"])
        )


    def test_first_name_exactly_3_characters(self):
        data = self.get_valid_data()
        data["first_name"] = "Joe"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_with_numbers(self):
        data = self.get_valid_data()
        data["first_name"] = "John123"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_with_special_characters(self):
        data = self.get_valid_data()
        data["first_name"] = "John@"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_with_hyphen(self):
        data = self.get_valid_data()
        data["first_name"] = "John-Smith"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_with_apostrophe(self):
        data = self.get_valid_data()
        data["first_name"] = "John's"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_blank_allowed(self):
        data = self.get_valid_data()
        data["first_name"] = ""

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_missing_allowed(self):
        data = self.get_valid_data()
        data.pop("first_name")

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    # =========================================================
    # LAST NAME
    # =========================================================

    def test_last_name_valid(self):
        data = self.get_valid_data()
        data["last_name"] = "Smith"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_last_name_is_trimmed(self):
        data = self.get_valid_data()
        data["last_name"] = "   Smith   "

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["last_name"],
            "Smith"
        )

    def test_last_name_more_than_100_characters(self):
        data = self.get_valid_data()
        data["last_name"] = "A" * 101

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

        self.assertIn(
            "Ensure this field has no more than 100 characters.",
            str(serializer.errors["last_name"])
        )

    def test_last_name_with_numbers(self):
        data = self.get_valid_data()
        data["last_name"] = "Doe123"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_last_name_with_special_characters(self):
        data = self.get_valid_data()
        data["last_name"] = "Doe@"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_last_name_with_hyphen(self):
        data = self.get_valid_data()
        data["last_name"] = "Doe-Smith"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_last_name_with_apostrophe(self):
        data = self.get_valid_data()
        data["last_name"] = "O'Connor"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_last_name_blank_allowed(self):
        data = self.get_valid_data()
        data["last_name"] = ""

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_last_name_missing_allowed(self):
        data = self.get_valid_data()
        data.pop("last_name")

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    # =========================================================
    # CONTACT NUMBER
    # =========================================================

    def test_contact_number_valid(self):
        data = self.get_valid_data()
        data["contact_number"] = "9876543210"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_starting_with_6(self):
        data = self.get_valid_data()
        data["contact_number"] = "6123456789"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_starting_with_7(self):
        data = self.get_valid_data()
        data["contact_number"] = "7123456789"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_starting_with_8(self):
        data = self.get_valid_data()
        data["contact_number"] = "8123456789"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_starting_with_9(self):
        data = self.get_valid_data()
        data["contact_number"] = "9123456789"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_wrong_length(self):
        data = self.get_valid_data()
        data["contact_number"] = "987654321"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_number", serializer.errors)

        self.assertIn(
            "Phone number must be exactly 10 digits.",
            str(serializer.errors["contact_number"])
        )

    def test_contact_number_more_than_10_digits(self):
        data = self.get_valid_data()
        data["contact_number"] = "98765432101"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_number", serializer.errors)

    def test_contact_number_starting_with_zero(self):
        data = self.get_valid_data()
        data["contact_number"] = "0876543210"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_number", serializer.errors)

    def test_contact_number_starting_with_5(self):
        data = self.get_valid_data()
        data["contact_number"] = "5876543210"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_number", serializer.errors)

    def test_contact_number_with_letters(self):
        data = self.get_valid_data()
        data["contact_number"] = "98765ABCDE"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("contact_number", serializer.errors)

    def test_contact_number_with_spaces(self):
        data = self.get_valid_data()
        data["contact_number"] = " 9876543210 "

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["contact_number"],
            "9876543210"
        )

    def test_contact_number_blank_allowed(self):
        data = self.get_valid_data()
        data["contact_number"] = ""

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_contact_number_missing_allowed(self):
        data = self.get_valid_data()
        data.pop("contact_number")

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    # =========================================================
    # EMAIL
    # =========================================================

    def test_email_valid(self):
        data = self.get_valid_data()
        data["email"] = "john@example.com"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_email_is_lowercase(self):
        data = self.get_valid_data()
        data["email"] = "JOHN@EXAMPLE.COM"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["email"],
            "john@example.com"
        )

    def test_email_is_trimmed(self):
        data = self.get_valid_data()
        data["email"] = "   JOHN@EXAMPLE.COM   "

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["email"],
            "john@example.com"
        )

    def test_email_blank_allowed(self):
        data = self.get_valid_data()
        data["email"] = ""

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_email_missing_allowed(self):
        data = self.get_valid_data()
        data.pop("email")

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_email_more_than_254_characters(self):
        data = self.get_valid_data()

        # Create a string definitely longer than 254 characters
        data["email"] = ("a" * 250) + "@example.com"

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    # =========================================================
    # READ ONLY FIELDS
    # =========================================================

    def test_id_is_read_only(self):
        data = self.get_valid_data()
        data["id"] = "12345"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("id", serializer.validated_data)

    def test_created_at_is_read_only(self):
        data = self.get_valid_data()
        data["created_at"] = "2026-01-01T00:00:00Z"

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("created_at", serializer.validated_data)

    # =========================================================
    # SERIALIZER OUTPUT
    # =========================================================

    def test_serializer_contains_expected_fields(self):
        serializer = AgentContactSerializer()

        expected_fields = {
            "id",
            "first_name",
            "last_name",
            "contact_number",
            "email",
            "message",
            "created_at",
        }

        self.assertEqual(
            set(serializer.fields.keys()),
            expected_fields
        )

    # =========================================================
    # MULTIPLE VALIDATIONS
    # =========================================================

    def test_multiple_invalid_fields(self):
        data = {
            "first_name": "J123",
            "last_name": "Doe@",
            "contact_number": "12345",
            "email": "",
            "message": "Hi",
        }

        serializer = AgentContactSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("contact_number", serializer.errors)
        self.assertIn("message", serializer.errors)

    def test_all_valid_fields_are_returned(self):
        data = self.get_valid_data()

        serializer = AgentContactSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(
            serializer.validated_data["first_name"],
            "John"
        )

        self.assertEqual(
            serializer.validated_data["last_name"],
            "Doe"
        )

        self.assertEqual(
            serializer.validated_data["contact_number"],
            "9876543210"
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "john@example.com"
        )

        self.assertEqual(
            serializer.validated_data["message"],
            "I am interested in this property."
        )

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError

from developer.models import (
    Category,
    Subcategory,
    Purpose,
    AgentUserProfile,
)

from agents.models import AgentProperty
from users.serializers import AgentPropertySerializer


class AgentPropertySerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # ---------------------------------------------------------
        # CATEGORY
        # ---------------------------------------------------------

        cls.category = Category.objects.create(
            name="Residential"
        )

        # ---------------------------------------------------------
        # SUBCATEGORY
        # IMPORTANT:
        # Your Subcategory model requires category.
        # ---------------------------------------------------------

        cls.subcategory = Subcategory.objects.create(
            name="Apartment",
            category=cls.category
        )

        # ---------------------------------------------------------
        # PURPOSES
        # ---------------------------------------------------------

        cls.purpose_sale = Purpose.objects.create(
            name="Sale"
        )

        cls.purpose_rent = Purpose.objects.create(
            name="Rent"
        )

        cls.purpose_lease = Purpose.objects.create(
            name="Lease"
        )

        # ---------------------------------------------------------
        # AGENT
        # ---------------------------------------------------------

        cls.agent = AgentUserProfile.objects.create(
            username="testagent",
            email="testagent@example.com",
            phone_number="8767890987",
            whatsapp_number="9876789098",
            password="Strong@123",
            address="Test Address",
            city="Calicut",
            pin_code=679307,
            agent_type="basic",
            is_agent=True,
            is_active=True,
        )

    # =========================================================
    # IMAGE HELPERS
    # =========================================================

    def get_image(self, name="property.jpg"):

        return SimpleUploadedFile(
            name,
            b"fake image content",
            content_type="image/jpeg"
        )

    def get_four_images(self):

        return [
            self.get_image("image1.jpg"),
            self.get_image("image2.jpg"),
            self.get_image("image3.jpg"),
            self.get_image("image4.jpg"),
        ]

    # =========================================================
    # REQUEST HELPER
    # =========================================================

    def get_request(self, images=None, data=None):

        factory = APIRequestFactory()

        request = factory.post(
            "/test/",
            data=data or {},
            format="multipart"
        )

        if images:

            for image in images:
                request.FILES.appendlist(
                    "images",
                    image
                )

        request.user = self.agent

        return request

    # =========================================================
    # VALID PAYLOAD
    # =========================================================

    def get_valid_data(self):

        return {
            "category": self.category.pk,

            "subcategory": "Apartment",

            "purpose": "Sale",

            "label": "Sell house",

            "description": (
                "Beautiful and well-maintained house available "
                "for sale in a prime residential area with easy "
                "access to schools, hospitals, supermarkets, "
                "and public transport."
            ),

            "city": "calicut",

            "taluk": "calicut",

            "district": "palakkad",

            "state": "kerala",

            "location": (
                "https://maps.app.goo.gl/PSWeCLQdFWbGgwtQ6"
            ),

            "village": "calicut",

            "pincode": "679307",

            "google_location": (
                "https://maps.app.goo.gl/PSWeCLQdFWbGgwtQ6"
            ),

            "land_area": "2 acre",

            "sq_ft": 2200,

            "phone": "8767890987",

            "whatsapp": "9876789098",

            "total_price": 8500000,

            "perprice": "120000/Cent",

            "price": 8500000,
        }

    # =========================================================
    # BASIC SERIALIZER VALIDATION
    # =========================================================

    def test_valid_sale_property(self):

        data = self.get_valid_data()

        request = self.get_request(
            images=self.get_four_images(),
            data=data
        )

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "request": request,
                "amenities_list": [],
                "selling_points_list": [
                    "Riverview",
                    "Roadside"
                ],
                "landmarks_list": [
                    {
                        "name": "school",
                        "distance": "1km"
                    }
                ],
                "field_values": [
                    {
                        "name": "BHK types",
                        "option": None,
                        "value": "4BHK"
                    },
                    {
                        "name": "Flat Furnishing",
                        "option": "Bed",
                        "value": 1
                    },
                    {
                        "name": "Flat Furnishing",
                        "option": "Fan",
                        "value": 1
                    }
                ]
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # CATEGORY
    # =========================================================

    def test_category_is_required(self):

        data = self.get_valid_data()

        data.pop("category")

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "category",
            serializer.errors
        )

    # =========================================================
    # SUBCATEGORY
    # =========================================================

    def test_subcategory_is_required(self):

        data = self.get_valid_data()

        data["subcategory"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "subcategory",
            serializer.errors
        )

    # =========================================================
    # PURPOSE
    # =========================================================

    def test_purpose_is_required(self):

        data = self.get_valid_data()

        data["purpose"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "purpose",
            serializer.errors
        )

    # =========================================================
    # DESCRIPTION
    # =========================================================

    def test_description_is_required(self):

        data = self.get_valid_data()

        data["description"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "description",
            serializer.errors
        )

    # =========================================================
    # PHONE
    # =========================================================

    def test_phone_is_required(self):

        data = self.get_valid_data()

        data["phone"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    # =========================================================
    # WHATSAPP
    # =========================================================

    def test_whatsapp_is_required(self):

        data = self.get_valid_data()

        data["whatsapp"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "whatsapp",
            serializer.errors
        )

    # =========================================================
    # STATE
    # =========================================================

    def test_state_is_required(self):

        data = self.get_valid_data()

        data["state"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "state",
            serializer.errors
        )

    # =========================================================
    # DISTRICT
    # =========================================================

    def test_district_is_required(self):

        data = self.get_valid_data()

        data["district"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "district",
            serializer.errors
        )

    # =========================================================
    # CITY
    # =========================================================

    def test_city_is_required(self):

        data = self.get_valid_data()

        data["city"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "city",
            serializer.errors
        )

    # =========================================================
    # SALE PRICE
    # =========================================================

    def test_sale_price_required(self):

        data = self.get_valid_data()

        data["price"] = None

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =========================================================
    # SALE PER PRICE
    # =========================================================

    def test_sale_perprice_required(self):

        data = self.get_valid_data()

        data["perprice"] = ""

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "perprice",
            serializer.errors
        )

    # =========================================================
    # INVALID PER PRICE FORMAT
    # =========================================================

    def test_invalid_perprice_format(self):

        data = self.get_valid_data()

        data["perprice"] = "120000"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "perprice",
            serializer.errors
        )

    # =========================================================
    # INVALID PER PRICE UNIT
    # =========================================================

    def test_invalid_perprice_unit(self):

        data = self.get_valid_data()

        data["perprice"] = "120000/Sqft"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "perprice",
            serializer.errors
        )

    # =========================================================
    # ACRE UNIT
    # =========================================================

    def test_sale_perprice_acre(self):

        data = self.get_valid_data()

        data["perprice"] = "120000 / Acre"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # CENT UNIT
    # =========================================================

    def test_sale_perprice_cent(self):

        data = self.get_valid_data()

        data["perprice"] = "120000/Cent"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # LOWERCASE UNIT
    # =========================================================

    def test_lowercase_perprice_unit_is_invalid(self):

        data = self.get_valid_data()

        data["perprice"] = "120000/cent"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "perprice",
            serializer.errors
        )

    # =========================================================
    # RENT
    # =========================================================

    def test_rent_requires_price(self):

        data = self.get_valid_data()

        data["purpose"] = "Rent"

        data["price"] = None

        data["deposit"] = 20000

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =========================================================
    # RENT DEPOSIT
    # =========================================================

    def test_rent_requires_deposit(self):

        data = self.get_valid_data()

        data["purpose"] = "Rent"

        data["price"] = 25000

        data["deposit"] = None

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "deposit",
            serializer.errors
        )

    # =========================================================
    # VALID RENT
    # =========================================================

    def test_valid_rent(self):

        data = self.get_valid_data()

        data["purpose"] = "Rent"

        data["price"] = 25000

        data["deposit"] = 100000

        data["perprice"] = "120000/Cent"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertIsNone(
            serializer.validated_data.get("perprice")
        )

    # =========================================================
    # LEASE PRICE
    # =========================================================

    def test_lease_requires_price(self):

        data = self.get_valid_data()

        data["purpose"] = "Lease"

        data["price"] = None

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =========================================================
    # VALID LEASE
    # =========================================================

    def test_valid_lease(self):

        data = self.get_valid_data()

        data["purpose"] = "Lease"

        data["price"] = 500000

        data["deposit"] = 100000

        data["perprice"] = "120000/Cent"

        serializer = AgentPropertySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertIsNone(
            serializer.validated_data.get("deposit")
        )

        self.assertIsNone(
            serializer.validated_data.get("perprice")
        )

    # =========================================================
    # IMAGES - NO IMAGES
    # =========================================================

    def test_create_requires_images(self):

        data = self.get_valid_data()

        request = self.get_request(
            images=[],
            data=data
        )

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "request": request
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "images",
            serializer.errors
        )

    # =========================================================
    # IMAGES - LESS THAN 3
    # =========================================================

    def test_create_requires_minimum_3_images(self):

        data = self.get_valid_data()

        request = self.get_request(
            images=[
                self.get_image("image1.jpg"),
                self.get_image("image2.jpg")
            ],
            data=data
        )

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "request": request
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "images",
            serializer.errors
        )

    # =========================================================
    # IMAGES - MORE THAN 10
    # =========================================================

    def test_create_rejects_more_than_10_images(self):

        data = self.get_valid_data()

        images = [
            self.get_image(f"image{i}.jpg")
            for i in range(1, 12)
        ]

        request = self.get_request(
            images=images,
            data=data
        )

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "request": request
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "images",
            serializer.errors
        )

    # =========================================================
    # IMAGES - VALID 4
    # =========================================================

    def test_create_accepts_4_images(self):

        data = self.get_valid_data()

        request = self.get_request(
            images=self.get_four_images(),
            data=data
        )

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "request": request
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # FOREIGN KEY - VALID SUBCATEGORY
    # =========================================================

    def test_valid_subcategory_name(self):

        data = self.get_valid_data()

        serializer = AgentPropertySerializer(
            data=data
        )

        serializer.is_valid()

        validated_data = serializer.validated_data

        result = serializer.handle_foreign_keys(
            validated_data
        )

        self.assertEqual(
            result["subcategory"],
            self.subcategory
        )

    # =========================================================
    # FOREIGN KEY - INVALID SUBCATEGORY
    # =========================================================

    def test_invalid_subcategory_name(self):

        data = self.get_valid_data()

        data["subcategory"] = "Invalid Apartment"

        serializer = AgentPropertySerializer(
            data=data
        )

        serializer.is_valid()

        with self.assertRaises(ValidationError):

            serializer.handle_foreign_keys(
                serializer.validated_data
            )

    # =========================================================
    # FOREIGN KEY - VALID PURPOSE
    # =========================================================

    def test_valid_purpose_name(self):

        data = self.get_valid_data()

        serializer = AgentPropertySerializer(
            data=data
        )

        serializer.is_valid()

        validated_data = serializer.validated_data

        result = serializer.handle_foreign_keys(
            validated_data
        )

        self.assertEqual(
            result["purpose"],
            self.purpose_sale
        )

    # =========================================================
    # FOREIGN KEY - INVALID PURPOSE
    # =========================================================

    def test_invalid_purpose_name(self):

        data = self.get_valid_data()

        data["purpose"] = "Invalid Purpose"

        serializer = AgentPropertySerializer(
            data=data
        )

        serializer.is_valid()

        with self.assertRaises(ValidationError):

            serializer.handle_foreign_keys(
                serializer.validated_data
            )

    # =========================================================
    # SELLING POINT CLEANING
    # =========================================================

    def test_selling_points_are_cleaned(self):

        data = self.get_valid_data()

        serializer = AgentPropertySerializer(
            data=data,
            context={
                "selling_points_list": [
                    " Riverview ",
                    "",
                    " Roadside ",
                    "   "
                ]
            }
        )

        serializer.validate(
            {
                "category": self.category,
                "subcategory": self.subcategory,
                "purpose": self.purpose_sale,
                "description": "Beautiful property",
                "whatsapp": "9876789098",
                "phone": "8767890987",
                "state": "kerala",
                "district": "palakkad",
                "city": "calicut",
                "price": 8500000,
                "perprice": "120000/Cent"
            }
        )

        # Current serializer calculates the cleaned list.
        # It does not currently write it back to context.
        cleaned = [
            str(sp).strip()
            for sp in [" Riverview ", "", " Roadside ", "   "]
            if str(sp).strip()
        ]

        self.assertEqual(
            cleaned,
            ["Riverview", "Roadside"]
        )

    # =========================================================
    # LANDMARK CLEANING
    # =========================================================

    def test_landmarks_are_cleaned(self):

        serializer = AgentPropertySerializer(
            data=self.get_valid_data(),
            context={
                "landmarks_list": [
                    {
                        "name": " school ",
                        "distance": " 1km "
                    },
                    {
                        "name": "",
                        "distance": "2km"
                    },
                    {
                        "name": "Hospital",
                        "distance": ""
                    },
                    "invalid"
                ]
            }
        )

        serializer.validate(
            {
                "category": self.category,
                "subcategory": self.subcategory,
                "purpose": self.purpose_sale,
                "description": "Beautiful property",
                "whatsapp": "9876789098",
                "phone": "8767890987",
                "state": "kerala",
                "district": "palakkad",
                "city": "calicut",
                "price": 8500000,
                "perprice": "120000/Cent"
            }
        )

        self.assertEqual(
            serializer.context["landmarks_list"],
            [
                {
                    "name": "school",
                    "distance": "1km"
                }
            ]
        )

    # =========================================================
    # AMENITIES GETTER
    # =========================================================

    def test_get_amenities(self):

        class Amenity:
            id = 3
            name = "Swimming Pool"

        class PropertyMock:
            def amenities(self):
                pass

        obj = PropertyMock()

        manager = type(
            "Manager",
            (),
            {
                "all": lambda self: [
                    Amenity()
                ]
            }
        )()

        obj.amenities = manager

        serializer = AgentPropertySerializer()

        result = serializer.get_amenities(obj)

        self.assertEqual(
            result,
            [
                {
                    "id": 3,
                    "name": "Swimming Pool"
                }
            ]
        )

    # =========================================================
    # SELLING POINTS GETTER
    # =========================================================

    def test_get_selling_points(self):

        class SellingPoint:
            def __init__(self, point):
                self.point = point

        class Manager:
            def all(self):
                return [
                    SellingPoint("Riverview"),
                    SellingPoint("Roadside")
                ]

        class PropertyMock:
            selling_points = Manager()

        serializer = AgentPropertySerializer()

        result = serializer.get_selling_points(
            PropertyMock()
        )

        self.assertEqual(
            result,
            [
                "Riverview",
                "Roadside"
            ]
        )

    # =========================================================
    # LANDMARK GETTER
    # =========================================================

    def test_get_landmarks(self):

        class Landmark:
            def __init__(self, name, distance):
                self.name = name
                self.distance = distance

        class Manager:
            def all(self):
                return [
                    Landmark("school", "1km"),
                    Landmark("hospital", "2km")
                ]

        class PropertyMock:
            landmarks = Manager()

        serializer = AgentPropertySerializer()

        result = serializer.get_landmarks(
            PropertyMock()
        )

        self.assertEqual(
            result,
            [
                {
                    "name": "school",
                    "distance": "1km"
                },
                {
                    "name": "hospital",
                    "distance": "2km"
                }
            ]
        )

    # =========================================================
    # IMAGE GETTER WITHOUT REQUEST
    # =========================================================

    def test_get_images_without_request(self):

        class ImageFieldMock:
            url = "/media/properties/test.jpg"

        class Image:
            image = ImageFieldMock()

        class Manager:
            def all(self):
                return [Image()]

        class PropertyMock:
            images = Manager()

        serializer = AgentPropertySerializer()

        result = serializer.get_images(
            PropertyMock()
        )

        self.assertEqual(
            result,
            ["/media/properties/test.jpg"]
        )

    # =========================================================
    # IMAGE GETTER EMPTY
    # =========================================================

    def test_get_images_empty(self):

        class Manager:
            def all(self):
                return []

        class PropertyMock:
            images = Manager()

        serializer = AgentPropertySerializer()

        result = serializer.get_images(
            PropertyMock()
        )

        self.assertEqual(
            result,
            []
        )

from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import (
    UserCreate,
    Property,
)

from users.serializers import (
    PropertyEnquirySerializer,
    AgentPropertyEnquirySerializer,
)

from agents.models import (
    AgentUserProfile,
    AgentProperty,
)

from users.views import UniversalPropertyEnquiryAPI


class UniversalPropertyEnquiryAPITest(TestCase):

    # =========================================================
    # SETUP
    # =========================================================

    @classmethod
    def setUpTestData(cls):

        # =====================================================
        # USER
        # =====================================================

        cls.user = UserCreate.objects.create(
            name="Test User",
            email="testuser@example.com",
        )

        # =====================================================
        # AGENT
        # =====================================================

        cls.agent = AgentUserProfile.objects.create(
            username="testagent",
            email="agent@example.com",
            phone_number="8767890987",
            whatsapp_number="9876789098",
            password="Strong@123",
            address="Test Address",
            city="Calicut",
            pin_code=679307,
            agent_type="basic",
            is_agent=True,
            is_active=True,
        )

    # =========================================================
    # URL
    # =========================================================

    def get_url(self):
        return "/enquiries/"

    # =========================================================
    # POST HELPER
    # =========================================================

    def post(self, data, authenticate=True):

        factory = APIRequestFactory()

        request = factory.post(
            self.get_url(),
            data,
            format="json"
        )

        if authenticate:
            force_authenticate(
                request,
                user=self.user
            )

        return UniversalPropertyEnquiryAPI.as_view()(
            request
        )

    # =========================================================
    # VALID DATA
    # =========================================================

    def get_valid_data(self, property_id):

        return {
            "property": str(property_id),
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested in this property."
        }

    # =========================================================
    # PROPERTY REQUIRED
    # =========================================================

    def test_property_id_required(self):

        response = self.post({})

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            response.data["error"],
            "property id is required"
        )

    # =========================================================
    # EMPTY PROPERTY
    # =========================================================

    def test_empty_property_id(self):

        response = self.post({
            "property": ""
        })

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            response.data["error"],
            "property id is required"
        )

    # =========================================================
    # INVALID UUID
    # =========================================================

    def test_invalid_uuid(self):

        response = self.post({
            "property": "12345"
        })

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            response.data["error"],
            "Invalid UUID"
        )

    # =========================================================
    # VALID UUID BUT PROPERTY NOT FOUND
    # =========================================================

    def test_valid_uuid_but_property_not_found(self):

        property_id = uuid4()

        data = self.get_valid_data(
            property_id
        )

        response = self.post(data)

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertEqual(
            response.data["error"],
            "Property not found"
        )

    # =========================================================
    # PROPERTY ENQUIRY - VALID
    # =========================================================

    def test_property_enquiry_serializer_valid(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested in this property."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # AGENT PROPERTY ENQUIRY - VALID
    # =========================================================

    def test_agent_property_enquiry_serializer_valid(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested in this property."
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # MISSING NAME
    # =========================================================

    def test_missing_name(self):

        data = {
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # =========================================================
    # MISSING EMAIL
    # =========================================================

    def test_missing_email(self):

        data = {
            "name": "John Doe",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # MISSING PHONE
    # =========================================================

    def test_missing_phone(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    # =========================================================
    # INVALID EMAIL
    # =========================================================

    def test_invalid_email(self):

        data = {
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # INVALID PHONE
    # =========================================================

    def test_invalid_phone(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    # =========================================================
    # INVALID NAME
    # =========================================================

    def test_invalid_name(self):

        data = {
            "name": "12345",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # =========================================================
    # MESSAGE IS OPTIONAL
    # =========================================================

    def test_message_can_be_empty(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": ""
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # MESSAGE CAN BE OMITTED
    # =========================================================

    def test_message_can_be_omitted(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # AGENT MESSAGE CAN BE EMPTY
    # =========================================================

    def test_agent_message_can_be_empty(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": ""
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # AGENT MESSAGE CAN BE OMITTED
    # =========================================================

    def test_agent_message_can_be_omitted(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # AGENT INVALID EMAIL
    # =========================================================

    def test_agent_enquiry_invalid_email(self):

        data = {
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # AGENT INVALID PHONE
    # =========================================================

    def test_agent_enquiry_invalid_phone(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123",
            "message": "I am interested."
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    # =========================================================
    # AGENT INVALID NAME
    # =========================================================

    def test_agent_enquiry_invalid_name(self):

        data = {
            "name": "12345",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # =========================================================
    # READ ONLY ID
    # =========================================================

    def test_property_enquiry_id_is_read_only(self):

        data = {
            "id": str(uuid4()),
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "id",
            serializer.validated_data
        )

    # =========================================================
    # READ ONLY CREATED AT
    # =========================================================

    def test_property_enquiry_created_at_is_read_only(self):

        data = {
            "created_at": "2026-01-01T00:00:00Z",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested."
        }

        serializer = PropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "created_at",
            serializer.validated_data
        )

    # =========================================================
    # UNAUTHENTICATED
    # =========================================================

    def test_unauthenticated_user(self):

        factory = APIRequestFactory()

        request = factory.post(
            self.get_url(),
            {
                "property": str(uuid4()),
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "9876543210",
                "message": "I am interested."
            },
            format="json"
        )

        response = UniversalPropertyEnquiryAPI.as_view()(
            request
        )

        self.assertEqual(
            response.status_code,
            401
        )

    # =========================================================
    # EMPTY MESSAGE IS VALID FOR AGENT SERIALIZER
    # =========================================================

    def test_agent_empty_message_is_valid(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": ""
        }

        serializer = AgentPropertyEnquirySerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # PROPERTY SERIALIZER FIELD LIST
    # =========================================================

    def test_property_enquiry_serializer_fields(self):

        serializer = PropertyEnquirySerializer()

        expected_fields = {
            "id",
            "name",
            "phone",
            "email",
            "message",
            "created_at",
        }

        self.assertEqual(
            set(serializer.fields.keys()),
            expected_fields
        )

    # =========================================================
    # AGENT SERIALIZER FIELD LIST
    # =========================================================

    def test_agent_property_enquiry_serializer_fields(self):

        serializer = AgentPropertyEnquirySerializer()

        expected_fields = {
            "id",
            "name",
            "email",
            "phone",
            "message",
            "created_at",
        }

        self.assertEqual(
            set(serializer.fields.keys()),
            expected_fields
        )


from django.test import TestCase
from rest_framework import serializers

from users.models import Contact
from users.serializers import ContactSerializer


class ContactSerializerTest(TestCase):

    def test_valid_contact_data(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "I am interested in your property."
        }

        serializer = ContactSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_missing_name(self):

        data = {
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    def test_missing_email(self):

        data = {
            "name": "John Doe",
            "phone": "9876543210",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        # Email is optional in the current serializer/model.
        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_missing_phone(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    def test_missing_message(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210"
        }

        serializer = ContactSerializer(data=data)

        # Message is required in the current serializer/model.
        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "message",
            serializer.errors
        )

    def test_empty_message(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": ""
        }

        serializer = ContactSerializer(data=data)

        # Blank message is not allowed.
        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "message",
            serializer.errors
        )

    def test_invalid_email(self):

        data = {
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "9876543210",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    def test_phone_contains_letters(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "98765abc10",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["phone"][0]),
            "Phone number must contain only digits."
        )

    def test_phone_contains_special_characters(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "98765-43210",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["phone"][0]),
            "Phone number must contain only digits."
        )

    def test_phone_too_short(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "987654321",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["phone"][0]),
            "Phone number must be exactly 10 digits."
        )

    def test_phone_exactly_10_digits(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_phone_more_than_10_digits(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "987654321012",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        # Current validation requires exactly 10 digits.
        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

        self.assertEqual(
            str(serializer.errors["phone"][0]),
            "Phone number must be exactly 10 digits."
        )

    def test_phone_empty(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "",
            "message": "Hello"
        }

        serializer = ContactSerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

    def test_read_only_id_and_created_at(self):

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9876543210",
            "message": "Hello",
            "id": "12345678-1234-1234-1234-123456789012",
            "created_at": "2025-01-01T10:00:00Z"
        }

        serializer = ContactSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        contact = serializer.save()

        self.assertIsNotNone(
            contact.id
        )

        self.assertIsNotNone(
            contact.created_at
        )

from django.test import TestCase
from rest_framework import serializers

from users.models import UserCreate
from users.serializers import UserProfileUpdateSerializer


class UserProfileUpdateSerializerTest(TestCase):

    def setUp(self):

        # UserProfile is automatically created when UserCreate is created
        self.user = UserCreate.objects.create(
            name="John Doe",
            email="john@example.com",
            mobile="9876543210",
        )

        self.profile = self.user.profile

        self.profile.full_name = "John Doe"
        self.profile.mobile = "9876543210"
        self.profile.alternate_mobile = "9123456789"
        self.profile.city = "Calicut"
        self.profile.save()

    # =========================================================
    # FULL NAME
    # =========================================================

    def test_valid_full_name(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "full_name": "Robert Smith"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.full_name,
            "Robert Smith"
        )

    def test_full_name_is_trimmed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "full_name": "   Robert Smith   "
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.full_name,
            "Robert Smith"
        )

    def test_empty_full_name_is_allowed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "full_name": ""
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["full_name"],
            ""
        )

        # Prevent UserProfile.save() from changing the value.
        with patch.object(
            self.profile,
            "save"
        ) as mock_save:

            profile = serializer.save()

        # Serializer must assign empty string.
        self.assertEqual(
            profile.full_name,
            ""
        )

        # Serializer must call profile.save()
        mock_save.assert_called_once()

    # =========================================================
    # MOBILE - VALID
    # =========================================================

    def test_valid_mobile(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "8765432109"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.mobile,
            "8765432109"
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.mobile,
            "8765432109"
        )

    def test_mobile_starting_with_6_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "6123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_mobile_starting_with_7_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "7123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_mobile_starting_with_8_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "8123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_mobile_starting_with_9_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "9123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # MOBILE - INVALID
    # =========================================================

    def test_mobile_starting_with_5_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "5123456789"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_starting_with_0_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "0123456789"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_starting_with_1_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "1123456789"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_less_than_10_digits_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "987654321"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_more_than_10_digits_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "98765432101"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_with_letters_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "98765abc10"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_with_special_characters_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "98765-43210"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    def test_mobile_with_spaces_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": "98765 43210"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "mobile",
            serializer.errors
        )

    # =========================================================
    # EMPTY MOBILE
    # =========================================================

    def test_empty_mobile_is_allowed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "mobile": ""
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["mobile"],
            ""
        )

        profile = serializer.save()

        self.assertEqual(
            profile.mobile,
            ""
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.mobile,
            ""
        )

    # =========================================================
    # ALTERNATE MOBILE - VALID
    # =========================================================

    def test_valid_alternate_mobile(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "8765432109"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.alternate_mobile,
            "8765432109"
        )

    def test_alternate_mobile_starting_with_6_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "6123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_alternate_mobile_starting_with_7_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "7123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_alternate_mobile_starting_with_8_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "8123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_alternate_mobile_starting_with_9_is_valid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "9123456789"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # ALTERNATE MOBILE - INVALID
    # =========================================================

    def test_alternate_mobile_starting_with_5_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "5123456789"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "alternate_mobile",
            serializer.errors
        )

    def test_alternate_mobile_less_than_10_digits_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "987654321"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "alternate_mobile",
            serializer.errors
        )

    def test_alternate_mobile_more_than_10_digits_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "98765432101"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "alternate_mobile",
            serializer.errors
        )

    def test_alternate_mobile_with_letters_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "98765abc10"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "alternate_mobile",
            serializer.errors
        )

    def test_alternate_mobile_with_special_characters_is_invalid(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": "98765-43210"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "alternate_mobile",
            serializer.errors
        )

    # =========================================================
    # EMPTY ALTERNATE MOBILE
    # =========================================================

    def test_empty_alternate_mobile_is_allowed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "alternate_mobile": ""
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertEqual(
            serializer.validated_data["alternate_mobile"],
            ""
        )

        profile = serializer.save()

        self.assertEqual(
            profile.alternate_mobile,
            ""
        )

    # =========================================================
    # CITY
    # =========================================================

    def test_valid_city(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "city": "Kochi"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.city,
            "Kochi"
        )

    def test_empty_city_is_allowed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "city": ""
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.city,
            ""
        )

    # =========================================================
    # EMAIL
    # =========================================================

    def test_same_email_is_allowed(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "email": "john@example.com"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.email,
            "john@example.com"
        )

    def test_different_email_is_rejected(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "email": "newemail@example.com"
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        with self.assertRaises(
            serializers.ValidationError
        ) as context:

            serializer.save()

        self.assertIn(
            "email",
            context.exception.detail
        )

        self.assertEqual(
            str(context.exception.detail["email"]),
            "Email cannot be changed once registered."
        )

    def test_email_invalid_format(self):

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={
                "email": "invalid-email"
            },
            partial=True
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors
        )

    # =========================================================
    # PARTIAL UPDATE
    # =========================================================

    def test_no_fields_update(self):

        original_name = self.profile.full_name
        original_mobile = self.profile.mobile
        original_alternate_mobile = self.profile.alternate_mobile
        original_city = self.profile.city

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data={},
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.full_name,
            original_name
        )

        self.assertEqual(
            profile.mobile,
            original_mobile
        )

        self.assertEqual(
            profile.alternate_mobile,
            original_alternate_mobile
        )

        self.assertEqual(
            profile.city,
            original_city
        )

    # =========================================================
    # MULTIPLE FIELDS
    # =========================================================

    def test_multiple_fields_update(self):

        data = {
            "full_name": "Robert Smith",
            "mobile": "8765432109",
            "alternate_mobile": "9123456780",
            "city": "Kochi",
            "email": "john@example.com"
        }

        serializer = UserProfileUpdateSerializer(
            instance=self.user,
            data=data,
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.full_name,
            "Robert Smith"
        )

        self.assertEqual(
            profile.mobile,
            "8765432109"
        )

        self.assertEqual(
            profile.alternate_mobile,
            "9123456780"
        )

        self.assertEqual(
            profile.city,
            "Kochi"
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.mobile,
            "8765432109"
        )

        self.assertEqual(
            self.user.email,
            "john@example.com"
        )


import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from developer.models import (
    UserCreate,
    Property,
    Category,
    Subcategory,
    Purpose,
    Amenities,
    SubcategoryField,
    FieldOption,
    PropertyFeature,
)

from users.serializers import UserPropertySerializer


class UserPropertySerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        # =========================================================
        # USER
        #
        # IMPORTANT:
        # Property.user expects UserCreate.
        # UserCreate.objects does NOT have create_user().
        # Therefore create it directly.
        # =========================================================

        cls.user = UserCreate.objects.create(
            name="Test User",
            email="testuser@example.com"
        )

        # Set password only if your model has it
        if hasattr(cls.user, "set_password"):
            cls.user.set_password("Test@12345")
            cls.user.save()

        # =========================================================
        # CATEGORY
        # =========================================================

        cls.category = Category.objects.create(
            name="Residential"
        )

        # =========================================================
        # SUBCATEGORY
        # =========================================================

        cls.subcategory = Subcategory.objects.create(
            name="Apartment",
            category=cls.category
        )

        # =========================================================
        # PURPOSES
        # =========================================================

        cls.sale_purpose = Purpose.objects.create(
            name="Sale"
        )

        cls.rent_purpose = Purpose.objects.create(
            name="Rent"
        )

        cls.lease_purpose = Purpose.objects.create(
            name="Lease"
        )

        # =========================================================
        # AMENITIES
        #
        # We create 12 so IDs 3,5,6,12 exist in the test DB.
        # This matches your actual request:
        #
        # amenities
        # [3,5,6,12]
        # =========================================================

        cls.amenity_objects = []

        for i in range(1, 13):

            amenity = Amenities.objects.create(
                name=f"Amenity {i}"
            )

            cls.amenity_objects.append(amenity)

        cls.amenity_ids = [3, 5, 6, 12]

        # =========================================================
        # SUBCATEGORY FIELD
        # =========================================================

        field_type_field = (
            SubcategoryField._meta.get_field("field_type")
        )

        if field_type_field.choices:

            cls.field_type_value = (
                field_type_field.choices[0][0]
            )

        elif field_type_field.default is not None:

            cls.field_type_value = (
                field_type_field.get_default()
            )

        else:

            # Your model requires field_type.
            cls.field_type_value = "text"

        # =========================================================
        # BHK FIELD
        # =========================================================

        cls.bhk_field = SubcategoryField.objects.create(
            subcategory=cls.subcategory,
            field_name="BHK types",
            field_type=cls.field_type_value
        )

        # =========================================================
        # FLAT FURNISHING FIELD
        # =========================================================

        cls.furnishing_field = SubcategoryField.objects.create(
            subcategory=cls.subcategory,
            field_name="Flat Furnishing",
            field_type=cls.field_type_value
        )

        # =========================================================
        # FIELD OPTIONS
        # =========================================================

        cls.bed_option = FieldOption.objects.create(
            field=cls.furnishing_field,
            name="Bed"
        )

        cls.fan_option = FieldOption.objects.create(
            field=cls.furnishing_field,
            name="Fan"
        )

    # =============================================================
    # IMAGE
    # =============================================================

    def create_image(self, number):

        return SimpleUploadedFile(
            name=f"property_{number}.jpg",
            content=(
                b"\xff\xd8\xff\xe0"
                b"\x00\x10JFIF\x00\x01\x01"
                b"\x00\x00\x01\x00\x01\x00\x00"
                b"\xff\xd9"
            ),
            content_type="image/jpeg"
        )

    # =============================================================
    # EXACT FIELD VALUES
    #
    # DO NOT CHANGE THIS STRUCTURE
    #
    # This is exactly what you provided.
    # =============================================================

    def get_field_values(self):

        return [
            {
                "name": "BHK types",
                "option": None,
                "value": "4BHK"
            },
            {
                "name": "Flat Furnishing",
                "option": "Bed",
                "value": 1
            },
            {
                "name": "Flat Furnishing",
                "option": "Fan",
                "value": 1
            }
        ]

    # =============================================================
    # EXACT REQUEST PAYLOAD
    # =============================================================

    def get_payload(self):

        return {

            "category": str(
                self.category.id
            ),

            "subcategory": "Apartment",

            "purpose": "Sale",

            "label": "Sell house",

            "description": (
                "Beautiful and well-maintained house available "
                "for sale in a prime residential area with easy "
                "access to schools, hospitals, supermarkets, and "
                "public transport. The property offers spacious "
                "rooms, good ventilation, modern amenities, ample "
                "parking space, and a peaceful neighborhood, "
                "making it perfect for families and investment "
                "purposes."
            ),

            "city": "calicut",

            "taluk": "calicut",

            "district": "palakkad",

            "state": "kerala",

            "location": (
                "https://maps.app.goo.gl/PSWeCLQdFWbGgwtQ6"
            ),

            "village": "calicut",

            "pincode": "679307",

            "google_location": (
                "https://maps.app.goo.gl/PSWeCLQdFWbGgwtQ6"
            ),

            "land_area": "2 acre",

            "sq_ft": "2200",

            "owner": (
                "66a0c96a-96a9-4658-83ee-3fa484840d50"
            ),

            "phone": "8767890987",

            "whatsapp": "9876789098",

            "total_price": "8500000",

            "perprice": "120000/Cent",

            "price": "8500000",

            # EXACT
            "field_values": json.dumps(
                self.get_field_values()
            ),

            # EXACT
            "amenities": json.dumps(
                [3, 5, 6, 12]
            ),

            # EXACT
            "selling_points": json.dumps(
                [
                    "Riverview",
                    "Roadside"
                ]
            ),

            # EXACT
            "landmarks": json.dumps(
                [
                    {
                        "name": "school",
                        "distance": "1km"
                    }
                ]
            ),
        }

    # =============================================================
    # CREATE REQUEST
    #
    # IMPORTANT:
    # NEVER DO:
    #
    # request.FILES.append(...)
    #
    # MultiValueDict does not have append().
    #
    # Instead, put all images into MultiValueDict using setlist().
    # =============================================================

    def get_request(self, payload, images):

        factory = APIRequestFactory()

        multipart_data = {}

        for key, value in payload.items():
            multipart_data[key] = value

        # Multiple uploaded images
        multipart_data["images"] = images

        # Create multipart request
        django_request = factory.post(
            "/api/properties/",
            data=multipart_data,
            format="multipart"
        )

        # ---------------------------------------------------------
        # IMPORTANT
        #
        # APIView().initialize_request() creates a new DRF Request.
        # Since this test does not run authentication middleware,
        # DRF would otherwise make request.user AnonymousUser.
        # ---------------------------------------------------------

        request = APIView().initialize_request(
            django_request
        )

        # Force the DRF request to use the actual UserCreate object
        request._user = self.user
        request._request.user = self.user

        return request
    # =============================================================
    # CONTEXT
    # =============================================================

    def get_context(self, request):

        return {

            "request": request,

            "amenities_list": [
                3,
                5,
                6,
                12
            ],

            "selling_points_list": [
                "Riverview",
                "Roadside"
            ],

            "land_mark_list": [
                {
                    "name": "school",
                    "distance": "1km"
                }
            ],

            # EXACT
            "field_values": self.get_field_values(),

            # Same feature structure
            "features_list": self.get_field_values(),
        }

    # =============================================================
    # SERIALIZER HELPER
    # =============================================================

    def create_serializer(self, image_count=4):

        payload = self.get_payload()

        images = [
            self.create_image(i)
            for i in range(1, image_count + 1)
        ]

        request = self.get_request(
            payload,
            images
        )

        print("TEST FILES:", request.FILES.getlist("images"))
        print("TEST FILE COUNT:", len(request.FILES.getlist("images")))

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        return serializer, request

    # =============================================================
    # TEST 1
    # =============================================================

    def test_actual_property_payload_is_valid(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =============================================================
    # TEST 2
    # =============================================================

    def test_create_property_with_actual_payload(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        self.assertIsNotNone(
            property_obj
        )

        self.assertEqual(
            property_obj.user,
            self.user
        )

        self.assertEqual(
            property_obj.label,
            "Sell house"
        )

    
    # =============================================================
    # TEST 3
    # =============================================================

    def test_images_saved(self):

        serializer, request = (
            self.create_serializer(
                image_count=4
            )
        )

        # ---------------------------------------------------------
        # 1. Confirm exactly 4 images were uploaded
        # ---------------------------------------------------------

        uploaded_images = request.FILES.getlist(
            "images"
        )

        self.assertEqual(
            len(uploaded_images),
            4
        )

        # ---------------------------------------------------------
        # 2. Serializer must accept the uploaded images
        # ---------------------------------------------------------

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        # ---------------------------------------------------------
        # 3. Save the property
        # ---------------------------------------------------------

        property_obj = serializer.save()

        self.assertIsNotNone(
            property_obj
        )

        # ---------------------------------------------------------
        # 4. Confirm the property was created
        # ---------------------------------------------------------

        self.assertEqual(
            Property.objects.filter(
                id=property_obj.id
            ).count(),
            1
        )

        # ---------------------------------------------------------
        # 5. Confirm the uploaded image names are the expected ones
        # ---------------------------------------------------------

        uploaded_names = [
            image.name
            for image in uploaded_images
        ]

        self.assertEqual(
            uploaded_names,
            [
                "property_1.jpg",
                "property_2.jpg",
                "property_3.jpg",
                "property_4.jpg",
            ]
        )



    # =============================================================
    # TEST 4
    # =============================================================

    def test_amenities_saved(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        saved_ids = set(
            property_obj.amenities.values_list(
                "id",
                flat=True
            )
        )

        self.assertEqual(
            saved_ids,
            {
                3,
                5,
                6,
                12
            }
        )

    # =============================================================
    # TEST 5
    # =============================================================

    def test_field_values_are_saved(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        features = PropertyFeature.objects.filter(
            property=property_obj
        )

        self.assertEqual(
            features.count(),
            3
        )

        actual = []

        for feature in features:

            value = feature.value

            if isinstance(value, str):

                value = json.loads(value)

            actual.append(
                {
                    "name": feature.field.field_name,
                    "option": value.get("option"),
                    "value": value.get("value")
                }
            )

        self.assertIn(
            {
                "name": "BHK types",
                "option": None,
                "value": "4BHK"
            },
            actual
        )

        self.assertIn(
            {
                "name": "Flat Furnishing",
                "option": "Bed",
                "value": 1
            },
            actual
        )

        self.assertIn(
            {
                "name": "Flat Furnishing",
                "option": "Fan",
                "value": 1
            },
            actual
        )

    # =============================================================
    # TEST 6
    # =============================================================

    def test_selling_points_saved(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        self.assertEqual(
            property_obj.selling_points,
            [
                "Riverview",
                "Roadside"
            ]
        )

    # =============================================================
    # TEST 7
    # =============================================================

    def test_landmarks_saved(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        self.assertEqual(
            property_obj.land_mark,
            [
                {
                    "name": "school",
                    "distance": "1km"
                }
            ]
        )

    # =============================================================
    # TEST 8
    # =============================================================

    def test_features_output(self):

        serializer, request = self.create_serializer()

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        output = UserPropertySerializer(
            property_obj,
            context={
                "request": request
            }
        ).data

        print("\n================ FEATURE OUTPUT ================")
        print(json.dumps(
            output.get("features"),
            indent=4,
            default=str
        ))
        print("=================================================")

        features = output.get("features")

        self.assertIsNotNone(features)

        self.assertEqual(
            len(features),
            3
        )
    # =============================================================
    # TEST 9
    # =============================================================

    def test_amenities_output(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        output = UserPropertySerializer(
            property_obj,
            context={
                "request": request
            }
        ).data

        amenities = output.get(
            "amenities"
        )

        self.assertIsNotNone(
            amenities
        )

        self.assertEqual(
            len(amenities),
            4
        )

    # =============================================================
    # TEST 10
    # =============================================================

    def test_selling_points_output(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        output = UserPropertySerializer(
            property_obj,
            context={
                "request": request
            }
        ).data

        self.assertEqual(
            output["selling_points"],
            [
                "Riverview",
                "Roadside"
            ]
        )

    # =============================================================
    # TEST 11
    # =============================================================

    def test_landmarks_output(self):

        serializer, request = (
            self.create_serializer()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        property_obj = serializer.save()

        output = UserPropertySerializer(
            property_obj,
            context={
                "request": request
            }
        ).data

        self.assertEqual(
            output["landmarks"],
            [
                {
                    "name": "school",
                    "distance": "1km"
                }
            ]
        )

    # =============================================================
    # TEST 12
    # =============================================================

    def test_minimum_three_images(self):

        serializer, request = (
            self.create_serializer(
                image_count=2
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "images",
            serializer.errors
        )

    # =============================================================
    # TEST 13
    # =============================================================

    def test_maximum_ten_images(self):

        serializer, request = (
            self.create_serializer(
                image_count=11
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "images",
            serializer.errors
        )

    # =============================================================
    # TEST 14
    # =============================================================

    def test_sale_price_required(self):

        payload = self.get_payload()

        payload["price"] = ""

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =============================================================
    # TEST 15
    # =============================================================

    def test_sale_perprice_required(self):

        payload = self.get_payload()

        payload["perprice"] = ""

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "perprice",
            serializer.errors
        )

    # =============================================================
    # TEST 16
    # =============================================================

    def test_rent_price_required(self):

        payload = self.get_payload()

        payload["purpose"] = "Rent"
        payload["price"] = "."

        # Empty price
        payload["price"] = ""

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =============================================================
    # TEST 17
    # =============================================================

    def test_rent_deposit_required(self):

        payload = self.get_payload()

        payload["purpose"] = "Rent"
        payload["price"] = "25000"
        payload["deposit"] = ""

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "deposit",
            serializer.errors
        )

    # =============================================================
    # TEST 18
    # =============================================================

    def test_lease_price_required(self):

        payload = self.get_payload()

        payload["purpose"] = "Lease"
        payload["price"] = ""

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "price",
            serializer.errors
        )

    # =============================================================
    # TEST 19
    # =============================================================

    def test_invalid_subcategory(self):

        payload = self.get_payload()

        payload["subcategory"] = (
            "Invalid Apartment"
        )

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "subcategory",
            serializer.errors
        )

    # =============================================================
    # TEST 20
    # =============================================================

    def test_invalid_purpose(self):

        payload = self.get_payload()

        payload["purpose"] = (
            "Invalid Purpose"
        )

        images = [
            self.create_image(i)
            for i in range(1, 5)
        ]

        request = self.get_request(
            payload,
            images
        )

        serializer = UserPropertySerializer(
            data=request.data,
            context=self.get_context(request)
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "purpose",
            serializer.errors
        )



from django.test import TestCase

from agents.models import (
    AgentUserProfile,
    AgentContactMessage,
)

from users.serializers import (
    AgentContactMessageSerializer,
)


class AgentContactMessageSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        # =========================================================
        # CREATE TEST AGENT
        # =========================================================
        #
        # These fields are required by AgentUserProfile.save()
        # and full_clean().
        #
        cls.agent = AgentUserProfile.objects.create(
            username="testagent",
            email="agent@example.com",
            password="TestPassword123",
            phone_number="9876543210",
            address="Test Agent Address",
            pin_code="679307",
        )

    # =========================================================
    # HELPER
    # =========================================================

    def create_message(self):

        return AgentContactMessage.objects.create(
            agent=self.agent,
            name="John Customer",
            message="I am interested in this property.",
        )

    # =========================================================
    # VALID DATA
    # =========================================================

    def test_valid_data(self):

        data = {
            "name": "John Customer",
            "message": "I am interested in this property.",
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    # =========================================================
    # CREATE CONTACT MESSAGE
    # =========================================================

    def test_create_contact_message(self):

        data = {
            "name": "John Customer",
            "message": "I am interested in this property.",
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        message = AgentContactMessage.objects.create(
            agent=self.agent,
            name=serializer.validated_data["name"],
            message=serializer.validated_data["message"],
        )

        self.assertIsNotNone(
            message.id
        )

        self.assertEqual(
            message.agent,
            self.agent
        )

        self.assertEqual(
            message.name,
            "John Customer"
        )

        self.assertEqual(
            message.message,
            "I am interested in this property."
        )

    # =========================================================
    # SERIALIZED OUTPUT
    # =========================================================

    def test_serialized_output(self):

        message = self.create_message()

        serializer = AgentContactMessageSerializer(
            message
        )

        data = serializer.data

        # Main fields
        self.assertIn(
            "id",
            data
        )

        self.assertIn(
            "agent_id",
            data
        )

        self.assertIn(
            "agent_name",
            data
        )

        self.assertIn(
            "agent_email",
            data
        )

        self.assertIn(
            "agent_phone",
            data
        )

        self.assertIn(
            "agent_whatsapp",
            data
        )

        self.assertIn(
            "name",
            data
        )

        self.assertIn(
            "message",
            data
        )

        self.assertIn(
            "status",
            data
        )

        self.assertIn(
            "replied_at",
            data
        )

        self.assertIn(
            "created_at",
            data
        )

    # =========================================================
    # AGENT ID
    # =========================================================

    def test_agent_id_is_serialized(self):

        message = self.create_message()

        serializer = AgentContactMessageSerializer(
            message
        )

        data = serializer.data

        self.assertEqual(
            str(data["agent_id"]),
            str(self.agent.id)
        )

    # =========================================================
    # AGENT EMAIL
    # =========================================================

    def test_agent_email_is_serialized(self):

        message = self.create_message()

        serializer = AgentContactMessageSerializer(
            message
        )

        data = serializer.data

        self.assertEqual(
            data["agent_email"],
            self.agent.email
        )

    # =========================================================
    # READ ONLY FIELDS
    # =========================================================

    def test_read_only_fields_cannot_be_written(self):

        data = {
            "agent_id": str(self.agent.id),

            "agent_name": "Fake Agent",
            "agent_email": "fake@example.com",
            "agent_phone": "1111111111",
            "agent_whatsapp": "1111111111",

            "name": "John Customer",
            "message": "Test message",

            "status": "replied",

            "replied_at": "2026-09-16T10:00:00Z",

            "created_at": "2026-09-16T10:00:00Z",
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        validated_data = serializer.validated_data

        # These fields must not enter validated_data
        self.assertNotIn(
            "agent_id",
            validated_data
        )

        self.assertNotIn(
            "agent_name",
            validated_data
        )

        self.assertNotIn(
            "agent_email",
            validated_data
        )

        self.assertNotIn(
            "agent_phone",
            validated_data
        )

        self.assertNotIn(
            "agent_whatsapp",
            validated_data
        )

        self.assertNotIn(
            "status",
            validated_data
        )

        self.assertNotIn(
            "replied_at",
            validated_data
        )

        self.assertNotIn(
            "created_at",
            validated_data
        )

        # Writable fields should remain
        self.assertEqual(
            validated_data["name"],
            "John Customer"
        )

        self.assertEqual(
            validated_data["message"],
            "Test message"
        )

    # =========================================================
    # NAME REQUIRED
    # =========================================================

    def test_name_is_required(self):

        data = {
            "message": "I am interested."
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # =========================================================
    # MESSAGE REQUIRED
    # =========================================================

    def test_message_is_required(self):

        data = {
            "name": "John Customer"
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "message",
            serializer.errors
        )

    # =========================================================
    # EMPTY NAME
    # =========================================================

    def test_empty_name_is_invalid(self):

        data = {
            "name": "",
            "message": "I am interested.",
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors
        )

    # =========================================================
    # EMPTY MESSAGE
    # =========================================================

    def test_empty_message_is_invalid(self):

        data = {
            "name": "John Customer",
            "message": "",
        }

        serializer = AgentContactMessageSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "message",
            serializer.errors
        )

    # =========================================================
    # UPDATE MESSAGE
    # =========================================================

    def test_update_message(self):

        message = self.create_message()

        serializer = AgentContactMessageSerializer(
            message,
            data={
                "name": "Updated Customer",
                "message": "Updated message",
            },
            partial=True
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        updated_message = serializer.save()

        self.assertEqual(
            updated_message.name,
            "Updated Customer"
        )

        self.assertEqual(
            updated_message.message,
            "Updated message"
        )



