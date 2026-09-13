import random
from django.shortcuts import render
from django.core.exceptions import BadRequest
from .data import data

subject = {
    "S": "science",
    "T": "technology",
    "H": "history",
    "G": "geography"
}

def index(request):
    return render(request, "index.html")

def quiz(request):
    category = request.GET.get("category")
    if(category not in data.keys()):
        raise BadRequest("Invalid Category!")

    questions = random.sample(data[category], k=10)
    params = { "data": questions }
    params["category"] = category
    return render(request, "quiz.html", params)

def result(request):
    params = { "data": [] }
    for id in request.POST.getlist("question-id"):
        s, i = subject[id[0]], int(id[1:])
        temp = data[s][i - 1]

        temp["answer"] = request.POST.get(id)
        temp["verdict"] = "correct" if temp["answer"] == temp["correct"] else "unanswered" if temp["answer"] == None else "incorrect"
        
        if(temp["answer"] != None):
            temp["user_answer"] = temp["options"][temp["answer"]]

        temp["correct_answer"] = temp["options"][temp["correct"]]
        params["data"].append(temp)

    params["info"] = {
        "percent": len([x for x in params["data"] if x["verdict"] == "correct"]) * 10,
        "correct": len([x for x in params["data"] if x["verdict"] == "correct"]),
        "incorrect": len([x for x in params["data"] if x["verdict"] == "incorrect"]),
        "unanswered": len([x for x in params["data"] if x["verdict"] == "unanswered"])
    }

    return render(request, "result.html", params)