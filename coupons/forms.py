from django import forms


class FileImportForm(forms.Form):
    excel_file = forms.FileField()
