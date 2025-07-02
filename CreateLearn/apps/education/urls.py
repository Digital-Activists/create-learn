from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .courses.view_sets import (
    CourseViewSet,
    FlashCardsDeckViewSet,
    FlashCardViewSet,
    LessonPageViewSet,
    LessonViewSet,
    ModuleViewSet,
    PageAttachmentViewSet,
)
from .examples_view import RatingExample, MyCoursesStudentExample, CourseDetailExample
from .views import (
    AddStudentsAPIView,
    ConstructorCoursesView,
    CourseDetailView,
    CourseEnrollView,
    CoursesListView,
    CreateCourseView,
    CreateModuleView,
    CreateLessonView,
    LessonDetailView,
    LessonsListView,
    TeacherCreateQuiz,
    TeacherCreateTasks,
    TeacherSettingsCourse,
    UsersPerCourseView,
    about_us,
    index,
    StudentRatingPerCourseView,
    StudentMyCoursesView,
    MyCoursesRedirect,
)


router = DefaultRouter()
router.register(r"lessons", LessonViewSet)
router.register(r"flash-cards", FlashCardViewSet)
router.register(r"flash-cards-decks", FlashCardsDeckViewSet)
router.register(r"lesson-pages", LessonPageViewSet)
router.register(r"page-attachments", PageAttachmentViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"modules", ModuleViewSet)

examples = [
    path("course-card", CourseDetailExample.as_view()),
    path("my-courses", MyCoursesStudentExample.as_view()),
    path("rating", RatingExample.as_view()),
]

constructor = [
    path("", RedirectView.as_view(pattern_name="teacher_my_courses")),
    path("my-courses", ConstructorCoursesView.as_view(), name="teacher_my_courses"),
    path("create", CreateCourseView.as_view(), name="teach_course_create"),
    path("<slug:slug>/new-module", CreateModuleView.as_view(), name="teach_create_module"),
    path(
        "<slug:slug>/module/<int:module>/new-lesson",
        CreateLessonView.as_view(),
        name="teach_create_lesson",
    ),
    path(
        "<slug:slug>/module/<int:module>/lesson/<int:lesson>",
        TeacherCreateTasks.as_view(),
        name="teach_create_tasks",
    ),
    path("<slug:slug>/setting", TeacherSettingsCourse.as_view(), name="teach_setting_course"),
    path("students", UsersPerCourseView.as_view(), name="users_per_course"),
    path(
        "<slug:slug>/module/<int:module>/lesson/<int:lesson>/quiz",
        TeacherCreateQuiz.as_view(),
        name="card_teach",
    ),
]

courses = [
    path("", CoursesListView.as_view(), name="education_courses"),
    path("<slug:slug>", CourseDetailView.as_view(), name="course_details"),
    path("<slug:slug>/enroll", CourseEnrollView.as_view(), name="enroll_course"),
    path("<slug:slug>/lessons", LessonsListView.as_view(), name="course_lessons"),
    path(
        "<slug:slug>/module/<int:module>/lesson/<int:lesson>",
        LessonDetailView.as_view(),
        name="lesson_details",
    ),
]

students = [
    path("my-courses", StudentMyCoursesView.as_view(), name="student_my_courses"),
    path("my-rating", StudentRatingPerCourseView.as_view(), name="student_my_rating"),
]

urlpatterns = [
    path("", index, name="home"),
    path("my-courses", MyCoursesRedirect.as_view(), name="my_courses"),
    path("api/", include(router.urls)),
    path("api/add-delete-students/", AddStudentsAPIView.as_view(), name="api_add_delete_students"),
    path("about_us", about_us, name="education_about_us"),
    path("courses/", include(courses)),
    path("student/", include(students)),
    path("examples/", include(examples)),
    path("constructor/", include(constructor)),
]
