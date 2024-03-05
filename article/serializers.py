from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'date_joined']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'image', 'content', 'created_date']

    def validate(self, attrs):
        title = attrs.get('title')
        content = attrs.get('content')
        exps = {}
        if not title[0].isupper():
            exps['title'] = []
            exps['title'].append("title ni katta harf bilan yozing")
        if not content[0].isupper():
            exps['content'] = "content ni katta harf bilan yozing"
        # if self.Meta.model.objects.filter(title=title).exists():
        #     exps['title'].append("bunday title avval qo'shilgan")
        if exps:
            raise ValidationError(exps)
        return attrs

    def create(self, validated_data):
        user_id = self.context['user_id']
        validated_data['author_id'] = user_id
        return super().create(validated_data)


class ArticlePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'image', 'content', 'created_date']