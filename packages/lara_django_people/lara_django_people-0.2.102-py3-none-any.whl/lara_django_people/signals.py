from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress


from .models import LaraUser, Entity, EntityRole, EntityClass, Group

# @receiver(post_save, sender=LaraUser)       
# def user_postsave_disa(sender, instance, created, **kwargs):
#     lara_user = instance
    
    # add profile if user is created
    # if created:
    #     entity = Entity.objects.get_or_create(
    #         name_full = lara_user.username,
    #         entity_class = EntityClass.objects.get(name='person'),
    #         # entity_role = EntityRole.objects.get(name='User'),
            
    #     )
    # else:
    #     pass
        # # update allauth emailaddress if exists 
        # try:
        #     email_address = EmailAddress.objects.get_primary(user)
        #     if email_address.email != user.email:
        #         email_address.email = user.email
        #         email_address.verified = False
        #         email_address.save()
        # except:
        #     # if allauth emailaddress doesn't exist create one
        #     EmailAddress.objects.create(
        #         user = user,
        #         email = user.email, 
        #         primary = True,
        #         verified = False
        #     )
