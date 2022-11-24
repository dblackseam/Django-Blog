from rest_framework import serializers
from blog.models import Article
from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import Article, Category, Comment

User = get_user_model()

class ArticleListSerializer(serializers.ModelSerializer):
    """ ModelSerializer благодаря классу мета позволяет задать поля сериализатора в fields на основании понятное дело
    модели, без необходимости задавать их вручную.
    Т.е. если представить что класса Meta нет, выглядело бы это так:
     slug = SlugField()
     title = CharField()
     Image = ImageField()
     id = SmallIntegerField()"""
    class Meta:
        model = Article
        fields = ["slug", "id", "title", "image"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'updated')


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count')


class FullArticleSerializer(ArticleSerializer):

    comments = CommentSerializer(source='comment_set', many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + (
            'content',
            'comments',
        )
