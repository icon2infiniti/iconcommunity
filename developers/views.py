from django.shortcuts import render
from .models import Tutorial, MiniCard
from el_pagination.decorators import page_template


@page_template('developers/blog_tutorial_page.html', key='blog_tutorial_page')
@page_template('developers/video_tutorial_page.html', key='video_tutorial_page')
def developers(request, template='developers/developers.html', extra_context=None):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = True
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    context = {
        'blog_tutorials': Tutorial.objects.filter(tutorial_category="Blog").order_by('-tutorial_date'),
        'video_tutorials': Tutorial.objects.filter(tutorial_category="Video").order_by('-tutorial_date'),
        'reward_calculators': MiniCard.objects.filter(minicard_category="Reward Calculator").order_by('-minicard_date'),
        'scores': MiniCard.objects.filter(minicard_category="SCORE").order_by('-minicard_date'),
        'wallets': MiniCard.objects.filter(minicard_category="Wallet").order_by('-minicard_date'),
        'dbs': MiniCard.objects.filter(minicard_category="Database").order_by('-minicard_date'),
        'ides': MiniCard.objects.filter(minicard_category="IDE").order_by('-minicard_date'),
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'DEVELOPERS',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
