from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Todo
from .serializers import TodoSerializer
from devhub.pagination import StandardResultsSetPagination

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_todos(request):
    todos = Todo.objects.all()
    paginator = StandardResultsSetPagination()
    paginated_todos = paginator.paginate_queryset(todos, request)
    serializer = TodoSerializer(paginated_todos, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_todos(request):
    query = request.query_params.get('q', '')
    todos = Todo.objects.filter(title__icontains=query)
    paginator = StandardResultsSetPagination()
    paginated_todos = paginator.paginate_queryset(todos, request)
    serializer = TodoSerializer(paginated_todos, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def retrieve_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TodoSerializer(todo)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TodoSerializer(todo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_todos(request):
    ids = request.data.get('ids', [])
    todos = Todo.objects.filter(id__in=ids)
    deleted_ids = []
    for todo in todos:
        deleted_ids.append(todo.id)
        todo.delete()
    return Response({'deleted_ids': deleted_ids}, status=status.HTTP_204_NO_CONTENT)
