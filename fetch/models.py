from django.db import models

# Create your models here.
class Candidate(models.Model):
    repo_id = models.BigIntegerField()
    repo_name = models.CharField(max_length=200)
    repo_url = models.CharField(max_length=200)
    keyword = models.CharField(max_length=100)
    description = models.TextField()