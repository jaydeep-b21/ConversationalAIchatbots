from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import os
import openai

openai.api_key = "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"


# Create your views here.
def chat(request):                                    #chat view
    # return HttpResponse("This Work")+
    return render(request, "index.html")

def about(request):                                    #chat view
    # return HttpResponse("This Work")
    return render(request, "about.html")

def chatAPI(request):                                 #API , returns json response       
    if request.method == "POST":
        prompt = request.POST["prompt"] 
        print(prompt,'\n','-'*50)

        def replace_chars(input_dict):
            for key, value in input_dict.items():
                if isinstance(value, str):
                    # Replace newline characters with <br> for string values
                    input_dict[key] = value.replace('\n', '<br>').replace('\r', '')
                elif isinstance(value, list):
                    # Recursively replace newline characters in list elements
                    input_dict[key] = [replace_chars(item) if isinstance(item, dict) else item for item in value]
                elif isinstance(value, dict):
                    # Recursively replace newline characters in dictionary values
                    input_dict[key] = replace_chars(value)
            return input_dict
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
         # Replace newline characters in the response_data dictionary
        response_data = replace_chars(response)
        print(response_data,'\n','-'*100)
        return JsonResponse(response_data)
    return HttpResponse("Bad Request")

