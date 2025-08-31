"""
Test file for user registration functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .validators import PersianPasswordValidator
from .serializers import UserSerializer

User = get_user_model()

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'bio': 'Test bio'
        }

    def test_password_validator(self):
        """Test password validation rules"""
        validator = PersianPasswordValidator()
        
        # Test valid password
        try:
            validator.validate('TestPass123!')
        except ValidationError:
            self.fail("Valid password should not raise ValidationError")
        
        # Test short password
        with self.assertRaises(ValidationError):
            validator.validate('Test1!')
        
        # Test password without uppercase
        with self.assertRaises(ValidationError):
            validator.validate('testpass123!')
        
        # Test password without lowercase
        with self.assertRaises(ValidationError):
            validator.validate('TESTPASS123!')
        
        # Test password without digit
        with self.assertRaises(ValidationError):
            validator.validate('TestPass!')
        
        # Test password without special character
        with self.assertRaises(ValidationError):
            validator.validate('TestPass123')

    def test_user_serializer_validation(self):
        """Test user serializer validation"""
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid())
        
        # Test duplicate username
        user = User.objects.create_user(
            username='testuser',
            email='another@example.com',
            password='TestPass123!'
        )
        
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        
        # Test duplicate email
        user.delete()
        user = User.objects.create_user(
            username='anotheruser',
            email='test@example.com',
            password='TestPass123!'
        )
        
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        
        # Test password mismatch
        user.delete()
        invalid_data = self.valid_user_data.copy()
        invalid_data['password_confirm'] = 'DifferentPass123!'
        
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_user_creation(self):
        """Test user creation with email verification"""
        serializer = UserSerializer(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        
        # Check that user is created but not active
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_email_verified)
        self.assertIsNotNone(user.email_verification_token)
        
        # Check that password is hashed
        self.assertNotEqual(user.password, self.valid_user_data['password'])

if __name__ == '__main__':
    import django
    django.setup()
    
    # Run tests
    test = UserRegistrationTest()
    test.setUp()
    
    print("Testing password validator...")
    test.test_password_validator()
    print("✓ Password validator tests passed")
    
    print("Testing user serializer validation...")
    test.test_user_serializer_validation()
    print("✓ User serializer validation tests passed")
    
    print("Testing user creation...")
    test.test_user_creation()
    print("✓ User creation tests passed")
    
    print("\nAll tests passed! ✅") 