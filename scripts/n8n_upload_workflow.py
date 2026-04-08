#!/usr/bin/env python3
"""
Script para fazer upload/atualizar workflow na N8N via API

Uso:
    python n8n_upload_workflow.py workflow.json                # Cria novo workflow
    python n8n_upload_workflow.py workflow.json --update ID    # Atualiza workflow existente
"""

import argparse
import json
import sys
import os
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Erro: Instale as bibliotecas necessarias:")
    print("  pip install requests python-dotenv")
    sys.exit(1)

# Configurar encoding para Windows
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')


def upload_workflow(workflow_json: dict, base_url: str, api_key: str, update_id: str = None) -> bool:
    """Faz upload de um workflow para a N8N"""

    base_url = base_url.rstrip('/')

    # Se tem update_id, atualiza workflow existente
    if update_id:
        url = f"{base_url}/api/v1/workflows/{update_id}"
        method = "PUT"
        print(f"Atualizando workflow ID: {update_id}")
    else:
        url = f"{base_url}/api/v1/workflows"
        method = "POST"
        print("Criando novo workflow...")

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key
    }

    # Remove campos que não devem ser enviados
    workflow_data = workflow_json.copy()
    for field in ['id', 'createdAt', 'updatedAt', 'versionId', 'activeVersionId', 'versionCounter', 'shared']:
        workflow_data.pop(field, None)

    # Adiciona settings padrão se não existir
    if 'settings' not in workflow_data:
        workflow_data['settings'] = {
            'executionOrder': 'v1',
            'binaryMode': 'separate'
        }

    try:
        response = requests.request(method, url, headers=headers, json=workflow_data, timeout=30)

        if response.status_code == 401:
            print("Erro 401: API KEY inválida ou expirada")
            return False
        elif response.status_code == 404 and update_id:
            print(f"Erro 404: Workflow '{update_id}' não encontrado")
            return False
        elif response.status_code not in [200, 201]:
            print(f"Erro {response.status_code}: {response.text}")
            return False

        result = response.json()

        if method == "POST":
            workflow_id = result.get('id', '')
            print(f"✅ Workflow criado com sucesso!")
            print(f"   ID: {workflow_id}")
            print(f"   Nome: {result.get('name', 'N/A')}")
        else:
            print(f"✅ Workflow atualizado com sucesso!")
            print(f"   ID: {update_id}")
            print(f"   Nome: {result.get('name', 'N/A')}")

        return True

    except requests.exceptions.Timeout:
        print("Erro: Timeout na requisição")
        return False
    except requests.exceptions.ConnectionError:
        print(f"Erro: Não foi possível conectar em {base_url}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Faz upload de workflow para a N8N via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python n8n_upload_workflow.py workflow.json
  python n8n_upload_workflow.py workflow.json --update 2SQKMc2vBxc7nlUK
  python n8n_upload_workflow.py workflow.json --url https://n8n.example.com
        """
    )

    parser.add_argument("workflow_json", help="Arquivo JSON do workflow")
    parser.add_argument("--update", "-u", metavar="ID",
                        help="ID do workflow para atualizar (em vez de criar novo)")
    parser.add_argument("--url", default=os.getenv("N8N_URL", "https://nell-unlandmarked-gayla.ngrok-free.dev"),
                        help="URL da instância N8N")
    parser.add_argument("--key", "-k", default=os.getenv("N8N_API_KEY"),
                        help="API Key da N8N")

    args = parser.parse_args()

    if not args.key:
        print("Erro: API KEY não fornecida")
        print("Use --key SUA_KEY ou defina N8N_API_KEY")
        sys.exit(1)

    # Carrega o workflow
    try:
        with open(args.workflow_json, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {args.workflow_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido: {e}")
        sys.exit(1)

    # Faz upload
    success = upload_workflow(
        workflow_json=workflow,
        base_url=args.url,
        api_key=args.key,
        update_id=args.update
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
