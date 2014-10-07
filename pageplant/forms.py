# -*- coding: utf-8 -*-

import datetime

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Submit,
                                 Div, HTML, Field)

from taggit.forms import TagField

from .models import Page
from .settings import PAGEPLANT_SETTINGS


class PageForm(forms.ModelForm):
    tags = TagField(
        label="Tags",
        required=False,
    )
    slug = forms.CharField(
        required=True,
        label='URL (uten spesialtegn og æøå)',
    )
    status = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect(), choices=Page.PAGE_STATUS_TYPES,
        initial='0'
    )
    language = forms.ChoiceField(
        label="Språk",
        required=True,
        choices=PAGEPLANT_SETTINGS['languages'],
        initial=PAGEPLANT_SETTINGS['default_language'],
    )
    meta_keywords = forms.CharField(
        label='Nøkkelord',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4})
    )
    meta_description = forms.CharField(
        label='Beskrivelse',
        required=False,
        widget=forms.Textarea(attrs={'rows': 6})
    )
    publish_at = forms.DateTimeField(
        label='Publiseringstidspunkt',
        input_formats=['%d/%m/%Y %H:%M'],
        initial=datetime.datetime.now,
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M')
    )

    def __init__(self, *args, **kwargs):
        Field.template = 'bootstrap/custom_field.html'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        # 2
                        Div(  # span7
                            Field(
                                'language'
                            ),
                            Field(
                                'header',
                                css_class="col-md-12 input-lg"
                            ),
                            Field(
                                'slug',
                            ),

                            Field(
                                'lead',
                                css_class="col-md-12",
                                style="height: 100px;"
                            ),
                            css_class='col-md-10'
                        ),
                        # Right column
                        Div(
                            Field('status',
                                  css_class=""),
                            css_class='col-md-2',
                        ),
                        css_class="row",
                    ),
                    Div(  # row
                        Div(  # md-12
                            Field(
                                'body',
                            ),
                            css_class="col-md-12",
                        ),
                        css_class="row",
                    ),
                    Div(  # row
                        Div(  # span7
                            Field(
                                'tags',
                            ),
                            css_class='col-md-10',
                        ),
                        Div(  # span2
                            Field(
                                'publish_at'
                            ),
                            css_class='col-md-2',
                        ),
                        css_class='row'
                    ),
                    css_class="panel-body",
                ),
                css_class='panel panel-default',  # 2
            )
        )
        self.helper.add_input(
            Submit('submit', 'Lagre', css_class="btn btn-primary"))

        super(PageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Page
        exclude = ('user',)
