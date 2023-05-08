from unicat.rest.views.IntegerChoicesView import IntegerChoiceView

from ..models.QuestionTypeChoices import QuestionTypeChoices


class QuestionTypeView(IntegerChoiceView):
    integer_choices = QuestionTypeChoices
