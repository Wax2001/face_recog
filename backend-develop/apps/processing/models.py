from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
import datetime

# Create your models here.

class User(AbstractUser):
    role = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(
        default=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    available = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '0. Пользователи'

    def __str__(self) -> str:
        return str(self.id)

    def user_images(self):
        if self.images.exists():
            return ([a.img.url for a in self.images.filter(available=True)])
        return ([])

    def user_image(self):
        try:
            return self.images.first().img
        except:
            return None

    def user_working_hours(self):
        try:
            return {
                'start_time': self.working_hours.start_time,
                'break_time_start': self.working_hours.break_time_start,
                'break_time_end': self.working_hours.break_time_end,
                'end_time': self.working_hours.end_time,
            }
        except:
            return None

    def user_salary(self):
        try:
            return {
                'hourly_rate': self.salary.hourly_rate,
                'allowance': self.salary.allowance,
            }
        except:
            return None

class WorkingHours(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='working_hours',
        null=True
    )
    start_time = models.TimeField(
        null=True
    )
    end_time = models.TimeField(
        null=True
    )
    break_time_start = models.TimeField(
        blank=True,
        null=True
    )
    break_time_end = models.TimeField(
        blank=True,
        null=True
    )
    available = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = 'Рабочий график'
        verbose_name_plural = '2. Рабочие графики'

    def __str__(self) -> str:
        return str(self.id)

class Salary(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='salary',
        null=True
    )
    total_work_hours = models.FloatField(
        default=0,
        help_text='in hours'
    )
    hourly_rate = models.FloatField(
        default=1,
        help_text='В долларах $'
    )
    allowance = models.FloatField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Надбавка в процентах 1-100%'
    )
    available = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = 'Заработная плата'
        verbose_name_plural = '3. Заработные платы'

    def __str__(self) -> str:
        return str(self.id)

class Image(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
        null=True
    )
    img = models.ImageField(
        upload_to=f'core/user_photos/'
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    available = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = '1. Изображения'

    def __str__(self) -> str:
        return str(self.id)

class Record(models.Model):
    user = models.ForeignKey(
        User,
        related_name='records',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    user_occurences = models.IntegerField(
        default=0,
        null=True,
        validators=[MinValueValidator(0)]
    )
    check_in_time = models.DateTimeField(
        blank=True,
        null=True
    )
    check_out_time = models.DateTimeField(
        blank=True,
        null=True
    )
    late_arrive_time = models.DateTimeField(
        blank=True,
        null=True
    )
    early_leave_time = models.DateTimeField(
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    obj_created_date = models.DateField(
        auto_now_add=True
    )
    completed = models.BooleanField(
        default=False
    )
    available = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = '4. Записи'

    def __str__(self) -> str:
        return str(self.id)

    def get_in_time(self):
        try:
            return self.check_in_time.time()
        except:
            return None

    def get_out_time(self):
        try:
            return self.check_out_time.time()
        except:
            return None

    def get_late_arrive_time(self):
        try:
            if self.user.working_hours.start_time > self.check_in_time.time():
                d_start = datetime.datetime.combine(
                    datetime.date.today(), 
                    self.check_in_time.time()
                    )
                d_end = datetime.datetime.combine(
                    datetime.date.today(), 
                    self.user.working_hours.start_time
                    )
                return d_end - d_start
        except:
            return None

    def get_early_leave_time(self):
        try:
            if self.user.working_hours.end_time > self.check_out_time.time():
                d_start = datetime.datetime.combine(
                    datetime.date.today(), 
                    self.check_out_time.time()
                    )
                d_end = datetime.datetime.combine(
                    datetime.date.today(), 
                    self.user.working_hours.end_time
                    )
                return d_end - d_start
        except:
            return None
