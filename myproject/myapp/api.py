from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ElecsQuestionsSerializer, ElecsOptionsSerializer, CommsQuestionsSerializer, CommsOptionsSerializer, MathQuestionsSerializer, MathOptionsSerializer, GEASQuestionsSerializer, GEASOptionsSerializer
from .models import ElecsQuestions, ElecsOptions, CommsQuestions, CommsOptions, MathQuestions, MathOptions, GEASQuestions, GEASOptions
from django.db.models import Max


class ElectronicsQuestionsAPI(viewsets.ViewSet):

    def list(self, request):
        questions = ElecsQuestions.objects.all()
        serializer = ElecsQuestionsSerializer(questions, many=True)
        elecs_questions = [{"question_id":question['id'], "question":question['content']} for question in serializer.data]
        data = {"elecs_questions":elecs_questions}
        return Response(data)

    def create(self, request):

        global field_labels

        if request.data:
            data = request.data
            max_question_id = ElecsQuestions.objects.aggregate(Max('id'))['id__max']
            max_option_id = ElecsOptions.objects.aggregate(Max('id'))['id__max']
            question = data.get('content')
            options = data.get('options')
            
            if max_question_id is None:
                max_question_id = 0
            
            if max_option_id is None:
                max_option_id = 0

            if question:
                new_question_id = max_question_id + 1
                new_question = ElecsQuestions.objects.create(id=new_question_id, content=question)

                if options:
                    for option_data in options:
                        max_option_id += 1
                        letter = option_data['letter']
                        content = option_data['content']
                        is_correct = option_data['is_correct']
                        new_option = ElecsOptions.objects.create(id=max_option_id, question_no_id=new_question_id, letter=letter, content=content, is_correct=is_correct)

                latest_max_qid = ElecsQuestions.objects.aggregate(Max('id'))['id__max']
                latest_max_opnid = ElecsOptions.objects.aggregate(Max('id'))['id__max']

            if latest_max_qid == max_option_id and latest_max_opnid == max_option_id:
                return Response({"message":"Question added succesfully"})
            
            else:
                return Response({"message":"There is an error during the process"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        
        data = request.data
        update_question_id = data.get('question_id')
        new_question = data.get('q_content')
       
        update_question = ElecsQuestions.objects.filter(id=pk).first()

        if update_question: 
           update_question.content = new_question
           update_question.save()
        
        return Response({"update_question_id":update_question_id, "new_question":new_question})
    

    def destroy(self, request, pk=None):
       question = ElecsQuestions.objects.filter(id=pk).first()
     
       if pk:
           question.delete()

       
           
       return Response({'message': 'Question deleted successfully'}, 200)
       
        

class ElectronicsChoicesAPI(viewsets.ViewSet):

    def list(self, request):
        questions = ElecsQuestions.objects.all()
        options = ElecsOptions.objects.all()
        serialized_options = ElecsOptionsSerializer(options, many=True).data
        serialized_questions = ElecsQuestionsSerializer(questions, many=True).data
        print(serialized_options)
        print(serialized_questions)
        elecs_questions = [{"id":question['id'], "content":question['content'], "options":[{"question_no":option['question_no_id'], "letter":option['letter'], "content":option['content'], "is_correct":option['is_correct']} for option in serialized_options if option['question_no_id'] == question['id']]} for question in serialized_questions]
        return Response(elecs_questions)
    


    def update(self, request, pk=None):
    
        data = request.data
        options = data.get('options')
        print(data)
        questions = ElecsOptions.objects.filter(question_no=pk).all()
        for question in questions:
            for option in options:
               if question.letter == option.get('letter'):
                   question.content = option.get('content')
                   question.is_correct = option.get('is_correct')
                   question.save()


        return Response(data)

            


class CommunicationsQuestionsAPI(viewsets.ViewSet):

    def list(self, request):
        questions = CommsQuestions.objects.all()
        serializer = CommsQuestionsSerializer(questions, many=True)
        comms_questions = [{"question_id":question['id'], "question":question['content']} for question in serializer.data]
        data = {"comms_questions":comms_questions}
        return Response(data)

    def create(self, request):

        global field_labels

        if request.data:
            data = request.data
            max_question_id = CommsQuestions.objects.aggregate(Max('id'))['id__max']
            max_option_id = CommsOptions.objects.aggregate(Max('id'))['id__max']
            question = data.get('content')
            options = data.get('options')
            
            if max_question_id is None:
                max_question_id = 0
            
            if max_option_id is None:
                max_option_id = 0

            if question:
                new_question_id = max_question_id + 1
                new_question = CommsQuestions.objects.create(id=new_question_id, content=question)

                if options:
                    for option_data in options:
                        max_option_id += 1
                        letter = option_data['letter']
                        content = option_data['content']
                        is_correct = option_data['is_correct']
                        new_option = CommsOptions.objects.create(id=max_option_id, question_no_id=new_question_id, letter=letter, content=content, is_correct=is_correct)

                latest_max_qid = CommsQuestions.objects.aggregate(Max('id'))['id__max']
                latest_max_opnid = CommsOptions.objects.aggregate(Max('id'))['id__max']

            if latest_max_qid == max_option_id and latest_max_opnid == max_option_id:
                return Response({"message":"Question added succesfully"})
            
            else:
                return Response({"message":"There is an error during the process"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        
        data = request.data
        update_question_id = data.get('question_id')
        new_question = data.get('q_content')
       
        update_question = CommsQuestions.objects.filter(id=pk).first()

        if update_question: 
           update_question.content = new_question
           update_question.save()
        
        return Response({"update_question_id":update_question_id, "new_question":new_question})
    

    def destroy(self, request, pk=None):
       question = CommsQuestions.objects.filter(id=pk).first()
     
       if pk:
           question.delete()

       
           
       return Response({'message': 'Question deleted successfully'}, 200)
       
        

class CommunicationsChoicesAPI(viewsets.ViewSet):

    def list(self, request):
        questions = CommsQuestions.objects.all()
        options = CommsOptions.objects.all()
        serialized_options = CommsOptionsSerializer(options, many=True).data
        serialized_questions = CommsQuestionsSerializer(questions, many=True).data
        print(serialized_options)
        print(serialized_questions)
        comms_questions = [{"id":question['id'], "content":question['content'], "options":[{"question_no":option['question_no_id'], "letter":option['letter'], "content":option['content'], "is_correct":option['is_correct']} for option in serialized_options if option['question_no_id'] == question['id']]} for question in serialized_questions]
        return Response(comms_questions)
    


    def update(self, request, pk=None):
    
        data = request.data
        options = data.get('options')
        print(data)
        questions = CommsOptions.objects.filter(question_no=pk).all()
        for question in questions:
            for option in options:
               if question.letter == option.get('letter'):
                   question.content = option.get('content')
                   question.is_correct = option.get('is_correct')
                   question.save()


        return Response(data)





class MathQuestionsAPI(viewsets.ViewSet):

    def list(self, request):
        questions = MathQuestions.objects.all()
        serializer = MathQuestionsSerializer(questions, many=True)
        math_questions = [{"question_id":question['id'], "question":question['content']} for question in serializer.data]
        data = {"math_questions":math_questions}
        print(data)
        return Response(data)

    def create(self, request):

        global field_labels

        if request.data:
            data = request.data
            max_question_id = MathQuestions.objects.aggregate(Max('id'))['id__max']
            max_option_id = MathOptions.objects.aggregate(Max('id'))['id__max']
            question = data.get('content')
            options = data.get('options')
            
            if max_question_id is None:
                max_question_id = 0
            
            if max_option_id is None:
                max_option_id = 0

            if question:
                new_question_id = max_question_id + 1
                new_question = MathQuestions.objects.create(id=new_question_id, content=question)

                if options:
                    for option_data in options:
                        max_option_id += 1
                        letter = option_data['letter']
                        content = option_data['content']
                        is_correct = option_data['is_correct']
                        new_option = MathOptions.objects.create(id=max_option_id, question_no_id=new_question_id, letter=letter, content=content, is_correct=is_correct)

                latest_max_qid = MathQuestions.objects.aggregate(Max('id'))['id__max']
                latest_max_opnid = MathOptions.objects.aggregate(Max('id'))['id__max']

            if latest_max_qid == max_option_id and latest_max_opnid == max_option_id:
                return Response({"message":"Question added succesfully"})
            
            else:
                return Response({"message":"There is an error during the process"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        
        data = request.data
        update_question_id = data.get('question_id')
        new_question = data.get('q_content')
       
        update_question = MathQuestions.objects.filter(id=pk).first()

        if update_question: 
           update_question.content = new_question
           update_question.save()
        
        return Response({"update_question_id":update_question_id, "new_question":new_question})
    

    def destroy(self, request, pk=None):
       question = MathQuestions.objects.filter(id=pk).first()
     
       if pk:
           question.delete()

       
           
       return Response({'message': 'Question deleted successfully'}, 200)
       
        

class MathChoicesAPI(viewsets.ViewSet):

    def list(self, request):
        questions = MathQuestions.objects.all()
        options = MathOptions.objects.all()
        serialized_options = MathOptionsSerializer(options, many=True).data
        serialized_questions = MathQuestionsSerializer(questions, many=True).data
        print(serialized_options)
        print(serialized_questions)
        math_questions = [{"id":question['id'], "content":question['content'], "options":[{"question_no":option['question_no_id'], "letter":option['letter'], "content":option['content'], "is_correct":option['is_correct']} for option in serialized_options if option['question_no_id'] == question['id']]} for question in serialized_questions]
        return Response(math_questions)
    


    def update(self, request, pk=None):
    
        data = request.data
        options = data.get('options')
        print(data)
        questions = MathOptions.objects.filter(question_no=pk).all()
        for question in questions:
            for option in options:
               if question.letter == option.get('letter'):
                   question.content = option.get('content')
                   question.is_correct = option.get('is_correct')
                   question.save()


        return Response(data)




class GEASQuestionsAPI(viewsets.ViewSet):

    def list(self, request):
        questions = GEASQuestions.objects.all()
        serializer = GEASQuestionsSerializer(questions, many=True)
        geas_questions = [{"question_id":question['id'], "question":question['content']} for question in serializer.data]
        data = {"geas_questions":geas_questions}
        print(data)
        return Response(data)

    def create(self, request):

        global field_labels

        if request.data:
            data = request.data
            max_question_id = GEASQuestions.objects.aggregate(Max('id'))['id__max']
            max_option_id = GEASOptions.objects.aggregate(Max('id'))['id__max']
            question = data.get('content')
            options = data.get('options')
            
            if max_question_id is None:
                max_question_id = 0
            
            if max_option_id is None:
                max_option_id = 0

            if question:
                new_question_id = max_question_id + 1
                new_question = GEASQuestions.objects.create(id=new_question_id, content=question)

                if options:
                    for option_data in options:
                        max_option_id += 1
                        letter = option_data['letter']
                        content = option_data['content']
                        is_correct = option_data['is_correct']
                        new_option = GEASOptions.objects.create(id=max_option_id, question_no_id=new_question_id, letter=letter, content=content, is_correct=is_correct)

                latest_max_qid = GEASQuestions.objects.aggregate(Max('id'))['id__max']
                latest_max_opnid = GEASOptions.objects.aggregate(Max('id'))['id__max']

            if latest_max_qid == max_option_id and latest_max_opnid == max_option_id:
                return Response({"message":"Question added succesfully"})
            
            else:
                return Response({"message":"There is an error during the process"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        
        data = request.data
        update_question_id = data.get('question_id')
        new_question = data.get('q_content')
       
        update_question = GEASQuestions.objects.filter(id=pk).first()

        if update_question: 
           update_question.content = new_question
           update_question.save()
        
        return Response({"update_question_id":update_question_id, "new_question":new_question})
    

    def destroy(self, request, pk=None):
       question = GEASQuestions.objects.filter(id=pk).first()
     
       if pk:
           question.delete()

       
           
       return Response({'message': 'Question deleted successfully'}, 200)
       
        

class GEASChoicesAPI(viewsets.ViewSet):

    def list(self, request):
        questions = GEASQuestions.objects.all()
        options = GEASOptions.objects.all()
        serialized_options = GEASOptionsSerializer(options, many=True).data
        serialized_questions = GEASQuestionsSerializer(questions, many=True).data
        print(serialized_options)
        print(serialized_questions)
        geas_questions = [{"id":question['id'], "content":question['content'], "options":[{"question_no":option['question_no_id'], "letter":option['letter'], "content":option['content'], "is_correct":option['is_correct']} for option in serialized_options if option['question_no_id'] == question['id']]} for question in serialized_questions]
        return Response(geas_questions)
    


    def update(self, request, pk=None):
    
        data = request.data
        options = data.get('options')
        print(data)
        questions = GEASOptions.objects.filter(question_no=pk).all()
        for question in questions:
            for option in options:
               if question.letter == option.get('letter'):
                   question.content = option.get('content')
                   question.is_correct = option.get('is_correct')
                   question.save()


        return Response(data)
    
