from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Profile, Log,Menu, PointRequest, PointRequest_Image,Notification,Promotion,Reward,ClaimedReward
# Register your models here.

class ProfileResource(resources.ModelResource):
    class Meta:
        model=Profile
        fields=('userid','name', 'status', 'points', 'created_at')

class ProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('userid','name', 'status', 'points', 'created_at')
    search_fields = ('name__username', 'status')
    resource_class=ProfileResource

    def userid(self,obj):
        return obj.name.id
    userid.short_description = 'User ID'

class LogAdmin(admin.ModelAdmin):
    list_display = ('userid','account', 'action', 'date', 'time')
    search_fields = ('account__name__username', 'action')
    list_filter = ('action', 'date')

    def userid(self, obj):
        return obj.account.name.id
    userid.short_description = 'User ID'

class MenuResource(resources.ModelResource):
    class Meta:
        model=Menu
        fields=('image','name', 'description', 'price')

class MenuAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name','description', 'price')
    resource_class=MenuResource

class PointResource(resources.ModelResource):
    class Meta:
        model=PointRequest
        fields =('account','points_requested','date_requested','status')

class PointRequestAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('account', 'points_requested', 'date_requested', 'status')
    search_fields = ('account__name__username', 'status')
    list_filter = ('status', 'date_requested')
    resource_class=PointResource

    def save_model(self, request, obj, form, change):

        message=""

        if change:
            old_obj = PointRequest.objects.get(pk=obj.pk)
            if old_obj.status != 'approved' and obj.status == 'approved':
                profile=obj.account
                profile.points += obj.points_requested
                if profile.points > 1000 and profile.status !='diamond':
                    profile.status = 'diamond'
                    message="Ur profile has upgraded to Diamond"
                profile.save()

        Notification.objects.create(
            account=obj.account,
            message=f"Your point request for {obj.points_requested} points has been {obj.status}.{message}"
        )

        super().save_model(request, obj, form, change)

class PointRequestImageAdmin(admin.ModelAdmin):
    list_display = ('request', 'image')
    search_fields = ('request__account__name__username',)

class NotificationAdmin(admin.ModelAdmin):
    list_display=('account','message','created_at')

class PromotionAdmin(admin.ModelAdmin):
    list_display=['name','description','audience','created_at','expired_date']

    def save_model(self,request,obj,form,change):

        user_message=f"New Promotion! {obj.name}"

        if not change:
            if obj.audience == "everyone":
                users=Profile.objects.all()
            elif obj.audience == "diamond":
                users=Profile.objects.filter(status="diamond")

            for user in users:
                create=Notification.objects.create(
                    account=user,
                    message=user_message
                )
                create.save()
                
        super().save_model(request,obj,form,change)

class RewardAdmin(admin.ModelAdmin):
    list_display=['name','points_required','description']

class ClaimedRewardResource(resources.ModelResource):
    class Meta:
        model=ClaimedReward
        fields=('profile','reward','claimed_at')

class ClaimedRewardAdmin(ImportExportModelAdmin):
    list_display=['profile','reward','claimed_at']
    resource_class=ClaimedRewardResource

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(PointRequest, PointRequestAdmin)
admin.site.register(PointRequest_Image, PointRequestImageAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Promotion,PromotionAdmin)
admin.site.register(Reward,RewardAdmin)
admin.site.register(ClaimedReward,ClaimedRewardAdmin)