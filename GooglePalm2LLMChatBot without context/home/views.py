from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import os
import re
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
        print('+'*50,'\n',prompt,'\n','+'*50)
        response = palm.chat(
            model = "models/chat-bison-001",
            messages = prompt,
            temperature=0
        )
        
        text = prompt
        print("text:",text,'\n')
        # Use regex to find the desired text between <span class="d-block" style="font-weight:800">Jaydeep:</span> and <span class="d-block" style="font-weight:800">Lily:</span>
        matches = re.findall(r'<span class="d-block" style="font-weight:800">Jaydeep:</span>(.*?)<span class="d-block" style="font-weight:800">Daisy:</span>', text, re.DOTALL)
        print("matches:",matches,'\n')
        # Print the matches
        if matches:
            last_match = matches[-1].strip()
            print("last_match:",last_match,'\n')
        prompt = last_match 
        print("Prompt:",prompt,'\n','^'*50)
        response=response.reply(prompt)
        response = response.last
        print(response,'\n','-'*50)
        response = response.replace('\n', '<br>').replace('\r', '<br>')
        return JsonResponse(response, safe=False)
    return HttpResponse("Bad Request")