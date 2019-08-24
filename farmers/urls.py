from django.urls import path
from . import views


urlpatterns = [
        path('',views.home,name='home'),
        path('farmer-signup/',views.f_signup,name='farmer-signup'),
        path('farmer-login/',views.f_login,name='farmer-login'),
        path('farmer_signup_action/',views.farmer_signup_action,name='farmer_signup_action'),
        path('farmer_login_action/',views.farmer_login_action,name='farmer_login_action'),
        path('farmer_profile/',views.farmer_profile,name='farmer_profile'),
        path('farmer_logout/',views.farmer_logout,name='farmer_logout'),
        path('farmer_list/',views.farmer_list,name='farmer_list'),
        path('farmer_profile_view/<str:username>',views.farmer_profile_view,name='farmer_profile_view'),
        path('enquire_experts/',views.enquire_experts,name='enquire_experts'),
        path('enquire_experts_action/',views.enquire_experts_action,name='enquire_experts_action'),
        path('message_farmer/',views.message_farmer,name='message_farmer'),
        path('chat_box/',views.chat_box,name='chat_box'),
        path('chat_screen/',views.chat_screen,name='chat_screen'),
        path('on_chat_submit/',views.on_chat_submit,name='on_chat_submit'),
        path('on_submit_solution/',views.on_submit_solution,name='on_submit_solution'),
        path('view_submitted_solution_expert/',views.view_submitted_solution_expert,name='view_submitted_solution_expert'),
        path('pending_enq_from_solved/',views.pending_enq_from_solved,name='pending_enq_from_solved'),
        path('view_enquiry',views.view_enquiry,name='view_enquiry'),
        path('chat_box_list/<str:username1>',views.chat_box_list,name='chat_box_list'),
        path('add_yield/',views.add_yield,name='add_yield'),
        path('add_yield_action/',views.add_yield_action,name='add_yield_action'),





]
