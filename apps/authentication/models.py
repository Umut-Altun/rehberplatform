from django.db import models
from django.contrib.auth.models import User
import random

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_verification_code(self):
        self.verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()
        return self.verification_code
