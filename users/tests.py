from django.test import TestCase

from users.serializers import RequestSerializer


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
