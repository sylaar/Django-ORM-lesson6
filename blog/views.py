from django.db.models import Count, Prefetch
from django.shortcuts import render, get_object_or_404

from blog.models import Comment, Post, Tag


def serialize_post_optimized(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag_optimized(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag_optimized(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_with_tag,
    }


def index(request):

    most_popular_posts = Post.objects.popular() \
                                     .prefetch_and_annotate_post() \
                                     .fetch_with_comments_count()

    most_fresh_posts = Post.objects.order_by('-published_at') \
                                   .prefetch_and_annotate_post() \
                                   .fetch_with_comments_count() 
    

    most_popular_tags = Tag.objects.popular().annotate(posts_with_tag=Count('posts'))

    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts[:5]
        ],
        'page_posts': [serialize_post_optimized(post) for post in most_fresh_posts[:5]],
        'popular_tags': [serialize_tag_optimized(tag) for tag in most_popular_tags[:5]],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    posts = Post.objects.prefetch_related('likes', Prefetch(
                                            'tags',
                                            queryset=Tag.objects.annotate(
                                            posts_with_tag=Count('posts')
                                            )))
    post = get_object_or_404(posts, slug=slug)
    
    comments = Comment.objects.filter(post=post).select_related('author')
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes.count(),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag_optimized(tag) for tag in post.tags.all()],
    }

    most_popular_tags = Tag.objects.popular().annotate(posts_with_tag=Count('posts'))[:5]

    most_popular_posts = Post.objects.popular() \
                                     .prefetch_and_annotate_post() \
                                     .fetch_with_comments_count()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag_optimized(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts[:5]
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)

    most_popular_tags = Tag.objects.popular().annotate(posts_with_tag=Count('posts'))

    most_popular_posts = Post.objects.popular() \
                                     .prefetch_and_annotate_post() \
                                     .fetch_with_comments_count()

    related_posts = Post.objects.filter(tags=tag) \
                                     .prefetch_and_annotate_post() \
                                     .fetch_with_comments_count()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag_optimized(tag) for tag in most_popular_tags[:5]],
        'posts': [serialize_post_optimized(post) for post in related_posts[:20]],
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts[:5]
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
