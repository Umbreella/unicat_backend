from unicat.rest.views.IntegerChoicesView import IntegerChoiceView

from ..models.LessonTypeChoices import LessonTypeChoices


class LessonTypeView(IntegerChoiceView):
    integer_choices = LessonTypeChoices
