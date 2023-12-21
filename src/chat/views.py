from django.shortcuts import render


def chat_page_view(request):
    return render(request, 'chat/index.html')
