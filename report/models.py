from django.db import models
from django.conf import settings
from django.utils import timezone

GENDER_CHOICES = (
    ('1', '女性'),
    ('2', '男性'),
)
NUM_CHOICES = (
  ('1', 1),
  ('2', 2),
  ('3', 3),
  ('4', 4),
  ('5', 5)
)

class Profile(models.Model):
  name = models.CharField("ハンドルネーム", max_length=255)
  phone = models.CharField("電話番号", max_length=255, blank=True)
  gender = models.CharField("性別", max_length=2, choices=GENDER_CHOICES, blank=True)
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

  def __str__(self):
    return self.name

class Department(models.Model):
  name = models.CharField('部署名', max_length=20)
  created_at = models.DateTimeField('日付',default=timezone.now)

  def __str__(self):
    return self.name

class Position(models.Model):
  name = models.CharField('役職', max_length=20)
  order = models.CharField('順位',max_length=1, choices=NUM_CHOICES)
  created_at = models.DateTimeField('日付', default=timezone.now)

  def __str__(self):
    return self.name

class Employee(models.Model):
  department = models.ForeignKey(
    Department, verbose_name='部署', related_name="em_department", on_delete=models.PROTECT
  )
  position = models.ForeignKey(
    Position, verbose_name='役職', related_name="em_position", on_delete=models.PROTECT
  )
  created_at = models.DateTimeField('日付', default=timezone.now)
  user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="em_user", on_delete=models.PROTECT)
  
  def __str__(self):
    return '{0} {1} {2}'.format(self.user, self.position, self.department)

