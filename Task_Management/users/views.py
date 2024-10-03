from rest_framework import generics, status
from .serialiazers import UserSerializer,UpdateProfileAndPasswordSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny] # to allow any user to sign up 
    serializer_class = UserSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        try:
            refresh_token = request.data["refresh"] # fetch the refresh token of the user 
            token = RefreshToken(refresh_token)
            token.blacklist() # bloks the token 
            return Response(status=204) # to send no content status after loging out
        
        except Exception as e: # if the token provided is not valid it raises 400 bad request
            print("Error During Logout:", str(e))
            return Response({"detail": str(e)}, status=400)
        
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user # assignes the user to current user
        user.delete()
        return Response(status=204) # to send no content status after deleting the account
    
class UpdateProfileAndPasswordView(generics.UpdateAPIView): # used generics.updateAPIView to allow bothe put and patch methods to be used to call this view
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileAndPasswordSerializer

    def get_object(self):
        return self.request.user # gets the user instance of the current user for updating