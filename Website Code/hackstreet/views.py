from django.shortcuts import render


def home(request):
    data = {
        "title" : "SKYY",
        "color" : "white"
    }
    return render(request, "index.html", data)


def aboutUs(request):
    data = {
        "title" : "SKYY | About US",
        "color" : "white",
        "css" : "/static/css/style_about.css",
    }
    return render(request, "about_us.html", data)


def ticket(request):
    data = {
        "title" : "SKYY | Ticket",
        "color" : "#0047AB;",
        "css" : "/static/css/style_ticket.css",
    }
    return render(request, "tickets.html", data)

