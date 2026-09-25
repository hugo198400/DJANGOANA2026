from django import forms

from .models import Actividad


class ActividadForm(forms.ModelForm):

    class Meta:
        model = Actividad

        fields = [
            "fase",
            "nombre",
            "control",
            "baselegal",
            "descripcion",
            "responsable",
            "fecha_inicio",
            "fecha_fin",
            "porcentaje_avance",
            "estado",
            "observaciones",
            "orden",
            "link",
        ]

        widgets = {
            "fase": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la actividad",
                }
            ),

            "control": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "baselegal": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Base legal / documento / numeral",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "responsable": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "fecha_inicio": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "fecha_fin": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "porcentaje_avance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                }
            ),

            "estado": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones...",
                }
            ),

            "orden": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enlace relacionado (opcional)",
                }),
        }

    def __init__(self, *args, proyecto=None, **kwargs):
        super().__init__(*args, **kwargs)

        if proyecto is not None:
            self.instance.proyecto = proyecto

        self.fields["fase"].queryset = self.fields[
            "fase"
        ].queryset.filter(activo=True)

        self.fields["responsable"].queryset = self.fields[
            "responsable"
        ].queryset.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser posterior "
                "a la fecha de fin."
            )

        return cleaned_data