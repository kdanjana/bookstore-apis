from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottleRate(UserRateThrottle):
    scope = 'book_review_create'
    
    
class ReviewListThrottleRate(UserRateThrottle):
    scope = 'reviews_list'