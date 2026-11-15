from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Article, Category, Comment

def news_list(request):
    articles = Article.objects.filter(is_published=True).order_by('-created_at', '-id')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')

    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )

    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, slug=None):
    if slug:
        article = get_object_or_404(Article, slug=slug, is_published=True)
    else:
        # Fallback to the latest article if no slug provided
        article = Article.objects.filter(is_published=True).first()

    if article:
        # Increment views
        Article.objects.filter(pk=article.pk).update(views_count=article.views_count + 1)
        related_articles = Article.objects.filter(is_published=True, category=article.category).exclude(pk=article.pk)[:3]
        comments = article.comments.filter(is_approved=True, parent__isnull=True).prefetch_related('replies')
        total_comments_count = article.comments.filter(is_approved=True).count()
    else:
        related_articles = []
        comments = []
        total_comments_count = 0

    if request.method == 'POST' and article:
        name = request.POST.get('name', '').strip()
        if not name:
            name = 'Anonymous'
        content = request.POST.get('comment', '').strip() or request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')
        reply_to_name = request.POST.get('reply_to_name', '').strip()

        parent = None
        if parent_id:
            parent = Comment.objects.filter(id=parent_id, article=article).first()
            if not reply_to_name and parent:
                reply_to_name = parent.name or 'Anonymous'

        if content:
            Comment.objects.create(
                article=article,
                parent=parent,
                reply_to_name=reply_to_name,
                name=name,
                email='',
                content=content,
            )
            return redirect('news_detail', slug=article.slug)

    context = {
        'article': article,
        'related_articles': related_articles,
        'comments': comments,
        'total_comments_count': total_comments_count,
    }
    return render(request, 'news/news_detail.html', context)
