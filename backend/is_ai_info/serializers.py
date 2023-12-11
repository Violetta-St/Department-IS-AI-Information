from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Group, Student, Educator, Subject, SubjectInSchedule, Question, QuestionReply


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class EducatorSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Educator
        fields = '__all__'


class SubjectSerializer(ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class SubjectInScheduleSerializer(ModelSerializer):
    educator = EducatorSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = SubjectInSchedule
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    question_from = StudentSerializer()
    question_to = EducatorSerializer()

    class Meta:
        model = Question
        fields = '__all__'


class QuestionReplySerializer(ModelSerializer):
    author_educator = EducatorSerializer()
    author_student = StudentSerializer()
    question = QuestionSerializer()

    class Meta:
        model = QuestionReply
        fields = '__all__'
