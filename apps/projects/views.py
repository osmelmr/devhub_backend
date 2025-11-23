from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Project
from .serializers import ProjectSerializer
from devhub.permissions import IsAdminUser
from devhub.pagination import StandardResultsSetPagination

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_projects(request):
    projects = Project.objects.all()
    paginator = StandardResultsSetPagination()
    paginated_projects = paginator.paginate_queryset(projects, request)
    serializer = ProjectSerializer(paginated_projects, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_own_projects(request):
    projects = Project.objects.filter(user=request.user)
    paginator = StandardResultsSetPagination()
    paginated_projects = paginator.paginate_queryset(projects, request)
    serializer = ProjectSerializer(paginated_projects, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_own_projects(request):
    query = request.query_params.get('q', '')
    projects = Project.objects.filter(user=request.user, title__icontains=query)
    paginator = StandardResultsSetPagination()
    paginated_projects = paginator.paginate_queryset(projects, request)
    serializer = ProjectSerializer(paginated_projects, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def retrieve_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        if project.user != request.user:
            return Response({'error': f'{project.title} is not your project'}, status=status.HTTP_403_FORBIDDEN)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def update_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        if project.user != request.user:
            return Response({'error': f'{project.title} is not your project'}, status=status.HTTP_403_FORBIDDEN)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def delete_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        if project.user != request.user:
            return Response({'error': f'{project.title} is not your project'}, status=status.HTTP_403_FORBIDDEN)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def delete_projects(request):
    ids = request.data.get('ids', [])
    projects = Project.objects.filter(id__in=ids)
    for project in projects:
        if project.user != request.user:
            return Response({'error': f'{project.title} is not your project'}, status=status.HTTP_403_FORBIDDEN)
        project.delete()
    return Response({'deleted_ids': ids}, status=status.HTTP_204_NO_CONTENT)
