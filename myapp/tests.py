from django.test import TestCase

# Create your tests here.
value = 1234
print(f'{value:,}')  # For Python ≥3.6
print(type(f'{value:,}'))
