from django import forms
from .models import Personal

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = "__all__"
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            "cedula": {
                "unique": "Ya existe una persona registrada con esta cédula.",
            },
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        instance = self.instance  # Instancia actual

    # Verifica si ya existe otra persona con la misma cédula
        if Personal.objects.filter(cedula=cedula).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("Ya existe una persona registrada con esta cédula.")

        return cedula


