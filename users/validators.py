from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class PersianPasswordValidator:
    """
    Custom password validator with Persian error messages
    """
    
    def validate(self, password, user=None):
        errors = []
        
        # Check minimum length
        if len(password) < 8:
            errors.append('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append('رمز عبور باید حداقل یک حرف کوچک داشته باشد.')
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            errors.append('رمز عبور باید حداقل یک عدد داشته باشد.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('رمز عبور باید حداقل یک کاراکتر خاص (!@#$%^&*(),.?":{}|<>) داشته باشد.')
        
        # Check for common patterns
        if re.search(r'(.)\1{2,}', password):
            errors.append('رمز عبور نباید شامل کاراکترهای تکراری متوالی باشد.')
        
        # Check for common patterns (only exact matches)
        common_patterns = ['password', 'admin', 'user', '123456', 'qwerty']
        password_lower = password.lower()
        for pattern in common_patterns:
            if pattern in password_lower:
                errors.append('رمز عبور نباید شامل الگوهای ساده باشد.')
                break
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return _(
            "رمز عبور شما باید:\n"
            "• حداقل ۸ کاراکتر باشد\n"
            "• حداقل یک حرف بزرگ داشته باشد\n"
            "• حداقل یک حرف کوچک داشته باشد\n"
            "• حداقل یک عدد داشته باشد\n"
            "• حداقل یک کاراکتر خاص داشته باشد\n"
            "• شامل کاراکترهای تکراری متوالی نباشد\n"
            "• شامل الگوهای ساده نباشد"
        ) 