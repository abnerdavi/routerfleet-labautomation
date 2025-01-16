from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import os

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

def manage_rsc_files(request):
    if request.method == "POST" and request.FILES.get('rsc_file'):
        try:
            uploaded_file = request.FILES['rsc_file']
            
            # Verificar extensão do arquivo
            if not uploaded_file.name.endswith('.rsc'):
                return JsonResponse({'error': 'Apenas arquivos .rsc são permitidos'})
            
            # Criar arquivo temporário local
            temp_path = f'/tmp/{uploaded_file.name}'
            with open(temp_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Copiar arquivo para o servidor remoto via scp
            scp_command = ["sshpass", "-p", "labredes","scp", temp_path, f"lab@172.18.0.1:/home/lab/labAutomation/mktk-configs/"]
            
            result = subprocess.run(scp_command, capture_output=True, text=True)
            
            # Limpar arquivo temporário
            os.remove(temp_path)
            
            if result.returncode != 0:
                return JsonResponse({'error': f'Erro no upload: {result.stderr}'})
            
            return JsonResponse({'success': 'Arquivo enviado com sucesso'})
            
        except Exception as e:
            return JsonResponse({'error': f'Erro: {str(e)}'})
    
    # Listar arquivos existentes
    try:
        result = subprocess.run(
            ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1","ls -l /home/lab/labAutomation/mktk-configs/*.rsc"],
            capture_output=True,
            text=True
        )
        
        files = []
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Extrair apenas o nome do arquivo da saída do ls
                    filename = line.split()[-1].split('/')[-1]
                    if filename:
                        files.append(filename)
    except Exception as e:
        files = []
        
    return render(request, 'labautomation/rsc_manager.html', {'files': files})

def get_file_content(request):
    if request.method == "POST":
        filename = request.POST.get('filename')
        if not filename:
            return JsonResponse({'error': 'Nome do arquivo não fornecido'})
            
        try:
            # Ler conteúdo do arquivo via SSH
            result = subprocess.run(
                ["sshpass", "-p", "labredes", "ssh", "lab@172.18.0.1", f"cat /home/lab/labAutomation/mktk-configs/{filename}"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return JsonResponse({'content': result.stdout})
            else:
                return JsonResponse({'error': f'Erro ao ler arquivo: {result.stderr}'})
                
        except Exception as e:
            return JsonResponse({'error': f'Erro: {str(e)}'})
            
    return JsonResponse({'error': 'Método não permitido'})
