import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Booking, Comment, CourtTimePrice, Trainings, AllTrainingSlots

class BookingModelTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_booking_creation(self):
        """Test booking model creation"""
        booking = Booking.objects.create(
            user_id=self.user,
            court_id=1,
            booking_datetime=datetime.datetime.now(),
            status='Подтверждено',
            price=100
        )
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.__str__(), f'User_id - {self.user}, время - {booking.booking_datetime}, court_id - 1, статус - Подтверждено')

    def test_booking_creation_2(self):
        """Test booking model creation"""
        booking = Booking.objects.create(
            user_id=self.user,
            court_id=1,
            booking_datetime=datetime.datetime.now(),
            status='Подтверждено',
            price=100
        )
        self.assertIsInstance(booking, Booking)
        self.assertEqual(booking.__str__(), f'User_id - {self.user}, время - {booking.booking_datetime}, court_id - 1, статус - Подтверждено')

    
class CommentModelTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_comment_creation(self):
        """Test comment model creation"""
        comment = Comment.objects.create(
            user_id=self.user,
            rating_value=5,
            text='Отличный корт!'
        )
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.__str__(), f'User_id - {self.user}, оценка - {5}, дата - {comment.created_at}')

    def test_comment_creation_2(self):
        """Test comment model creation"""
        comment = Comment.objects.create(
            user_id=self.user,
            rating_value=5,
            text='Отличный корт!'
        )
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.__str__(), f'User_id - {self.user}, оценка - {5}, дата - {comment.created_at}')


class CourtTimePriceModelTest(TestCase):
    def test_court_time_price_creation(self):
        """Test court time price model creation"""
        court_time_price = CourtTimePrice.objects.create(
            week_day='Понедельник',
            time='06:00',
            price=500
        )
        self.assertIsInstance(court_time_price, CourtTimePrice)
        self.assertEqual(court_time_price.__str__(), 'Понедельник, 06:00 - 500 руб.')

    def test_court_time_price_creation_2(self):
        """Test court time price model creation"""
        court_time_price = CourtTimePrice.objects.create(
            week_day='Понедельник',
            time='06:00',
            price=500
        )
        self.assertIsInstance(court_time_price, CourtTimePrice)
        self.assertEqual(court_time_price.__str__(), 'Понедельник, 06:00 - 500 руб.')

    

class TrainingsModelTest(TestCase):
    def test_trainings_creation(self):
        """Test trainings model creation"""
        training = Trainings.objects.create(
            trainer_name='Александр Игнатов',
            level='light',
            date=datetime.date.today(),
            time='10:00'
        )
        self.assertIsInstance(training, Trainings)

    def test_trainings_creation_2(self):
        """Test trainings model creation"""
        training = Trainings.objects.create(
            trainer_name='Александр Игнатов',
            level='light',
            date=datetime.date.today(),
            time='10:00'
        )
        self.assertIsInstance(training, Trainings)


class AllTrainingSlotsModelTest(TestCase):
    def test_all_training_slots_creation(self):
        """Test all training slots model creation"""
        all_training_slots = AllTrainingSlots.objects.create(
            training_id=1,
            slot_number=1,
            user_id=1,
            status=1
        )
        self.assertIsInstance(all_training_slots, AllTrainingSlots)
        self.assertEqual(all_training_slots.__str__(), 'Номер тренировки: 1, Место: 1, user_id: 1')

    def test_all_training_slots_creation_2(self):
        """Test all training slots model creation"""
        all_training_slots = AllTrainingSlots.objects.create(
            training_id=1,
            slot_number=1,
            user_id=1,
            status=1
        )
        self.assertIsInstance(all_training_slots, AllTrainingSlots)
        self.assertEqual(all_training_slots.__str__(), 'Номер тренировки: 1, Место: 1, user_id: 1')

    
class ShowBookingsViewTest(TestCase):
    def setUp(self):
        # Create a client for sending requests
        self.client = Client()
        # Create a user for authentication (if required)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_show_bookings_view(self):
        """Test show bookings view"""
        # Get the URL for the show_bookings view
        url = reverse('bookings_with_offset', kwargs={'week_offset': 0})
        # Send a GET request to this URL
        response = self.client.get(url)
        # Check that the view returned HTTP code 200 (successful request)
        self.assertEqual(response.status_code, 200)
        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'bookings.html')

    def test_show_bookings_view_2(self):
        """Test show bookings view"""
        # Get the URL for the show_bookings view
        url = reverse('bookings_with_offset', kwargs={'week_offset': 0})
        # Send a GET request to this URL
        response = self.client.get(url)
        # Check that the view returned HTTP code 200 (successful request)
        self.assertEqual(response.status_code, 200)
        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'bookings.html')

class MainPageViewTest(TestCase):
    def test_main_page_view(self):
        """Test main page view"""
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')

    def test_main_page_view_2(self):
        """Test main page view"""
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')


class ShowTrainingsViewTest(TestCase):
    def test_show_trainings_view(self):
        """Test show trainings view"""
        url = reverse('trainings_light')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_light.html')

    def test_show_trainings_view_2(self):
        """Test show trainings view"""
        url = reverse('trainings_light')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_light.html')

    def test_trainings_medium_view(self):
        """Test show trainings view"""
        url = reverse('trainings_medium')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_medium.html')

    def test_trainings_medium_view_2(self):
        """Test show trainings view"""
        url = reverse('trainings_medium')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_medium.html')

    def test_trainings_hard_view(self):
        """Test show trainings view"""
        url = reverse('trainings_hard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_hard.html')

    def test_trainings_hard_view_2(self):
        """Test show trainings view"""
        url = reverse('trainings_hard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainings_hard.html')


class ShowBookingRulesViewTest(TestCase):
    def test_show_booking_rules_view(self):
        """Test show booking rules view"""
        url = reverse('booking_rules')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_rules.html')

    def test_show_booking_rules_view_2(self):
        """Test show booking rules view"""
        url = reverse('booking_rules')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_rules.html')

    
class UsersViewTest(TestCase): # Add user-related test
    def setUp(self):
        self.client = Client()

    def test_login_page_view(self):
        """Test login page view"""
        url = reverse('users:login')  # Corrected namespacing
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_page_view_2(self):
        """Test login page view"""
        url = reverse('users:login')  # Corrected namespacing
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    
    def test_register_page_view(self):
        """Test register page view"""
        url = reverse('users:register')  # Corrected namespacing
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_page_view_2(self):
        """Test register page view"""
        url = reverse('users:register')  # Corrected namespacing
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')


