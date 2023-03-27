from rest_framework import (status, views, permissions, response)
from main.models import ScoreAPILog

class GetScoreView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        # convert reponse data into json
        input = self.request.query_params.get('input') or 0
        score = int(input) + 1
        ScoreAPILog.objects.create(user=request.user, score=score)
        return response.Response({'Score': score}, status=status.HTTP_200_OK)