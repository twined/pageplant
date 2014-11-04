# -*- coding: utf-8 -*-

import datetime

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from crispy_forms.layout import Div
from crispy_forms.layout import HTML
from crispy_forms.layout import Field

from taggit.forms import TagField
from cerebrum.fields import SlugField

from .models import BasePage
from .settings import PAGEPLANT_SETTINGS


class BasePageForm(forms.ModelForm):
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
        widget=forms.RadioSelect(), choices=BasePage.PAGE_STATUS_TYPES,
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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                # 2
                Div(  # span7
                    Field('is_partial'),
                    Field('identifier'),
                    Field(
                        'language'
                    ),
                    Field(
                        'header',
                        css_class="col-md-12 input-lg"
                    ),
                    SlugField(
                        'slug',
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
                Div(
                    HTML(  # md-12
                        '<button class="btn btn-small btn-error" type="button" id="toggleTemplateLock"><i class="fa fa-lock"> </i> L&aring;s opp mal</button>',
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
        )
        self.helper.add_input(
            Submit('submit', 'Lagre', css_class="btn btn-primary"))

        super(BasePageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BasePage
        exclude = ('user',)


class BaseTreePageForm(BasePageForm):
    def __init__(self, *args, **kwargs):
        super(BaseTreePageForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(
            0,
            Div(  # md-12
                Field(
                    'parent',
                    css_class="selectpicker",
                ),
                css_class="col-md-6 row",
            ),
        )

    class Meta:
        model = BasePage
        exclude = ('user',)
