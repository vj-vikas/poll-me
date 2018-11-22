from django import forms
from .models import Poll,choice

class PollForm(forms.ModelForm):

	choice1 = forms.CharField(
							label = 'First choice',
							max_length= '100',
							min_length= '3',
							widget = forms.TextInput(attrs={'class':'form-control'}))
	choice2 = forms.CharField(
							label = 'Second choice',
							max_length= '100',
							min_length= '3',
							widget = forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Poll
		fields =['text','choice1','choice2'] 
		widgets = {
					'text':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20})
		}


class EditPollForm(forms.ModelForm):
	"""docstring for EditPollForm"""
	class Meta:
		model = Poll
		fields = ['text']
		widgets = {
				'text':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20})
		}

class ChoiceForm(forms.ModelForm):
	
	class Meta:
		model = choice
		fields =['choice_text'] 
		widgets = {
					'choice_text':forms.Textarea(attrs={'class':'form-control','rows':5,'cols':20})
		}

		