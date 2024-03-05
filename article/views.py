from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer, ArticlePostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def article_list_view(request):
    qs = Article.objects.all()
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
        serializer = ArticlePostSerializer(data=request.data)
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
