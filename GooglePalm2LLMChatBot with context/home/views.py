from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import os
import json

import google.generativeai as palm

api_key = "PALM_2_API"
palm.configure(api_key= api_key)


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
        response = palm.chat(
            model = "models/chat-bison-001",
            messages = prompt,
            temperature=0
        ) 
        print(response,'\n','-'*100)

        def replace_characters(input_text):
            # Replace \n and \r characters with space using .replace()
            text_without_newlines = input_text.replace('<br>', ' ')

            # Replace * and ** with blank space
            text_without_extrachars = text_without_newlines.replace('*', '').replace('**', '')

            return text_without_extrachars

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

        response_data = {
            'model': response.model,
            'context': response.context,
            'messages': response.messages,
            'temperature': response.temperature,
            'candidates': response.candidates,
        }
        print(response_data,'\n','+'*100)
        
        # Replace newline characters in the response_data dictionary
        response_data1 = replace_chars(response_data)
        print(type(response_data1))
        print(response_data1,'\n','1'*100)
         ########################################JSON File
        response_input_text = str(response_data)
        result_jsonfile = replace_characters(response_input_text)
        print(type(result_jsonfile))
        print(result_jsonfile,'\n','2'*100)
        # Convert the modified string into a dictionary
        result_jsonfile = eval(result_jsonfile)
        print(type(result_jsonfile))

        # Write to a JSON file
        with open('modified_system_requirements1.json', 'w') as json_file:
            json.dump(response_data1, json_file, indent=4)
        with open('modified_system_requirements2.json', 'w') as json_file:
            json.dump(result_jsonfile, json_file, indent=4)

        print("JSON file created successfully.")

        # Return the response as JSON
        return JsonResponse(response_data1, safe=False)
    return HttpResponse("Bad Request")



