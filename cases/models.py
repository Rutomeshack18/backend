from django.db import models
from django.contrib.auth.models import AbstractUser


class Court(models.Model):
    court_name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False  # Prevent Django from managing this table
        db_table = 'courts'  # Use the existing table name

class CaseClassification(models.Model):
    case_class = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'case_classifications'  # Use the existing table name

class County(models.Model):
    county_name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'counties'  # Use the existing table name

class Action(models.Model):
    action_type = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'actions'  # Use the existing table name

class Citation(models.Model):
    citation_text = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'citations'  # Use the existing table name

class Judge(models.Model):
    judge_name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'judges'  # Use the existing table name

class Party(models.Model):
    party_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'parties'  # Use the existing table name

class Case(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    date_delivered = models.DateField(null=True)
    
    court = models.ForeignKey(Court, db_column='court_id', on_delete=models.CASCADE)
    case_classification = models.ForeignKey(CaseClassification, db_column='case_class_id', on_delete=models.CASCADE)
    action = models.ForeignKey(Action, db_column='action_id', on_delete=models.CASCADE)
    citation = models.ForeignKey(Citation, db_column='citation_id', on_delete=models.CASCADE)
    county = models.ForeignKey(County, db_column='county_id', on_delete=models.CASCADE)
    
    full_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'cases'

class CaseJudge(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'case_judges'  # Use the existing table name

class CaseParty(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'case_parties'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username