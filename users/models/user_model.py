from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self',
                                       through='Connection',
                                       related_name='followers',
                                       symmetrical=False,
                                       verbose_name='подписки')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return '{} ({})'.format(self.username, self.email)


class Connection(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='rel_from_set',
                                  verbose_name='подписчик')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='rel_to_set',
                                verbose_name='автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_from', 'user_to'],
                                    name='unique_follow')]
        ordering = ('-created',)
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def clean(self, *args, **kwargs):
        if self.user_to == self.user_from:
            raise ValidationError('На себя подписываться нельзя!')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} следит за {}'.format(self.user_from, self.user_to)
