from django.shortcuts import render
from .models import Comment, Booking

# Create your views here.
def show_main_page(request):
    if request.method == 'POST':
        post_comment(request)

    coms = Comment.objects.all()
    data = {'comments': coms}
    return render(request, 'main_page.html', context = data)


def show_trainings(request):
    return render(request, 'trainings.html')


def show_bookings(request):
    return render(request, 'bookings.html')


def show_booking_rules(request):
    return render(request, 'booking_rules.html')

def trainings_light(request):
    return render(request, '')


def post_comment(request):

    print('post comment')
    comment_text = request.POST.get('comment')
    rating_value = request.POST.get('rating_value')

    if not comment_text or not rating_value:
        return render(request, 'main_page.html')
    
    try:
        rating = int(rating_value)
        if not 1 <= rating <= 5:
            return render(request, 'main_page.html')
        
    except ValueError:
        return render(request, 'main_page.html')

    # Создаем и сохраняем комментарий
    comment = Comment(user_id = request.user, text = comment_text, rating_value = rating)
    comment.save()
