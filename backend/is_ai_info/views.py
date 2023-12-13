from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from .models import Group, Educator, Question, Student, QuestionReply, SubjectInSchedule
from .serializers import StudentSerializer, GroupSerializer, EducatorSerializer, UserSerializer, \
    SubjectInScheduleSerializer, QuestionSerializer, QuestionReplySerializer, StudentSerializerCreateUpdate, \
    SubjectInScheduleSerializerCreateUpdate, EducatorSerializerCreateUpdate, QuestionReplySerializerCreateUpdate, \
    QuestionSerializerCreateUpdate, SubjectInScheduleSerializerForList, QuestionReplySerializerForList


class AdminViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = EducatorSerializer
    #permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False)
    def new_educator(self, request):
        username = request.data.pop('username')
        password = request.data.pop('password')
        with transaction.atomic():
            data = request.data
            user = User.objects.create(username=username, password=password)
            data['user'] = user.pk
            serializer = EducatorSerializerCreateUpdate(data=data)
            serializer.is_valid(raise_exception=True)
            educator = serializer.save()
        return Response(EducatorSerializer(educator).data)

    @action(methods=['post'], detail=True)
    def new_subject_in_schedule(self, request, pk=None):
        educator = get_object_or_404(Educator, pk=pk)
        data = request.data
        data['educator'] = educator.pk
        serializer = SubjectInScheduleSerializerCreateUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        return Response(SubjectInScheduleSerializer(subject).data)

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
        with transaction.atomic():
            user = User.objects.create(username=username, password=password)
            data = request.data
            data['user'] = user.pk
            data['group'] = group.pk
            serializer = StudentSerializerCreateUpdate(data=data)
            serializer.is_valid(raise_exception=True)
            student = serializer.save()
        return Response(StudentSerializer(student).data)


class StudentViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    #permission_classes = [IsAuthenticated]


class EducatorViewSet(ReadOnlyModelViewSet):
    queryset = Educator.objects.all()
    serializer_class = EducatorSerializer
    #permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = self.get_serializer(instance).data
        response['schedule'] = SubjectInScheduleSerializerForList(
            SubjectInSchedule.objects.filter(educator=instance).order_by('-even_week', 'day', 'from_to'), many=True
        ).data
        return Response(response)


class ForumViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['question_from'] = Student.objects.get(user=request.user).pk
        serializer = QuestionSerializerCreateUpdate(data=data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return Response(QuestionSerializer(question).data, status=201)

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(question)
        response = serializer.data
        response['replies'] = QuestionReplySerializerForList(
            QuestionReply.objects.filter(question=question).order_by('-reply_datetime'), many=True).data
        return Response(response)

    @action(methods=['post'], detail=True)
    def reply(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        data = request.data
        data['question'] = question.pk
        user = request.user
        if Educator.objects.filter(user=user).count() > 0:
            data['author_educator'] = Educator.objects.get(user=user).pk
        else:
            data['author_student'] = Student.objects.get(user=user).pk
        serializer = QuestionReplySerializerCreateUpdate(data=data)
        serializer.is_valid(raise_exception=True)
        reply = serializer.save()
        return Response(QuestionReplySerializer(reply).data)
