from django.db import models
from django.contrib.auth.models import User



class FileModel(models.Model):
    """
        Test model
    """
    # document = models.FileField(validators=[validate_file_infection])
    file = models.FileField(blank=True,null=True)

    def __str__(self):
        return str(self.id)


class ImgModel(models.Model):
    """
        Image model
    """
    file = models.ForeignKey(FileModel,on_delete=models.CASCADE)
    img = models.ImageField(upload_to ='uploads/',null=True,blank=True)

    def __str__(self):
        return str(self.id)