# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import IntegrityError

from django import conf as authentication_conf

class UserProfile(models.Model):
    """
    Model for extended information of User at django.contrib.auth
    """

    # One to one references to User Model
    user = models.OneToOneField(User)
    # Activation toke for email verification
    activation_token = models.CharField(max_length=40, blank=True)
    # Expiration date for activation token
    expiration = models.DateTimeField(blank=True, null=True)
    # Profile description
    profile = models.TextField()
    # Slug
    slug = models.SlugField()
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.user.username)
        successful_save = False
        saved_object = None
        while not successful_save:
            try:
                saved_object = super(UserProfile, self).save(force_insert, force_update, using, update_fields)
                successful_save = True
            except IntegrityError:
                    self.slug = self.slug[:-4] + "-" + generate_random_string(4)
        return saved_object

    def __unicode__(self):
        return unicode(self.user)

def generate_random_string(n):
    """
    Generates a random string of length n
    :param n: Length of string
    :return: Random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for a in range(n))