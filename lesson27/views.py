from django.shortcuts import render                 # 404
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)  # 404

