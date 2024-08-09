from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork


class MoviesApiMixin:
    http_method_names = ['get']
    model = FilmWork

    def get_queryset(self):
        queryset = FilmWork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type'
        ).annotate(
            genres=Coalesce(ArrayAgg('genres__name', distinct=True), []),
            actors=Coalesce(
                ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='actor'), distinct=True),
                []),
            directors=Coalesce(
                ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='director'), distinct=True),
                []),
            writers=Coalesce(
                ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='writer'), distinct=True),
                [])
        ).order_by('title')
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = context['object_list']
        paginator = context['paginator']
        page = context['page_obj']

        results = list(queryset)

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.number - 1 if page.has_previous() else None,
            "next": page.number + 1 if page.has_next() else None,
            "results": results,
        }

        return context


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_context_data(self, **kwargs):
        return self.object
