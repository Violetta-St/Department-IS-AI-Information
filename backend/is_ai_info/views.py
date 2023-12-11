from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from .models import Group, Educator, Question, Student, QuestionReply
from .serializers import StudentSerializer, GroupSerializer, EducatorSerializer, UserSerializer, \
    SubjectInScheduleSerializer, QuestionSerializer, QuestionReplySerializer


class AdminViewSet(GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False)
    def new_educator(self, request):
        username = request.data.pop('username')
        password = request.data.pop('password')
        serializer = EducatorSerializer(request.data)
        with transaction.atomic():
            user = User.objects.create(username=username, password=password)
            serializer.user = UserSerializer(user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def new_subject_in_schedule(self, request, pk=None):
        educator = get_object_or_404(Educator, pk=pk)
        serializer = SubjectInScheduleSerializer(data=request.data)
        serializer.educator = EducatorSerializer(educator)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def new_group(self, request):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def new_student(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        username = request.data.pop('username')
        password = request.data.pop('password')
        serializer = StudentSerializer(data=request.data)
        serializer.group = GroupSerializer(group)
        with transaction.atomic():
            user = User.objects.create(username=username, password=password)
            serializer.user = UserSerializer(user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class StudentViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class EducatorViewSet(ReadOnlyModelViewSet):
    queryset = Educator.objects.all()
    serializer_class = EducatorSerializer
    permission_classes = [IsAuthenticated]


class ForumViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(question)
        response = serializer.data
        response['replies'] = QuestionReply.objects.filter(question).order_by('-reply_datetime')
        return Response(response)

    @action(methods=['post'], detail=True)
    def reply(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionReplySerializer(data=request.data)
        user = request.user
        if Educator.objects.filter(user=user) > 0:
            serializer.author_educator = EducatorSerializer(Educator.objects.get(user=user))
        else:
            serializer.author_student = StudentSerializer(Student.objects.get(user=user))
        serializer.question = QuestionSerializer(question)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
