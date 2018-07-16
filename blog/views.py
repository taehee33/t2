# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm , ContactForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages

#import sample_to_data
import eval as ev


def box(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/box.html', {'box': box})




def story(request):

    qs = Post.objects.all()

    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    return render(request, 'blog/story.html', {
        'post_story' : qs,
        'q' : q,
    })

    #if request.method == "submit":
    #    return redirect('post_detail', {})
    #else:
    #    form = PostForm()
    #return render(request, 'blog/post_story.html', {})


    #return render(request, 'blog/post_story.html', {})
    #return HttpResponse("finish")

'''

@app.route('/',methods=['GET','POST'])
def find_word(predictions=None):
    form = ReusableForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        name=request.form['dataname']
        name=name.replace(" ","")
        print (form.validate())
        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ')
            print(name)
            noun_word=sample_to_data.sample_to_data(name)
            print(noun_word)
            noun_word=str(noun_word)
            predictions,prob= ev.eval(noun_word)
            prob=round(prob*100,2)
            print(prob)

            return render_template('index1.html',form=form, predictions=predictions,prob=prob)
        else:
            flash('Error: . 최소 4글자 이상 100글자 이하로 철제목을 입력하세요.')


    return render_template('index1.html',predictions=None,form=None,prob=None)

'''

'''
def fla(request):
    predictions = '준영구, ant c is working'
    prob = '80'

    #data['csrfmiddlewaretoken'] = '{ csrf_token }'

    #return render('post_fla.html' , predictions= 'sss',prob='80')
    return render(request, 'blog/fla.html', {'predictions' : None, 'prob': None})
'''


def fla(request):
    form = ContactForm(request.POST)

    print (form.errors)
    if request.method == 'POST':
        name=request.POST['dataname']
        name=name.replace(" ","")
        print (form.is_valid())
        if form.is_valid():

            # Save the comment here.
            messages.add_message(request, messages.INFO, 'Thanks for registration ')
            print(name)
            noun_word=sample_to_data.sample_to_data(name)
            print(noun_word)
            noun_word=str(noun_word)
            predictions,prob= ev.eval(noun_word)

            predictions = 'aaa'
            prob = '80'
            prob=round(prob*100,2)
            print(prob)

            return render(request, 'blog/fla.html', {'predictions' : None, 'prob': None})
        else:
            messages.add_message(request, messages.INFO, 'Error: . 최소 4글자 이상 100글자 이하로 철제목을 입력하세요.')


    return render(request, 'blog/fla.html', {'predictions' : None, 'prob': None})
'''


def fla(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "blog/fla.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')


    '''


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


#def publish(self):
#    self.published_date = timezone.now()
#    self.save()


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')





def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
