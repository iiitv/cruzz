# Django
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Django
from authentication.serializers import RegistrationSerializer, LoginSerializer, UserUpdateSerializer
from authentication.renderers import UserJSONRenderer


def land(request):
    return render(request, 'home.html')


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
            'first_name': user_data.get('first_name', None),
            'last_name': user_data.get('last_name', None),
            'city': user_data.get('city', None),
            'state': user_data.get('state', None),
            'country': user_data.get('country', None),
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'is_staff': user_data.get('is_staff', None),
            'is_superuser': user_data.get('is_staff', None),
            'bio': user_data.get('bio', request.user.profile.bio or None),
            'image': user_data.get('image', request.user.profile.image or None)
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
