import random

class Interrupcao:
    """
    Classe base que representa uma interrupção gerada por um dispositivo.
    Esta classe é usada pelo Escalonador para gerenciar prioridades.
    """
    def __init__(self, tipo, tempo_geracao, tempo_tratamento):
        self.tipo = tipo  # 'teclado', 'impressora' ou 'disco'
        self.tempo_geracao = tempo_geracao  # Quando a interrupção foi gerada
        self.tempo_tratamento = tempo_tratamento  # Quanto tempo leva para tratar
        self.tempo_inicio_tratamento = None  # Será definido quando começar o tratamento
        self.tempo_fim_tratamento = None  # Será definido quando terminar o tratamento

    def __str__(self):
        return (f"Interrupção [{self.tipo.upper()}] | "
                f"Gerada em: T={self.tempo_geracao} | "
                f"Tempo de tratamento: {self.tempo_tratamento}ut")


class DispositivoBase:
    """
    Classe base abstrata para todos os dispositivos de I/O.
    Define o comportamento comum e a interface que todos os dispositivos devem implementar.
    
    """
    def __init__(self, tipo, prioridade, tempo_min, tempo_max, prob_interrupcao):
        """
        Parâmetros:
        - tipo: string identificadora ('teclado', 'impressora', 'disco')
        - prioridade: descrição textual da prioridade (ex: 'Alta', 'Média', 'Baixa')
        - tempo_min: tempo mínimo de tratamento da interrupção (em unidades de tempo)
        - tempo_max: tempo máximo de tratamento da interrupção (em unidades de tempo)
        - prob_interrupcao: probabilidade de gerar interrupção em cada unidade de tempo (0.0 a 1.0)
        """
        self.tipo = tipo
        self.prioridade = prioridade
        self.tempo_min = tempo_min
        self.tempo_max = tempo_max
        self.prob_interrupcao = prob_interrupcao
        
        # Estatísticas do dispositivo
        self.total_interrupcoes_geradas = 0
        self.interrupcoes_pendentes = 0

    def pode_gerar_interrupcao(self):
        """
        Utiliza RNG (Random Number Generator) para determinar se o dispositivo
        gera uma interrupção neste momento.
        
        Retorna True com probabilidade definida em prob_interrupcao.
        """
        return random.random() < self.prob_interrupcao

    def gerar_tempo_tratamento(self):
        """
        Gera aleatoriamente o tempo que será necessário para tratar a interrupção.
        Usa distribuição uniforme entre tempo_min e tempo_max.
        """
        return random.randint(self.tempo_min, self.tempo_max)

    def tentar_gerar_interrupcao(self, tempo_atual):
        """
        Tenta gerar uma interrupção baseado na probabilidade configurada.
        
        Retorna:
        - Objeto Interrupcao se foi gerada
        - None caso contrário
        """
        if self.pode_gerar_interrupcao():
            tempo_tratamento = self.gerar_tempo_tratamento()
            interrupcao = Interrupcao(self.tipo, tempo_atual, tempo_tratamento)
            
            self.total_interrupcoes_geradas += 1
            self.interrupcoes_pendentes += 1
            
            return interrupcao
        
        return None

    def interrupcao_tratada(self):
        """
        Deve ser chamado quando uma interrupção deste dispositivo foi completamente tratada.
        """
        if self.interrupcoes_pendentes > 0:
            self.interrupcoes_pendentes -= 1

    def obter_estatisticas(self):
        """
        Retorna um dicionário com estatísticas do dispositivo.
        """
        return {
            'tipo': self.tipo,
            'prioridade': self.prioridade,
            'total_interrupcoes': self.total_interrupcoes_geradas,
            'pendentes': self.interrupcoes_pendentes
        }

    def __str__(self):
        return (f"Dispositivo: {self.tipo.upper()} | "
                f"Prioridade: {self.prioridade} | "
                f"Tempo tratamento: {self.tempo_min}-{self.tempo_max}ut | "
                f"Prob: {self.prob_interrupcao*100:.1f}%")


class Teclado(DispositivoBase):
    """
    Dispositivo de Entrada: TECLADO
    - Prioridade: ALTA (usuário aguardando resposta imediata)
    - Tempo de tratamento: RÁPIDO (1-3 unidades de tempo)
    - Frequência: BAIXA (usuário não digita constantemente)
    """
    def __init__(self):
        super().__init__(
            tipo='teclado',
            prioridade='Alta',
            tempo_min=1,
            tempo_max=3,
            prob_interrupcao=0.05  # 5% de chance por unidade de tempo
        )


class Impressora(DispositivoBase):
    """
    Dispositivo de Saída: IMPRESSORA
    - Prioridade: MÉDIA (operação importante mas não urgente)
    - Tempo de tratamento: MODERADO (3-7 unidades de tempo)
    - Frequência: MODERADA 
    """
    def __init__(self):
        super().__init__(
            tipo='impressora',
            prioridade='Média',
            tempo_min=3,
            tempo_max=7,
            prob_interrupcao=0.08  # 8% de chance por unidade de tempo
        )


class Disco(DispositivoBase):
    """
    Dispositivo de Armazenamento: DISCO
    - Prioridade: BAIXA (operação em background)
    - Tempo de tratamento: LENTO (5-12 unidades de tempo)
    - Frequência: ALTA (muitas operações de I/O)
    """
    def __init__(self):
        super().__init__(
            tipo='disco',
            prioridade='Baixa',
            tempo_min=5,
            tempo_max=12,
            prob_interrupcao=0.15  # 15% de chance por unidade de tempo
        )


class GerenciadorDispositivos:
    """
    Classe que centraliza o gerenciamento de todos os dispositivos.
    Facilita a integração com o resto do sistema.
    
    Responsabilidade: Coordenar a geração de interrupções de múltiplos dispositivos.
    """
    def __init__(self):
        # Instancia os três dispositivos
        self.teclado = Teclado()
        self.impressora = Impressora()
        self.disco = Disco()
        
        # Lista para facilitar iteração
        self.dispositivos = [self.teclado, self.impressora, self.disco]

    def verificar_interrupcoes(self, tempo_atual):
        """
        Verifica todos os dispositivos e retorna uma lista de interrupções geradas
        neste instante de tempo.
        
        Esta função PODE retornar múltiplas interrupções simultâneas,
        testando assim o mecanismo de prioridade do Escalonador (Membro 2).
        
        Retorna: lista de objetos Interrupcao
        """
        interrupcoes_geradas = []
        
        for dispositivo in self.dispositivos:
            interrupcao = dispositivo.tentar_gerar_interrupcao(tempo_atual)
            if interrupcao:
                interrupcoes_geradas.append(interrupcao)
        
        return interrupcoes_geradas

    def notificar_interrupcao_tratada(self, tipo_dispositivo):
        """
        Notifica o dispositivo específico que sua interrupção foi tratada.
        """
        for dispositivo in self.dispositivos:
            if dispositivo.tipo == tipo_dispositivo:
                dispositivo.interrupcao_tratada()
                break

    def obter_estatisticas_gerais(self):
        """
        Retorna estatísticas de todos os dispositivos.
        """
        estatisticas = {}
        for dispositivo in self.dispositivos:
            estatisticas[dispositivo.tipo] = dispositivo.obter_estatisticas()
        return estatisticas

    def listar_dispositivos(self):
        """
        Retorna informações formatadas sobre todos os dispositivos.
        """
        info = "=== DISPOSITIVOS DE I/O CADASTRADOS ===\n"
        for dispositivo in self.dispositivos:
            info += f"{dispositivo}\n"
        return info


if __name__ == "__main__":
    print("=== TESTE DO MÓDULO DE DISPOSITIVOS ===\n")
    
    # Cria o gerenciador
    gerenciador = GerenciadorDispositivos()
    
    # Lista dispositivos configurados
    print(gerenciador.listar_dispositivos())
    
    # Simula 20 unidades de tempo
    print("\n=== SIMULAÇÃO DE GERAÇÃO DE INTERRUPÇÕES ===")
    for tempo in range(20):
        interrupcoes = gerenciador.verificar_interrupcoes(tempo)
        
        if interrupcoes:
            print(f"\n[Tempo {tempo}] Interrupções geradas:")
            for int_obj in interrupcoes:
                print(f"  - {int_obj}")
        else:
            print(f"[Tempo {tempo}] Nenhuma interrupção")
    
    # Exibe estatísticas
    print("\n=== ESTATÍSTICAS FINAIS ===")
    stats = gerenciador.obter_estatisticas_gerais()
    for tipo, info in stats.items():
        print(f"{tipo.upper()}: {info['total_interrupcoes']} interrupções geradas")