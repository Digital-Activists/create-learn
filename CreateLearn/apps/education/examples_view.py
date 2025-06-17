from django.views.generic import ListView, TemplateView


class CourseDetailExample(TemplateView):
    template_name = "examples/cart.html"


class MyCoursesStudentExample(TemplateView):
    template_name = "examples/my_courses_stud.html"


class RatingExample(TemplateView):
    template_name = "examples/rating.html"
