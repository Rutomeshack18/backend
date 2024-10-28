from django.contrib import admin
from .models import Court, CaseClassification, County, Action, Citation, Judge, Party, Case, CaseJudge, CaseParty

admin.site.register(Court)
admin.site.register(CaseClassification)
admin.site.register(County)
admin.site.register(Action)
admin.site.register(Citation)
admin.site.register(Judge)
admin.site.register(Party)
admin.site.register(Case)
admin.site.register(CaseJudge)
admin.site.register(CaseParty)
