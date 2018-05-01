from django import forms

class Registerkey(forms.Form):
    name=forms.CharField(max_length=50,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'name',
            }
        ))
    email=forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'email',
            }
        ))
    key=forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'key',
            }
        ))

class Loginform(forms.Form):
    email=forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'email',
            }
        ))
    key=forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'key',
            }
        ))

class Postone(forms.Form):
    image=forms.FileField()

class Deleteone(forms.Form):
    name=forms.CharField(max_length=100,widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'image name',
            }
        ))

class Updateone(forms.Form):
    image=forms.FileField()

class Getlist(forms.Form):
    key=forms.CharField(max_length=100, widget=forms.TextInput(
            attrs={
                'class':'input100',
                'placeholder':'id',
            }
        ))

class Getone(forms.Form):
    key=forms.CharField(max_length=100)
    image=forms.CharField(max_length=100)

class Forgotkey(forms.Form):
    email=forms.CharField(max_length=100)