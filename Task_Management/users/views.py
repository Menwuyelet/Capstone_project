from rest_framework import generics, status
from .serialiazers import UserSerializer,UpdateProfileAndPasswordSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    #queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            print("Error During Logout:", str(e))
            return Response({"detail": str(e)}, status=400)
        
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateProfileAndPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UpdateProfileAndPasswordSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # This will handle both profile and password update
            return Response({'message': 'Profile and password updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        user = request.user
        serializer = UpdateProfileAndPasswordSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # This will handle both profile and password update
            return Response({'message': 'Profile and password updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)