from rest_framework.exceptions import ValidationError
from datetime import date


def validate_age(birthday):
    if birthday is None:
        raise ValidationError('Enter your birthday before posting')
    
    try:
        birthday = date.fromisoformat(birthday)
    except ValueError:
        raise ValidationError("Некорректный формат даты рождения")
    
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) > (birthday.month, birthday.day))
    if age < 18:
        raise ValidationError('You must be 18 to create a product')
    return birthday
