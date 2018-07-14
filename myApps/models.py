# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NewsArticle(models.Model):
    type = models.ForeignKey('NewsType', models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    publish_time = models.DateTimeField(db_column='Publish_time', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    from_host = models.CharField(max_length=128, blank=True, null=True)
    read_total = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'News_article'


class NewsLiked(models.Model):
    news = models.ForeignKey(NewsArticle, models.DO_NOTHING, db_column='News_id', blank=True, null=True)  # Field name made lowercase.
    use = models.ForeignKey('User', models.DO_NOTHING, db_column='Use_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'News_liked'


class NewsType(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'News_type'


class Permission(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Permission'


class Review(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    use = models.ForeignKey('User',  db_column='Use_id', blank=True, null=False, on_delete=models.CASCADE)  # Field name made lowercase.
    news = models.ForeignKey(NewsArticle, db_column='News_id',  blank=True, null=False, on_delete=models.CASCADE)  # Field name made lowercase.
    rev_content = models.CharField(db_column='Rev_content', max_length=256, blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='create_time', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Review'


class ReviewLiked(models.Model):
    r_liked_id = models.AutoField(db_column='R_liked_id', primary_key=True)  # Field name made lowercase.
    r_id = models.ForeignKey(Review, db_column='ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    use = models.ForeignKey('User', db_column='Use_id', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    is_liked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Review_liked'


class Role(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    role = models.ManyToManyField(Permission, through='RolePerRel')

    class Meta:
        managed = False
        db_table = 'Role'


class RolePerRel(models.Model):
    per = models.ForeignKey(Permission, models.DO_NOTHING, db_column='Per_id', primary_key=True)  # Field name made lowercase.
    role = models.ForeignKey(Role, models.DO_NOTHING, db_column='Role_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Role_Per_Rel'
        unique_together = (('per', 'role'),)


class User(models.Model):
    rol = models.ForeignKey(Role, models.DO_NOTHING, db_column='Rol_id', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    last_login_time = models.DateTimeField(db_column='Last_login_time', blank=True, null=True)  # Field name made lowercase.
    nick_name = models.CharField(max_length=32, blank=True, null=True)
    head_icon = models.CharField(max_length=256, blank=True, null=True)
    follow_type = models.ManyToManyField(NewsType, through='UserFollowRel')

    class Meta:
        managed = False
        db_table = 'User'


class UserFollowRel(models.Model):
    id = models.ForeignKey(NewsType, models.DO_NOTHING, db_column='id', primary_key=True)
    use = models.ForeignKey(User, models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Follow_Rel'
        unique_together = (('id', 'use'),)
