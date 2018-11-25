from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from .models import choice,Poll
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import PollForm,EditPollForm,ChoiceForm
import datetime


# Create your views here.
@login_required
def polls_list(request):
	
	polls = Poll.objects.all()
	context = {
				'polls':polls

				}
	return render(request,'polls/polls_list.html',context)

@login_required
def add_poll(request):
	if request.method == 'POST':
		form = PollForm(request.POST)
		if form.is_valid():
			new_poll = form.save(commit=False)
			new_poll.pub_date = datetime.datetime.now()
			new_poll.owner = request.user
			new_poll.save()
			new_choice1 = choice(
								poll = new_poll,
								choice_text = form.cleaned_data['choice1']								
							).save()
			new_choice2 = choice(
								poll = new_poll,
								choice_text = form.cleaned_data['choice2']								
							).save()
			messages.success(request,'poll and choices added',extra_tags='alert alert-success')
			return redirect('polls:list')

	else:
		form = PollForm()
	
	context = {'form':form}
	return render(request,'polls/add_poll.html',context)

@login_required
def edit_poll(request,poll_id):
	poll = get_object_or_404(Poll,id=poll_id)
	if request.user != poll.owner:
		return redirect('/')
		
	if request.method == "POST":
		form = EditPollForm(request.POST,instance=poll)
		if form.is_valid():
			form.save()
			messages.success(request,'poll edited',extra_tags='alert alert-success')
			return redirect('polls:list')
	else:
		form = EditPollForm(instance=poll)

	return render(request,'polls/edit_poll.html',{'form':form,'poll':poll})
	
@login_required
def poll_detail(request,poll_id):
	#poll= Poll.objects.get(id=poll_id)
	poll=get_object_or_404(Poll,id= poll_id)

	context={'poll':poll}
	return render(request,'polls/poll_detail.html',context)

@login_required
def poll_vote(request,poll_id):
	poll=get_object_or_404(Poll,id= poll_id)
	choice_id = request.POST.get('Choice')
	if choice_id:
		Choice = choice.objects.get(id=choice_id)
		Choice.votes += 1
		Choice.save()

	else:
		messages.error(request,'no choice found')
		return HttpResponseRedirect(reverse("polls:detail",args=(poll_id,)))
	
	return render(request,'polls/poll_results.html',{'poll':poll})
	
@login_required
def add_choice(request,poll_id):
	poll = get_object_or_404(Poll,id=poll_id)
	if request.user != poll.owner:
		return redirect('/')

	if request.method == "POST":
		form = ChoiceForm(request.POST)
		if form.is_valid:
			new_choice = form.save(commit=False)
			new_choice.poll = poll
			new_choice.save()
			messages.success(request,'choice added successfully',extra_tags='alert alert-success')
			return redirect('polls:list')
	else:
		form = ChoiceForm()
	return render(request,'polls/add_choice.html',{'form':form})

def edit_choice(request,choice_id):
	Choice = get_object_or_404(choice,id=choice_id)
	poll = get_object_or_404(Poll,id=Choice.poll.id)
	if request.user != poll.owner:
		return redirect('/')

	if request.method == "POST":
		form = ChoiceForm(request.POST)
		if form.is_valid:
			form.save()
			messages.success(request,'choice edited successfully',extra_tags='alert alert-success')
			return redirect('polls:list')
	else:
		form = ChoiceForm(instance=Choice)
	return render(request,'polls/add_choice.html',{'form':form,'edit_mode':True,'Choice':Choice})

@login_required
def delete_choice(request,choice_id):
	Choice = get_object_or_404(choice,id=choice_id)
	poll = get_object_or_404(Poll,id=Choice.poll.id)
	if request.user != poll.owner:
		return redirect('/')

	if request.method == "POST":
		Choice.delete()
		messages.success(request,'choice delelted',
			extra_tags='alert alert-success ')
		return redirect('polls:list')

	return render(request,'polls/delete_choice_confirm.html',{'Choice':Choice})

@login_required
def delete_poll(request,poll_id):
	poll=get_object_or_404(Poll,id=poll_id)
	if request.user != poll.owner:
		return redirect('/')

	if request.method=='POST':
		poll.delete()
		messages.success(request,'Poll is delelted successfully',
						extra_tags='alert alert-success')
		return redirect('polls:list')

	return render(request,'polls/delete_poll_confirm.html',{'poll':poll})
	