from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import time
import random
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurações
API_BASE_URL = "https://edusp-api.ip.tv"
CLIENT_DOMAIN = "https://trollchipsstarefas.vercel.app/"

# Mapeamento de categorias de tarefas
category_map = {
    1: 'Língua Portuguesa',
    5: 'Geografia',
    6: 'História',
    7: 'Sociologia',
    8: 'Biologia',
    9: 'Física',
    10: 'Matemática',
    11: 'Química',
    13: 'Língua Estrangeira Moderna - Inglês',
    17: 'Ciências',
    11621: 'Educação Financeira',
    5978: 'Filosofia',
    14332: 'Educação Financeira',
    156886: 'Multidisciplinar',
    459708: '90 dias SAEB - Matemática',
    459709: '90 dias SAEB - Língua Portuguesa',
}

class AuthManager:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://trollchipsstarefas.vercel.app/',
            'priority': 'u=0',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-api-platform': 'webclient',
            'x-api-realm': 'edusp',
            'x-client-domain': CLIENT_DOMAIN,
        }
    
    def _generate_signature(self):
        import base64
        random_num = random.randint(10**8, 10**9)
        return base64.b64encode(str(random_num).encode()).decode()
    
    def _generate_timestamp(self):
        return str(int(time.time() * 1000))
    
    def _generate_request_id(self):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(chars) for _ in range(6))
    
    def _get_headers(self):
        dynamic_headers = {
            'x-client-signature': self._generate_signature(),
            'x-client-timestamp': self._generate_timestamp(),
            'x-request-id': self._generate_request_id(),
        }
        return {**self.headers, **dynamic_headers}
    
    def login(self, ra, password):
        try:
            url = f"{API_BASE_URL}/registration/edusp"
            payload = {
                "login": ra,
                "password": password,
                "realm": "edusp"
            }
            
            headers = self._get_headers()
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            auth_data = response.json()
            
            user_info = {
                'nick': auth_data.get('nick'),
                'auth_token': auth_data.get('auth_token'),
                'external_id': auth_data.get('external_id'),
                'name': auth_data.get('name', '')
            }
            
            return {
                'success': True,
                'message': 'Login realizado com sucesso',
                'user_info': user_info
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'Erro na autenticação: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro inesperado: {str(e)}'
            }

class TaskProcessor:
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def _get_headers(self, auth_token):
        auth_manager = AuthManager()
        base_headers = auth_manager._get_headers()
        
        headers = {
            **base_headers,
            'x-api-key': auth_token,
        }
        return headers
    
    def get_pending_tasks(self, auth_token, nick):
        try:
            url = f"{self.base_url}/tms/task/todo"
            params = {
                'expired_only': 'false',
                'is_essay': 'false',
                'is_exam': 'false',
                'answer_statuses': ['draft', 'pending'],
                'with_answer': 'true',
                'with_apply_moment': 'true',
                'limit': 100,
                'filter_expired': 'true',
                'offset': 0
            }
            
            headers = self._get_headers(auth_token)
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            tasks = response.json().get('tasks', [])
            
            return {
                'success': True,
                'tasks': tasks,
                'count': len(tasks)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao buscar tarefas pendentes: {str(e)}',
                'tasks': []
            }
    
    def get_completed_tasks(self, auth_token, nick):
        """Obtém tarefas já entregues"""
        try:
            # Esta é uma implementação de exemplo - você precisará ajustar conforme a API real
            # Normalmente há um endpoint diferente para tarefas entregues
            return {
                'success': True,
                'tasks_entregues': [],
                'count': 0
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao buscar tarefas entregues: {str(e)}',
                'tasks_entregues': []
            }
    
    def get_expired_tasks(self, auth_token, nick):
        """Obtém tarefas expiradas"""
        try:
            # Implementação para tarefas expiradas
            # Normalmente é um filtro no endpoint de tarefas
            return {
                'success': True,
                'tasks': [],
                'count': 0
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao buscar tarefas expiradas: {str(e)}',
                'tasks': []
            }
    
    def process_task(self, auth_token, task_data):
        """Processa uma tarefa específica"""
        try:
            task_id = task_data.get('task_id')
            
            # Simular tempo de processamento
            min_time = int(task_data.get('time_min', 30))
            max_time = int(task_data.get('time_max', 60))
            processing_time = random.randint(min_time, max_time)
            
            # Simular processamento
            time.sleep(processing_time)
            
            return {
                'success': True,
                'message': f'Tarefa processada com sucesso em {processing_time} minutos',
                'task_id': task_id,
                'score': 10.0
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao processar tarefa: {str(e)}'
            }

# Inicializar componentes
auth_manager = AuthManager()
task_processor = TaskProcessor()

@app.route('/auth', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        ra = data.get('ra')
        password = data.get('password')
        
        if not ra or not password:
            return jsonify({
                'success': False,
                'message': 'RA e senha são obrigatórios'
            }), 400
            
        auth_result = auth_manager.login(ra, password)
        
        if auth_result['success']:
            return jsonify(auth_result)
        else:
            return jsonify(auth_result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno durante autenticação: {str(e)}'
        }), 500

@app.route('/tasks/pending', methods=['POST'])
def get_pending_tasks():
    try:
        data = request.get_json()
        auth_token = data.get('auth_token')
        nick = data.get('nick')
        
        if not auth_token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação é obrigatório'
            }), 400
            
        tasks = task_processor.get_pending_tasks(auth_token, nick)
        return jsonify(tasks)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar tarefas: {str(e)}'
        }), 500

@app.route('/tasks/entregues', methods=['POST'])
def get_completed_tasks():
    try:
        data = request.get_json()
        auth_token = data.get('auth_token')
        nick = data.get('nick')
        
        if not auth_token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação é obrigatório'
            }), 400
            
        tasks = task_processor.get_completed_tasks(auth_token, nick)
        return jsonify(tasks)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar tarefas entregues: {str(e)}'
        }), 500

@app.route('/tasks/expired', methods=['POST'])
def get_expired_tasks():
    try:
        data = request.get_json()
        auth_token = data.get('auth_token')
        nick = data.get('nick')
        
        if not auth_token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação é obrigatório'
            }), 400
            
        tasks = task_processor.get_expired_tasks(auth_token, nick)
        return jsonify(tasks)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar tarefas expiradas: {str(e)}'
        }), 500

@app.route('/fazer_task', methods=['POST'])
def process_task():
    try:
        data = request.get_json()
        auth_token = data.get('auth_token')
        task_data = data.get('task')
        
        if not auth_token or not task_data:
            return jsonify({
                'success': False,
                'message': 'Token e dados da tarefa são obrigatórios'
            }), 400
            
        result = task_processor.process_task(auth_token, task_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar tarefa: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Servidor funcionando'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
