from django.urls import path

from api.views import *

urlpatterns = [
    path('api/v1/upload/', UploadContractFile.as_view()),
    path('api/v1/myfiles/', MyFiles.as_view()),
    path('api/v1/download/', DownloadContractFile.as_view()),
    path('api/v1/submit/', SubmitContractAddress.as_view()),
    path('api/v1/result/', QueryResult.as_view()),

    path('api/v1/user/nonce/', AuthView.as_view()),
    path('api/v1/user/auth/', AuthView.as_view()),

    # triathon
    path('api/v1/user/get_nonce/', LoginView.as_view()),
    path('api/v1/user/login/', LoginView.as_view()),

    path('api/v1/check_status', CheckStatus.as_view()),
    path('api/v1/total', TotalDetection.as_view()),
    path('api/v1/history', DetectionLog.as_view()),
    path('api/v1/details', DetectionDetails2.as_view()),

]
