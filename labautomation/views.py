from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import subprocess

def script_execution(request):
    if request.method == "POST":
        script_option = request.POST.get("option")
        scripts = {
            "1": "pb_lab1.yml",
            "2": "pb_lab2.yml",
            "3": "pb_lab3.yml",
            "4": "pb_lab4.yml",
        }
        selected_script = scripts.get(script_option)

        if selected_script:
            try:
                # Executar o script no Bash
                result = subprocess.run(
                    ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1", f"ansible-playbook /home/lab/labAutomation/playbooks/{selected_script}"],
                    capture_output=True,
                    text=True,
                )

                combined_output = ""
                if result.stdout:
                    combined_output += result.stdout
                if result.stderr:
                    combined_output += "\nErros:\n" + result.stderr
                
                # Se não houver saída, adicionar uma mensagem
                if not combined_output:
                    combined_output = "O script foi executado, mas não produziu nenhuma saída."
                
                return JsonResponse({"output": combined_output})
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            return JsonResponse({"error": "Opção inválida"})
    return render(request, "labautomation/script_execution.html")
