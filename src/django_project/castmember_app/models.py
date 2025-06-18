from uuid import uuid4
from django.db import models

class CastMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)

    class Meta:
        db_table = "cast_member"

        def __str__(self):
            return f"{self.name} - {self.type}"