from django.urls import path

from api.views import *

urlpatterns = [
    path('upload/', UploadContractFile.as_view()),
    path('myfiles/', MyFiles.as_view()),
    path('download/', DownloadContractFile.as_view()),
    path('submit/', SubmitContractAddress.as_view()),

    path('user/nonce/', AuthView.as_view()),
    path('user/auth/', AuthView.as_view()),

]
