from django.shortcuts import render
from .models import BlogTutorial, VideoTutorial, VideoPresentation
from el_pagination.decorators import page_template


@page_template('developers/blog_tutorial_page.html', key='blog_tutorial_page')
@page_template('developers/video_tutorial_page.html', key='video_tutorial_page')
def developers(request, template='developers/developers.html', extra_context=None):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = False
    if 'navbar' not in request.session:
        request.session['navbar'] = True

    video_tutorials = VideoTutorial.objects.all().order_by('-video_tutorial_date')
    for url in video_tutorials:
        url.video_tutorial_link = url.video_tutorial_link.replace("watch?v=", "embed/")+"?rel=0"

    video_presentations = VideoPresentation.objects.all().order_by('-video_presentation_date')
    for url in video_presentations:
        url.video_presentation_link = url.video_presentation_link.replace("watch?v=", "embed/")+"?rel=0"

    context = {
        'blog_tutorials': BlogTutorial.objects.all().order_by('-blog_tutorial_date'),
        'video_tutorials': video_tutorials,
        'video_presentations': video_presentations,
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'section': 'DEVELOPERS',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
