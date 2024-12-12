from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import subprocess

def get_available_playbooks():
    try:
        # Executar comando ls via SSH para listar os playbooks
        result = subprocess.run(
            ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1", "ls /home/lab/labAutomation/playbooks/*.yml"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Processar a saída para obter apenas os nomes dos arquivos
        playbooks = []
        for line in result.stdout.strip().split('\n'):
            if line:  # Ignorar linhas vazias
                filename = line.split('/')[-1]  # Pega apenas o nome do arquivo
                playbooks.append(filename)
        
        return sorted(playbooks)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao listar playbooks: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

def script_execution(request):
    if request.method == "POST":
        selected_script = request.POST.get("playbooks")
        
        if selected_script:
            try:
                combined_output = ""
                combined_output += f"{'='*50}\nExecutando: {selected_script}\n{'='*50}\n"

                # Executar o script no Bash
                result = subprocess.run(
                    ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1", f"ansible-playbook /home/lab/labAutomation/playbooks/{selected_script}"],
                    capture_output=True,
                    text=True,
                )

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
            return JsonResponse({"error": "Nenhum playbook selecionado"})
    playbooks = get_available_playbooks()
    return render(request, "labautomation/script_execution.html", {"playbooks": playbooks})
