from urllib import request

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from app.forms import LessonCreateForm, StudentCreateForm, StudentCreateFromCSVForm
from app.library.etl.in_memory_file_csv import InMemoryStudentCSVHandler
from app.models import Lesson, Payment, Student, TeachingRoom, Tutor
from app.utils.calendar import get_lessons_to_display
from app.utils.reports import (
    get_lessons_today_and_tomorrow,
    get_money_per_week,
    get_student_missing_payment,
    get_students_missing_payments,
    get_total_student_missing_payment,
)


class TutorProfileView(LoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request):
        context = {
            "money_weekly": get_money_per_week(request.user.tutor.lesson_set.all()),
            "students_missing_payments": get_students_missing_payments(
                request.user.tutor.student_set.all()
            ),
            "incoming_lessons_today_and_tomorrow": get_lessons_today_and_tomorrow(
                request.user.tutor.lesson_set
            ),
        }

        return render(request, self.template_name, context)


class TutorReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Tutor
    template_name = "reminder.html"
    fields = [
        "send_reminder_hours_before",
        "send_reminders_to_yourself",
        "send_reminders_to_students",
        "message_template_to_yourself",
        "message_template_to_students",
    ]


class StudentCreateView(LoginRequiredMixin, CreateView):
    template_name = "student_create_form.html"
    form_class = StudentCreateForm

    def get_queryset(self):
        return super().get_queryset().filter(tutor=request.user.tutor)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(StudentCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs["tutor"] = self.request.user.tutor
        return kwargs


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = "student_create_form.html"
    form_class = StudentCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(StudentUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs["tutor"] = self.request.user.tutor
        return kwargs


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = "/students"
    template_name = "student_confirm_delete.html"


class StudentCreateFromCSVView(LoginRequiredMixin, View):
    form_class = StudentCreateFromCSVForm
    template_name = "student_create_from_csv_form.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            handler = InMemoryStudentCSVHandler(
                csv_file=request.FILES["csv_with_students"],
                model_in_csv=Student,
                uploader_model=request.user.tutor,
                msg_fail="{} already exists in data base.",
                msg_success="{} added to database successfully.",
            )
            handler.etl()
            log = handler.log
            return render(
                request, self.template_name, {"form": self.form_class(), "log": log}
            )

        return render(request, self.template_name, {"form": form})


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "student_detail.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            lessons=self.object.lesson_set.all(),
            payments=get_student_missing_payment(self.object.payment_set.all()),
            total_missing_payment=get_total_student_missing_payment(
                self.object.payment_set
            ),
        )


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "student_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(tutor=self.request.user.tutor)


class LessonCreateView(LoginRequiredMixin, CreateView):
    template_name = "lesson_create_form.html"
    form_class = LessonCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LessonCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs["tutor"] = self.request.user.tutor
        kwargs["student"] = Student.objects.filter(tutor=self.request.user.tutor)
        return kwargs


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lesson_create_form.html"
    form_class = LessonCreateForm
    model = Lesson

    def get_queryset(self):
        return super().get_queryset().filter(tutor=request.user.tutor)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LessonUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs["tutor"] = self.request.user.tutor
        return kwargs


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson_detail.html"


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "lesson_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(tutor=self.request.user.tutor)

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = object_list if object_list else self.object_list
        return super(LessonListView, self).get_context_data(
            object_list=object_list,
            lessons_this_week=get_lessons_to_display(object_list, week="current"),
            lessons_next_week=get_lessons_to_display(object_list, week="next"),
        )


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


@login_required
def change_payment_status(request):
    payment = Payment.objects.get(pk=int(request.POST.get("id_payment")))
    payment.change_status_to_paid()
    payment.save()
    return redirect(request.POST.get("redirect_back_path"))


def lesson_room(request, room_code):
    if room_code == "demo":
        return render(
            request,
            "lesson_room.html",
            {
                "room_name": room_code,
                "username": "student",
                "is_lessons_paid": False,
            },
        )

    teaching_room = TeachingRoom.objects.filter(url=room_code).first()
    if teaching_room:
        # from teaching room we can get all info we want to customize experience of a lesson
        # print(teaching_room.lesson.student.first_name)

        lesson = teaching_room.lesson

        if request.user.is_authenticated:
            username = request.user.username + "_tutor"
        else:
            username = lesson.student.first_name

        return render(
            request,
            "lesson_room.html",
            {
                "room_name": room_code,
                "username": username,
                "lesson": lesson,
                "is_lesson_paid": True,
            },
        )

    return redirect("home")
