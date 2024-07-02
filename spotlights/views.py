from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SpotlightCelebritySerializer, SpotlightMovieSerializer, SpotlightWebSeriesSerializer
from .models import SpotlightCelebrities, SpotlightMovies, SpotlightWebSeries


class SpotlightDataView(APIView):
    def get(self, request, *args, **kwargs):
        fields_param = request.query_params.get('fields', '')
        response_data = {}

        if 'celebrity' in fields_param:
            celebrities = SpotlightCelebrities.objects.filter(active=True)
            response_data['celebrities'] = SpotlightCelebritySerializer(
                celebrities, many=True, context={"request": request}).data

        if 'movie' in fields_param:
            movies = SpotlightMovies.objects.filter(active=True)
            response_data['movies'] = SpotlightMovieSerializer(
                movies, many=True, context={"request": request}).data

        if 'webseries' in fields_param:
            web_series = SpotlightWebSeries.objects.filter(active=True)
            response_data['webseries'] = SpotlightWebSeriesSerializer(
                web_series, many=True, context={"request": request}).data

        return Response(response_data)
