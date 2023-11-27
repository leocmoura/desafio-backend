from django.db import models
from users.models import CustomUser
from movies.models import Movie

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message