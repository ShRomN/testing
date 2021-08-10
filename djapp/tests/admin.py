from django.contrib import admin

# Register your models here.
from .models import InformationTestUser
from .models import KettellQuestion, KettellAnswer
from .models import MMPIQuestion, MMPIAnswer
from .models import SCLQuestion, SCLAnswer
from .models import TSafetyQuestion, TSafetyAnswer
from .models import RPMQuestion, RPMAnswer
from .models import ComAnalogQuestion, ComAnalogAnswer


admin.site.register(InformationTestUser)
admin.site.register(KettellQuestion)
admin.site.register(KettellAnswer)
admin.site.register(MMPIQuestion)
admin.site.register(MMPIAnswer)
admin.site.register(SCLQuestion)
admin.site.register(SCLAnswer)
admin.site.register(TSafetyQuestion)
admin.site.register(TSafetyAnswer)
admin.site.register(RPMQuestion)
admin.site.register(RPMAnswer)
admin.site.register(ComAnalogQuestion)
admin.site.register(ComAnalogAnswer)