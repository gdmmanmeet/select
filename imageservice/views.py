from django.http.response import HttpResponse, Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import utils


class ImageService(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, filename):
        if not filename:
            return self.list(request)
        content, content_type = utils.get_image(filename, request.user.id)
        if not content:
            raise Http404
        resp = HttpResponse(content, content_type=content_type)
        resp['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return resp

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('file')
        if not utils.is_valid_image(image_file):
            raise ValidationError("Invalid file.")
        image_path = utils.get_image_path(image_file.name, request.user.id)
        if utils.image_exists(image_path):
            raise ValidationError("Image already exist with same name.")
        utils.save_image(image_file, image_path)
        return Response("success")

    def patch(self, request, filename):
        image_file = request.FILES.get('file')
        if not utils.is_valid_image(image_file):
            raise ValidationError("Invalid file.")
        image_path = utils.get_image_path(filename, request.user.id)
        if not utils.image_exists(image_path):
            raise ValidationError("No image to update")
        utils.save_image(image_file, image_path)
        return Response(image_file.name)

    def delete(self, request, filename):
        image_path = utils.get_image_path(filename, request.user.id)
        if not utils.image_exists(image_path):
            raise ValidationError("Image does not exist.")
        utils.delete_image(filename, request.user.id)
        return Response("success")

    def list(self, request):
        return Response(utils.get_user_images(request.user.id))


class RegenerateAuthToken(APIView):
    
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Delete old token
        Token.objects.filter(user=user).delete()

        # create new token
        token = Token.objects.create(user=user)
        utils.create_user_image_dir(user.id)
        return Response({'token': token.key})
