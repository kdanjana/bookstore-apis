As much as I understand, There are two ways to handle permissions in APIView class
Statically assign a proper Permission classes to APIView.permission_classes (like extend BasePermission)
Dynamically decide Permission instances in APIView (override APIView.get_permission())
APIView checks permissions returned from .get_permission().
And .get_permission() instantiates Permissions from .permission_classes.
In my situation, Only I needed a predefined Permission but depending on method. So I chose latter approach.



The create() and update() methods(defined in serialiers) define how fully fledged (model)instances are 
created or modified when calling serializer.save()
create() and update() are inherent when u use ModelSerializer



book = serializers.StringRelatedField(many=True, read_only=True, source='books')------>
will give the def__str__(): mentioned in the book model, 'books' is the related name linking book model with author model


serializers.py
bookslist = serializers.SerializerMethodField()
def get_bookslist(self, obj):
        qs = Book.objects.filter(author=obj)
        return BookModSerializer(qs, many=True).data





TOken authentication:::
in django projects settings.py::
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
and INSTALLED_APPS : [......., 'rest_framework.authtoken', ]
we installed new app rest_framework.authtoken and then do python manage.py migrate,
we do this because the newly installed app wil create a new table in our db called token in which token is stored
token in created when user is logging in and the token is deleted as soon as user is loggedout.

Token Authentcation::
generating tokens:::
1.by using signals
use this when u want to generate token when user is registered
if u want every user to have an automatically generated Token, u can simply catch the User's post_save signal.
If you've already created some users, you can generate tokens for all existing users like this:
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
for user in User.objects.all():
    Token.objects.get_or_create(user=user)
2. By exposing an api endpoint
When using TokenAuthentication, you may want to provide a mechanism for clients to obtain a token given the
username and password. REST framework provides a built-in view to provide this behaviour. To use it, add the
obtain_auth_token view to your URLconf:
3. With Django admin
4. Using Django manage.py command




filtering-----3 types ------ filter, search, order content
easy implementation of filtering is by using  get_queryset()
generic filtering -- installing pkg - pip install django-filter
                                        INSTALLED_APPS = [
                                                       ...
                                                        'django_filters',
                                         ]
 You should now either add the filter backend to your settings:
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
Or add the filter backend to an individual View or ViewSet.
from django_filters.rest_framework import DjangoFilterBackend
class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]                                   

django_filter only works on genercis i.e filter,search,order work only on generics APIView

filterset_fields ---> filtering / searching based on exact given params

search_fields -----> searching, no need to be exact