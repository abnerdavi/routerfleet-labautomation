from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import subprocess

def hello_world(request):
    return HttpResponse("Hello, World! Bem-vindo à LabAutomation by Routerfleet!")

def script_execution(request):
    if request.method == "POST":
        script_option = request.POST.get("option")
        scripts = {
            "1": "script1.sh",
            "2": "script2.sh",
            "3": "script3.sh",
            "4": "script4.sh",
        }
        selected_script = scripts.get(script_option)

        if selected_script:
            try:
                # Executar o script no Bash
                result = subprocess.run(
                    ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1", f"bash {selected_script}"],
                    capture_output=True,
                    text=True,
                )
                output = result.stdout
                error = result.stderr
                return JsonResponse({"output": output, "error": error})
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            return JsonResponse({"error": "Opção inválida"})
    return render(request, "labautomation/script_execution.html")
