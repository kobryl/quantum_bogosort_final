from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Tf
# Create your views here.


def index(request):
    tfs = Tf.objects.all()
    context = {'tfs': tfs}
    return render(request, 'final/index.html', context)


def tf(request, tf_id):
    tf = get_object_or_404(Tf, pk=tf_id)
    return render(request, 'final/tf.html', {'tf': tf})