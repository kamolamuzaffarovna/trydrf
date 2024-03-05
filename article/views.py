from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer, ArticlePostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadonly


@api_view(['GET'])
def article_list_view(request):
    qs = Article.objects.all()
    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q)
    serializer = ArticleSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def article_detail_view(request, pk):
    obj = get_object_or_404(Article, id=pk)
    serializer = ArticleSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([BasicAuthentication])
def article_created_view(request):
    context = {
        'user_id': request.user.id
    }
    serializer = ArticleSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    data = {
        'success': False,
        'message': 'Something gets wrong',
        'detail': serializer.errors
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def article_list_create_api_view(request):
    if request.method == "POST":
        context = {
            'user_id': request.user.id
        }
        serializer = ArticlePostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            obj = get_object_or_404(Article, pk=serializer.data.get('id'))
            success_serializer = ArticleSerializer(obj)
            return Response(success_serializer.data, status=status.HTTP_201_CREATED)
        data = {
            'success': False,
            'message': "Xatolik bor",
            'detail': "Xatolikni toping"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    qs = Article.objects.all()
    serializer = ArticleSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_article_list_view(request):
    user = request.user
    article = Article.objects.filter(author_id=user.id)
    serializer = ArticleSerializer(article, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsOwnerOrReadonly])
def article_update_view(request, pk):
    obj = get_object_or_404(Article, id=pk)
    data = request.data
    partial = False
    if request.method == 'PATCH':
        partial = True
    serializer = ArticleSerializer(data=data, instance=obj, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadonly])
def article_delete_view(request, pk):
    obj = get_object_or_404(Article, id=pk)
    obj.delete()
    return Response({"success": True, "message": "Article deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadonly])
def article_rud_view(request, pk):
    obj = get_object_or_404(Article, id=pk)
    if request.method == 'GET':
        qs = Article.objects.all()
        serializer = ArticleSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        obj = get_object_or_404(Article, id=pk)
        obj.delete()
        return Response({"success": True, "message": "Article deleted"}, status=status.HTTP_204_NO_CONTENT)
    else:
        data = request.data
        partial = False
        if request.method == 'PATCH':
            partial = True
        serializer = ArticleSerializer(data=data, instance=obj, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
