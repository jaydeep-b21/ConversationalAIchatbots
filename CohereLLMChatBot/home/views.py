from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import os
import cohere

cohere_api_key = "COHERE_API"

co = cohere.Client(cohere_api_key)


# Create your views here.
def chat(request):                                    #chat view
    # return HttpResponse("This Work")+
    return render(request, "inde.html")

def about(request):                                    #chat view
    # return HttpResponse("This Work")
    return render(request, "about.html")

def chatAPI(request):
    if request.method == "POST":
        prompt= request.POST["prompt"]
        response = co.generate(
            model='command-xlarge-nightly',
            prompt= prompt,
            max_tokens=300,
            temperature=0.9,
            k=0,
            p=0.75,
            frequency_penalty=0,
            presence_penalty=0,
            stop_sequences=[],
            return_likelihoods='NONE')
        print(response, '-'*50)
        print(response.generations[0].text)
        return JsonResponse(response.generations[0].text, safe=False)
    return HttpResponse("Bad Request")
        

