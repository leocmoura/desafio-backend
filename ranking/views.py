from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ranking.models import Ranking, Comment
from ranking.serializers import UserRateMovieSerializer, UserRankingListSerializer, GeneralMovieRatingSerializer, CommentSerializer, CommentListSerializer
from ranking.repository import create_ranking_instance, calculate_movie_ratings
from notification.models import Notification

class UserRateMovieView(CreateAPIView):
    queryset = Ranking.objects.all()
    serializer_class = UserRateMovieSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie')
        rating = int(request.data.get('personal_rating'))
        comment_text = request.data.get('comment')

        ranking_instance = create_ranking_instance(user, movie_id, rating, comment=comment_text)
       
        return Response(self.serializer_class(instance=ranking_instance).data, status=status.HTTP_201_CREATED)

class UserRankingListView(generics.ListAPIView):
    serializer_class = UserRankingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ranking.objects.filter(user=user).select_related('movie')

class RatingDeleteView(generics.DestroyAPIView):
    queryset = Ranking.objects.all()
    serializer_class = UserRateMovieSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'Rating successfully deleted.'})
        except Ranking.DoesNotExist:
            return Response({'message':'Rating not found.'})

class GeneralListMovieRatingView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        movie_ratings = calculate_movie_ratings()

        results = [
            {
                'movie_title': item['movie__title'],
                'rating': item['avg_rating']
            }
            for item in movie_ratings
        ]

        serializer = GeneralMovieRatingSerializer(results, many=True)

        return Response(serializer.data)

class CommentsListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentListSerializer

    def get(self, request):
        comments = Ranking.objects.filter(comment__isnull=False).select_related('user', 'movie', 'comment')
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)