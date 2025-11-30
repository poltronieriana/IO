class Escalonador:
    """
    Classe responsável por gerenciar a fila de interrupções e aplicar a lógica de
    prioridade (Teclado > Impressora > Disco).
    """

    def __init__(self):
        # Lista que armazena as interrupções pendentes
        self.fila_interrupcoes = []
        
        # Mapa de prioridades: Valores numéricos maiores indicam maior prioridade
        self.prioridades = {
            'teclado': 3,
            'impressora': 2,
            'disco': 1
        }

    def adicionar_interrupcao(self, interrupcao):
        """
        Recebe um objeto de interrupção e o adiciona à fila de espera.
        Realiza validação para garantir que o objeto possui o atributo 'tipo' necessário.
        """
        # Validação: Garante que o objeto recebido é compatível com o escalonador
        if not hasattr(interrupcao, 'tipo'):
            raise ValueError("Erro de Integração: O objeto de interrupção deve possuir o atributo 'tipo'.")
            
        # Verifica se o tipo é conhecido pelo sistema de prioridades
        if interrupcao.tipo not in self.prioridades:
            print(f"   [Aviso] Tipo de interrupção '{interrupcao.tipo}' desconhecido. Será tratado com prioridade mínima.")

        self.fila_interrupcoes.append(interrupcao)

    def tem_interrupcao_pendente(self):
        """
        Retorna True se houver interrupções na fila aguardando processamento.
        """
        return len(self.fila_interrupcoes) > 0

    def obter_proxima_interrupcao(self):
        """
        Reordena a fila com base na prioridade e retorna a interrupção mais prioritária.
        Resolve conflitos de interrupções simultâneas garantindo que a de maior valor seja atendida primeiro.
        """
        if not self.fila_interrupcoes:
            return None

        # Ordena a lista in-place.
        # A chave de ordenação busca o valor numérico no dicionário 'prioridades'.
        # reverse=True garante que a maior prioridade fique no índice 0.
        self.fila_interrupcoes.sort(
            key=lambda x: self.prioridades.get(x.tipo, 0), 
            reverse=True
        )

        # Remove e retorna o primeiro elemento (o de maior prioridade)
        proxima = self.fila_interrupcoes.pop(0)
        
        return proxima

    def ver_tamanho_fila(self):
        """
        Retorna a quantidade de interrupções atualmente na fila.
        """
        return len(self.fila_interrupcoes)