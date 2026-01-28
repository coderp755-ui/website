from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer

# REGISTER NEW USER (Role-based creation)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    current_user = request.user
    requested_role = request.data.get('role')
    
    # Role-based permission checks
    if current_user.role == 'super':
        # Super admin can create country and branch admins
        if requested_role not in ['country', 'branch']:
            return Response(
                {"detail": "Super admin can only create country or branch admins"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    elif current_user.role == 'country':
        # Country admin can only create branch admins within their country
        if requested_role != 'branch':
            return Response(
                {"detail": "Country admin can only create branch admins"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        # Ensure the branch belongs to the country admin's country
        branch_id = request.data.get('branch')
        if branch_id:
            from apps.locations.models import Branch
            try:
                branch = Branch.objects.get(id=branch_id)
                if branch.country != current_user.country:
                    return Response(
                        {"detail": "You can only create users for branches in your country"}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Branch.DoesNotExist:
                return Response(
                    {"detail": "Invalid branch"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Set the country for branch admin to be same as country admin
        request.data['country'] = current_user.country.id if current_user.country else None
    else:
        # Branch admin cannot create users
        return Response(
            {"detail": "You don't have permission to create users"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user:
        # Return basic info, JWT token can be added later
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "country": user.country.code if user.country else None,
            "branch": user.branch.slug if user.branch else None,
        }, status=status.HTTP_200_OK)
    return Response(
        {"detail": "Invalid credentials"}, 
        status=status.HTTP_401_UNAUTHORIZED
    )

# GET USER LIST (Role-based filtering)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    current_user = request.user
    
    if current_user.role == 'super':
        # Super admin can see all users
        users = User.objects.all()
    elif current_user.role == 'country':
        # Country admin can see branch admins in their country
        users = User.objects.filter(
            role='branch',
            country=current_user.country
        )
    else:
        # Branch admin cannot list users
        return Response(
            {"detail": "You don't have permission to list users"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# GET CURRENT USER INFO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# UPDATE USER (Role-based)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    current_user = request.user
    
    try:
        user_to_update = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"detail": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Permission checks
    if current_user.role == 'super':
        # Super admin can update country and branch admins
        if user_to_update.role not in ['country', 'branch']:
            return Response(
                {"detail": "Cannot update this user"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    elif current_user.role == 'country':
        # Country admin can only update branch admins in their country
        if (user_to_update.role != 'branch' or 
            user_to_update.country != current_user.country):
            return Response(
                {"detail": "You can only update branch admins in your country"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        # Branch admin can only update themselves
        if user_to_update != current_user:
            return Response(
                {"detail": "You can only update your own profile"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = UserSerializer(user_to_update, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE USER (Role-based)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    current_user = request.user
    
    try:
        user_to_delete = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"detail": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Permission checks
    if current_user.role == 'super':
        # Super admin can delete country and branch admins
        if user_to_delete.role not in ['country', 'branch']:
            return Response(
                {"detail": "Cannot delete this user"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    elif current_user.role == 'country':
        # Country admin can only delete branch admins in their country
        if (user_to_delete.role != 'branch' or 
            user_to_delete.country != current_user.country):
            return Response(
                {"detail": "You can only delete branch admins in your country"}, 
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        # Branch admin cannot delete users
        return Response(
            {"detail": "You don't have permission to delete users"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_to_delete.delete()
    return Response(
        {"detail": "User deleted successfully"}, 
        status=status.HTTP_204_NO_CONTENT
    )