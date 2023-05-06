from unicat.rest.views.IntegerChoicesView import IntegerChoiceView

from ..models.LearningFormat import LearningFormat


class LearningFormatView(IntegerChoiceView):
    integer_choices = LearningFormat
