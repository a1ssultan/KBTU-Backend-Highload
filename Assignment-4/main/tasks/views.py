from django.shortcuts import render
from .forms import EmailForm
from .tasks import send_email_task


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.id)
            return render(request, 'email_sent.html', {'email': email})
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form})
