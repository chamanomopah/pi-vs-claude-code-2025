"""
Processador de comandos de voz.
Interpreta comandos reconhecidos e executa ações.
"""

import re
import subprocess
import platform
from typing import Optional, Dict, List, Callable
import logging


class Command:
    """Representa um comando de voz."""
    
    def __init__(self, text: str, confidence: float = 1.0):
        """
        Inicializa comando.
        
        Args:
            text: Texto do comando
            confidence: Confiança do reconhecimento (0-1)
        """
        self.text = text.lower().strip()
        self.confidence = confidence
        self.intent = None
        self.entities = {}
    
    def __repr__(self) -> str:
        return f"Command(text='{self.text}', confidence={self.confidence})"


class CommandProcessor:
    """
    Processador de comandos de voz.
    Mapeia comandos para ações.
    """
    
    # Padrões de comandos
    COMMAND_PATTERNS = {
        # Comandos do sistema
        r'(\b(abrir|abre|open)\s+(?P<app>.+))': 'open_app',
        r'(\b(fechar|fecha|close)\s+(?P<app>.+))': 'close_app',
        r'(\b(desligar|desliga|shutdown|desligar\s+computador))': 'shutdown',
        r'(\b(reiniciar|reinicia|restart))': 'restart',
        r'(\b(hora|horas|que\s+horas\s+são))': 'get_time',
        r'(\b(data|dia|que\s+dia\s+é|hoje))': 'get_date',
        
        # Comandos de volume
        r'(\b(aumentar|aumenta|subir|sobe)\s+volume)': 'volume_up',
        r'(\b(diminuir|diminui|baixar|baixa)\s+volume)': 'volume_down',
        r'(\b(mutar|muda|silenciar))': 'mute',
        r'(\b(desmutar|ativar\s+som))': 'unmute',
        
        # Comandos de pesquisa
        r'(\b(pesquisar|pesquisa|procurar|procura|google)\s+(?P<query>.+))': 'search',
        r'(\b(youtube)(\s+(?P<query>.+)))?': 'youtube',
        
        # Comandos de informação
        r'(\b(clima|tempo|previsão))': 'weather',
        r'(\b(notícias|noticias))': 'news',
        
        # Comandos gerais
        r'(\b(ajuda|help|comandos))': 'help',
        r'(\b(cancelar|cancela|parar|pare))': 'cancel',
    }
    
    def __init__(self):
        """Inicializa processador de comandos."""
        self.custom_handlers: Dict[str, Callable] = {}
        self.logger = logging.getLogger('CommandProcessor')
        
        logging.info("✅ CommandProcessor inicializado")
        logging.info(f"   {len(self.COMMAND_PATTERNS)} padrões de comandos carregados")
    
    def process(self, command: Command) -> Optional[Dict]:
        """
        Processa um comando e retorna a ação correspondente.
        
        Args:
            command: Instância de Command
            
        Returns:
            Dict com intent e entidades ou None
        """
        for pattern, intent in self.COMMAND_PATTERNS.items():
            match = re.search(pattern, command.text, re.IGNORECASE)
            
            if match:
                command.intent = intent
                command.entities = match.groupdict() if match.groupdict() else {}
                
                self.logger.info(f"🎯 Intent reconhecido: '{intent}'")
                
                if command.entities:
                    self.logger.debug(f"   Entidades: {command.entities}")
                
                return {
                    'intent': intent,
                    'entities': command.entities,
                    'text': command.text,
                    'confidence': command.confidence
                }
        
        # Comando não reconhecido
        self.logger.warning(f"❓ Comando não reconhecido: '{command.text}'")
        return None
    
    def execute(self, command: Command) -> bool:
        """
        Executa um comando.
        
        Args:
            command: Instância de Command
            
        Returns:
            True se executado com sucesso
        """
        result = self.process(command)
        
        if not result:
            return False
        
        intent = result['intent']
        entities = result['entities']
        
        # Verificar handler customizado
        if intent in self.custom_handlers:
            try:
                return self.custom_handlers[intent](entities)
            except Exception as e:
                self.logger.error(f"Erro no handler customizado: {e}")
                return False
        
        # Executar ação padrão
        return self._execute_default(intent, entities)
    
    def _execute_default(self, intent: str, entities: Dict) -> bool:
        """Executa ação padrão baseada no intent."""
        try:
            if intent == 'open_app':
                return self._open_app(entities.get('app', ''))
            
            elif intent == 'close_app':
                return self._close_app(entities.get('app', ''))
            
            elif intent == 'shutdown':
                return self._shutdown()
            
            elif intent == 'restart':
                return self._restart()
            
            elif intent == 'get_time':
                return self._get_time()
            
            elif intent == 'get_date':
                return self._get_date()
            
            elif intent == 'volume_up':
                return self._volume_up()
            
            elif intent == 'volume_down':
                return self._volume_down()
            
            elif intent == 'mute':
                return self._mute()
            
            elif intent == 'unmute':
                return self._unmute()
            
            elif intent == 'search':
                return self._search(entities.get('query', ''))
            
            elif intent == 'youtube':
                query = entities.get('query', '')
                return self._youtube(query)
            
            elif intent == 'help':
                return self._help()
            
            else:
                self.logger.warning(f"Intent sem implementação: '{intent}'")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao executar comando: {e}")
            return False
    
    # Implementações das ações
    
    def _open_app(self, app_name: str) -> bool:
        """Abre um aplicativo."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.Popen(['start', app_name], shell=True)
            elif system == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', app_name])
            else:  # Linux
                subprocess.Popen([app_name])
            
            self.logger.info(f"✅ Abrindo: {app_name}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao abrir {app_name}: {e}")
            return False
    
    def _close_app(self, app_name: str) -> bool:
        """Fecha um aplicativo."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run(['taskkill', '/f', '/im', f'{app_name}.exe'], 
                             capture_output=True)
            elif system == 'Darwin':
                subprocess.run(['pkill', '-x', app_name], capture_output=True)
            else:  # Linux
                subprocess.run(['pkill', app_name], capture_output=True)
            
            self.logger.info(f"✅ Fechando: {app_name}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao fechar {app_name}: {e}")
            return False
    
    def _shutdown(self) -> bool:
        """Desliga o computador."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run(['shutdown', '/s', '/t', '0'])
            elif system == 'Darwin':
                subprocess.run(['shutdown', '-h', 'now'])
            else:
                subprocess.run(['shutdown', 'now'])
            
            self.logger.info("⚠️  Desligando computador...")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao desligar: {e}")
            return False
    
    def _restart(self) -> bool:
        """Reinicia o computador."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run(['shutdown', '/r', '/t', '0'])
            elif system == 'Darwin':
                subprocess.run(['shutdown', '-r', 'now'])
            else:
                subprocess.run(['shutdown', '-r', 'now'])
            
            self.logger.info("⚠️  Reiniciando computador...")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao reiniciar: {e}")
            return False
    
    def _get_time(self) -> bool:
        """Diz a hora atual."""
        from datetime import datetime
        
        time_str = datetime.now().strftime("%H:%M")
        self.logger.info(f"🕐 Agora são {time_str}")
        print(f"\n🕐 Agora são {time_str}")
        return True
    
    def _get_date(self) -> bool:
        """Diz a data atual."""
        from datetime import datetime
        
        date_str = datetime.now().strftime("%d de %B de %Y")
        self.logger.info(f"📅 Hoje é {date_str}")
        print(f"\n📅 Hoje é {date_str}")
        return True
    
    def _volume_up(self) -> bool:
        """Aumenta o volume."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                # Usar PowerShell para aumentar volume
                subprocess.run([
                    'powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'
                ])
            elif system == 'Darwin':
                subprocess.run(['osascript', '-e', 
                               'set volume output volume (output volume of (get volume settings) + 10)'])
            else:
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', '10%+'])
            
            self.logger.info("🔊 Volume aumentado")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao aumentar volume: {e}")
            return False
    
    def _volume_down(self) -> bool:
        """Diminui o volume."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run([
                    'powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'
                ])
            elif system == 'Darwin':
                subprocess.run(['osascript', '-e',
                               'set volume output volume (output volume of (get volume settings) - 10)'])
            else:
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', '10%-'])
            
            self.logger.info("🔉 Volume diminuído")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao diminuir volume: {e}")
            return False
    
    def _mute(self) -> bool:
        """Muta o áudio."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run([
                    'powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
                ])
            elif system == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume with output muted'])
            else:
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', 'mute'])
            
            self.logger.info("🔇 Áudio mutado")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao mutar: {e}")
            return False
    
    def _unmute(self) -> bool:
        """Desmuta o áudio."""
        system = platform.system()
        
        try:
            if system == 'Windows':
                subprocess.run([
                    'powershell', '-c',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
                ])
            elif system == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume without output muted'])
            else:
                subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', 'unmute'])
            
            self.logger.info("🔊 Áudio ativado")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao desmutar: {e}")
            return False
    
    def _search(self, query: str) -> bool:
        """Faz uma pesquisa no Google."""
        import urllib.parse
        import webbrowser
        
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            webbrowser.open(url)
            
            self.logger.info(f"🔍 Pesquisando: {query}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao pesquisar: {e}")
            return False
    
    def _youtube(self, query: str) -> bool:
        """Abre o YouTube ou faz uma pesquisa."""
        import webbrowser
        
        try:
            if query:
                # Pesquisar no YouTube
                import urllib.parse
                encoded_query = urllib.parse.quote(query)
                url = f"https://www.youtube.com/results?search_query={encoded_query}"
            else:
                # Abrir YouTube
                url = "https://www.youtube.com"
            
            webbrowser.open(url)
            
            self.logger.info(f"📺 YouTube: {query if query else 'home'}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao abrir YouTube: {e}")
            return False
    
    def _help(self) -> bool:
        """Mostra ajuda."""
        print("\n" + "=" * 60)
        print("COMANDOS DISPONÍVEIS")
        print("=" * 60)
        
        commands = [
            ("Abrir aplicativo", "abrir [nome do app]"),
            ("Fechar aplicativo", "fechar [nome do app]"),
            ("Desligar computador", "desligar"),
            ("Reiniciar computador", "reiniciar"),
            ("Ver hora", "que horas são"),
            ("Ver data", "que dia é hoje"),
            ("Aumentar volume", "aumentar volume"),
            ("Diminuir volume", "diminuir volume"),
            ("Mut", "mutar"),
            ("Pesquisar", "pesquisar [termo]"),
            ("YouTube", "youtube [termo]"),
            ("Ajuda", "ajuda"),
        ]
        
        for desc, cmd in commands:
            print(f"  📌 {desc:20s} : '{cmd}'")
        
        print("=" * 60 + "\n")
        return True
    
    def register_handler(self, intent: str, handler: Callable):
        """
        Registra um handler customizado para um intent.
        
        Args:
            intent: Nome do intent
            handler: Função que recebe entities e retorna bool
        """
        self.custom_handlers[intent] = handler
        self.logger.info(f"Handler registrado para intent: '{intent}'")
    
    def list_intents(self) -> List[str]:
        """Retorna lista de intents disponíveis."""
        return list(self.COMMAND_PATTERNS.values())
