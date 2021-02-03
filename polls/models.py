from django.db import models

class AdminLogs(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    cmd = models.ForeignKey('CmdTypes', models.DO_NOTHING)
    cmd_text = models.TextField(blank=True, null=True)

class CmdTypes(models.Model):
    cmd_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

class Groups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

class Polls(models.Model):
    poll_title = models.TextField()
    poll_start = models.IntegerField()
    poll_end = models.IntegerField()
    poll_description = models.TextField(blank=True, null=True)
    poll_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    
class QuestionTypes(models.Model):
    question_type = models.IntegerField(primary_key=True)
    name = models.TextField()

class Questions(models.Model):
    poll = models.ForeignKey(Polls, models.DO_NOTHING)
    question_id = models.AutoField(primary_key=True)
    question_type = models.ForeignKey(QuestionTypes, models.DO_NOTHING, db_column='question_type')
    question_title = models.TextField()
    question_choices = models.TextField(blank=True, null=True)

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    nickname = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Groups, models.DO_NOTHING)

class Usersanswers(models.Model):
    user_answer = models.TextField()
    user = models.ForeignKey(Users, models.DO_NOTHING)
    poll = models.ForeignKey(Polls, models.DO_NOTHING)
    timestamp = models.IntegerField()