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
from .views import (
    AddStudentsAPIView,
    ConstructorCoursesView,
    CourseDetailExample,
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
)

router = DefaultRouter()
router.register(r"lessons", LessonViewSet)
router.register(r"flash-cards", FlashCardViewSet)
router.register(r"flash-cards-decks", FlashCardsDeckViewSet)
router.register(r"lesson-pages", LessonPageViewSet)
router.register(r"page-attachments", PageAttachmentViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"modules", ModuleViewSet)

urlpatterns = [
    path("", index, name="home"),
    path("api/", include(router.urls)),
    path("api/add-delete-students/", AddStudentsAPIView.as_view(), name="api_add_delete_students"),
    path("about_us", about_us, name="education_about_us"),
    # Examples
    path("examples/course-card", CourseDetailExample.as_view(), name="course_details"),
    # Courses
    path("courses", CoursesListView.as_view(), name="education_courses"),
    path("courses/<slug:slug>", CourseDetailView.as_view(), name="course_details"),
    path("courses/<slug:slug>/enroll", CourseEnrollView.as_view(), name="enroll_course"),
    path(
        "courses/<slug:slug>/lessons",
        LessonsListView.as_view(),
        name="course_lessons",
    ),
    path(
        "courses/<slug:slug>/module/<int:module>/lesson/<int:lesson>",
        LessonDetailView.as_view(),
        name="lesson_details",
    ),
    # Constructor
    path("constructor", RedirectView.as_view(pattern_name="my_courses")),
    path("constructor/my-courses", ConstructorCoursesView.as_view(), name="my_courses"),
    path("constructor/create", CreateCourseView.as_view(), name="teach_course_create"),
    path(
        "constructor/<slug:slug>/new-module",
        CreateModuleView.as_view(),
        name="teach_create_module",
    ),
    path(
        "constructor/<slug:slug>/module/<int:module>/new-lesson",
        CreateLessonView.as_view(),
        name="teach_create_lesson",
    ),
    path(
        "constructor/<slug:slug>/module/<int:module>/lesson/<int:lesson>",
        TeacherCreateTasks.as_view(),
        name="teach_create_tasks",
    ),
    path(
        "constructor/<slug:slug>/setting",
        TeacherSettingsCourse.as_view(),
        name="teach_setting_course",
    ),
    path("constructor/students", UsersPerCourseView.as_view(), name="users_per_course"),
    path(
        "constructor/<slug:slug>/module/<int:module>/lesson/<int:lesson>/quiz",
        TeacherCreateQuiz.as_view(),
        name="card_teach",
    ),
]
