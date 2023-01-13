from django.urls import path

from api.views import *

urlpatterns = [
    path('upload/', UploadContractFile.as_view()),
    path('myfiles/', MyFiles.as_view()),
    path('download/', DownloadContractFile.as_view()),
    path('submit/', SubmitContractAddress.as_view()),
    path('result/', QueryResult.as_view()),

    path('user/nonce/', AuthView.as_view()),
    path('user/auth/', AuthView.as_view()),

    # triathon
    path('user/get_nonce/', LoginView.as_view()),
    path('user/login/', LoginView.as_view()),

    path('api/v1/check_status', CheckStatus.as_view()),
    path('api/v1/total', TotalDetection.as_view()),
    path('api/v1/history', DetectionLog.as_view()),
    path('api/v1/details', DetectionDetails.as_view()),

]
