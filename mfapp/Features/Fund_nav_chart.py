# mfapp/feature/Fund_nav_chart.py
import requests
import logging
from django.db.models import Q
from mfapp.forms import FundSearchForm
from mfapp.models import CSVData
from django.shortcuts import render

logger = logging.getLogger(__name__)

API_URL = 'https://api.mfapi.in/mf/'

def fund_dashboard(request):
    """
    Handle the fund dashboard view, processing search requests and fetching NAV data.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML response with fund data.
    """
    context = {
        'form': FundSearchForm(),
        'dates': [],
        'navs': [],
        'error': None,
        'scheme_name': None,
    }

    if request.method == 'POST':
        form = FundSearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['query'].strip()
            logger.info(f"User searched for: {query}")

            try:
                mutual_fund = CSVData.objects.get(
                    Q(scheme_name__icontains=query) |
                    Q(scheme_id__iexact=query) |
                    Q(isin__iexact=query) |
                    Q(scheme_code__iexact=query)
                )

                # Fetch historical data using the scheme code from the API
                response = requests.get(f'{API_URL}{mutual_fund.scheme_code}')

                if response.ok:
                    data = response.json().get('data', [])
                    context['dates'] = [entry['date'] for entry in data]
                    context['navs'] = [entry['nav'] for entry in data]
                    context['scheme_name'] = mutual_fund.scheme_name
                    logger.info(f"Fetched NAV data for {mutual_fund.scheme_name}: Dates - {context['dates']}, NAVs - {context['navs']}")
                else:
                    context['error'] = 'Error fetching historical data from API.'
                    logger.error(f"API request failed with status code: {response.status_code}")

            except CSVData.DoesNotExist:
                context['error'] = 'No mutual fund found with the given ID, ISIN, scheme name, or scheme code.'
                logger.warning(context['error'])
            except Exception as e:
                context['error'] = 'An unexpected error occurred.'
                logger.error(f"Unexpected error: {str(e)}")

    # Return an HttpResponse using render
    return render(request, 'Fund_nav_chart.html', context)

