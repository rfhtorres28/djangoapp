from rest_framework import serializers
from .models import ElecsQuestions, ElecsOptions, CommsQuestions, CommsOptions, MathQuestions, MathOptions, GEASQuestions, GEASOptions


class ElecsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElecsOptions
        fields = ['question_no_id', 'letter', 'content', 'is_correct']



class ElecsQuestionsSerializer(serializers.ModelSerializer):
    options = ElecsOptionsSerializer(many=True)

    class Meta:
        model = ElecsQuestions
        fields = ['id', 'content', 'options']



class CommsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommsOptions
        fields = ['question_no_id', 'letter', 'content', 'is_correct']



class CommsQuestionsSerializer(serializers.ModelSerializer):
    options = CommsOptionsSerializer(many=True)

    class Meta:
        model = CommsQuestions
        fields = ['id', 'content', 'options']




class MathOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathOptions
        fields = ['question_no_id', 'letter', 'content', 'is_correct']



class MathQuestionsSerializer(serializers.ModelSerializer):
    options = MathOptionsSerializer(many=True)

    class Meta:
        model = MathQuestions
        fields = ['id', 'content', 'options']



class GEASOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GEASOptions
        fields = ['question_no_id', 'letter', 'content', 'is_correct']



class GEASQuestionsSerializer(serializers.ModelSerializer):
    options = GEASOptionsSerializer(many=True)

    class Meta:
        model = GEASQuestions
        fields = ['id', 'content', 'options']