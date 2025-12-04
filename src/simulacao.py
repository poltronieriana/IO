from processo import Processo
from dispositivos import GerenciadorDispositivos, Interrupcao
from escalonador import Escalonador

class Simulador:
    """Gerencia o fluxo principal da simulação"""
    
    def __init__(self, tempo_total, seed=None):
        """Inicializa os componentes da simulação"""
        
        # Instância dos componentes principais
        self.processo = Processo(pid=1)
        self.dispositivos = GerenciadorDispositivos()
        self.escalonador = Escalonador()
        
        # Informações de tempo e estados
        self.tempo_atual = 0
        self.tempo_total = tempo_total
        self.interrupcao_ativa = None
        self.tempo_restante = 0
        
        # Informações da simulação
        self.info = {
            'tempo_processo': 0,
            'tempo_interrupcoes': 0,
            'total_interrupcoes': 0,
            'por_tipo': {'teclado': 0, 'impressora': 0, 'disco': 0}
        }
    
    def gerar_interrupcoes(self):
        """Verifica se algum dispositivo gerou interrupções neste ciclo"""
        novas = self.dispositivos.verificar_interrupcoes(self.tempo_atual)
        for interrupcao in novas:
            # Coloca cada nova interrupção na fila do escalonador
            self.escalonador.adicionar_interrupcao(interrupcao)
        return novas
    
    def processar_ciclo(self):
        """Executa um passo da simulação"""
        
        # Caso haja interrupção sendo tratada
        if self.interrupcao_ativa:
            self.tempo_restante -= 1
            self.info['tempo_interrupcoes'] += 1
            
            # Se tempo do tratamento acabou
            if self.tempo_restante <= 0:
                self.finalizar_tratamento()
                return 'INTERRUPCAO_FINALIZADA'
            return 'TRATANDO_INTERRUPCAO'
        
        # Gera possíveis novas interrupções
        self.gerar_interrupcoes()
        
        # Se existir interrupção pendente, inicia tratamento
        if self.escalonador.tem_interrupcao_pendente():
            interrupcao = self.escalonador.obter_proxima_interrupcao()
            if interrupcao:
                self.iniciar_tratamento(interrupcao)
                return 'INTERRUPCAO_INICIADA'
        
        # Caso contrário, o processo principal continua executando
        if self.processo.executa_processo():
            self.info['tempo_processo'] += 1
            return 'PROCESSO_EXECUTANDO'
        
        # Se o processo terminou, finaliza
        return 'PROCESSO_FINALIZADO'
    
    def iniciar_tratamento(self, interrupcao):
        """Começa o tratamento de uma interrupção"""
        
        # Guarda as informações do processo
        self.processo.backup_processo()
        
        # Configura o estado atual
        self.interrupcao_ativa = interrupcao
        self.tempo_restante = interrupcao.tempo_tratamento
        
        # Atualiza estatísticas
        self.info['total_interrupcoes'] += 1
        self.info['por_tipo'][interrupcao.tipo] += 1
        
        # Marca o início do tratamento
        interrupcao.tempo_inicio_tratamento = self.tempo_atual
    
    def finalizar_tratamento(self):
        """Conclui o tratamento da interrupção"""
        if not self.interrupcao_ativa:
            return
        
        # Notifica o dispositivo de que a interrupção foi tratada
        self.dispositivos.notificar_interrupcao_tratada(self.interrupcao_ativa.tipo)
        
        # Restaura o contexto do processo
        self.processo.restaura_processo(
            self.processo.programa_contador,
            self.processo.progresso_execucao
        )
        
        # Limpa estado interno
        self.interrupcao_ativa.tempo_fim_tratamento = self.tempo_atual
        self.interrupcao_ativa = None
        self.tempo_restante = 0
    
    def avancar_tempo(self):
        """Avança o tempo global da simulação"""
        self.tempo_atual += 1
        # Continua enquanto houver tempo e o processo não estiver encerrado
        return self.tempo_atual <= self.tempo_total and self.processo.estado != 'FINALIZADO'
    
    def obter_estado_atual(self):
        """Retorna as informações do estado atual"""
        return {
            'tempo': self.tempo_atual,
            'processo': self.processo,
            'interrupcao_ativa': self.interrupcao_ativa,
            'fila_tamanho': self.escalonador.ver_tamanho_fila(),
            'info': self.info.copy()
        }
