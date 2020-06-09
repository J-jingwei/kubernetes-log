from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import logman.kubetools as tools


def index(request):
    if request.GET.get('svc') and request.GET.get('env'):
        keyword = request.GET['svc']
        if '_' in keyword:
            keyword = keyword.replace('_', '-')
        env = request.GET['env']
        all = tools.ToolsBundle(serverName=keyword, envName=env)
        svc_data = all.svc()
        pod_data = all.pod()
        ing_data = all.ing()
        return render(request, "svc.html", {"PodBundle": pod_data, "SvcBundle": svc_data, "IngBundle": ing_data})
    elif request.GET.get('urlpath') and request.GET.get('env'):
        urlpath = request.GET['urlpath']
        env = request.GET['env']
        all = tools.ToolsBundle(urlPath=urlpath, envName=env)
        dataing = all.ingpath()
        ing_data = dataing
        for s in ing_data:
            server = s.get('ing_svc')
            all2 = tools.ToolsBundle(serverName=server, envName=env)
            svc_data = all2.svc()
            pod_data = all2.pod()
            ing_data = all2.ing()
            return render(request, "svc.html", {"PodBundle": pod_data, "SvcBundle": svc_data, "IngBundle": ing_data})
    else:
        return render(request, 'svc.html')

