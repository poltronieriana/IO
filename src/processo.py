class Processo:
    """
    Representa o Process Control Block (PCB) e o processo no sistema operacional simulado.
    Responsabilidade do Membro 1: Gerenciamento de Contexto.
    """

    def __init__(self, pid):
        self.pid = pid
        # Registradores
        self.programa_contador = 0  # PC
        self.ponto_pilha = 0        # SP (Ponto de Pilha)
        
        # Estado de Execução
        self.progresso_execucao = 0.0 
        self.estado = 'RODANDO'     # Estados: RODANDO, ESPERA, FINALIZADO

    def executa_processo(self):
        """
        Simula a execução do processo incrementando o PC e o progresso.
        O processo só executa se estiver no estado RODANDO.
        """
        if self.estado == 'RODANDO':
            if self.progresso_execucao < 100.0:
                self.progresso_execucao += 1.0 # Avança 1.0 por unidade de tempo
            
            # Incrementa o PC
            self.programa_contador += 1
            
            # Verifica se o processo terminou
            if self.progresso_execucao >= 100.0:
                self.estado = 'FINALIZADO'
            
            return True # Execução bem sucedida 
        
        return False # Processo não está em RODANDO

    def backup_processo(self):
        """
        Salva o estado atual do processo e o move para o estado de ESPERA.
        """
        if self.estado == 'RODANDO':
            self.estado = 'ESPERA' # 1. Atualiza o estado para indicar que foi interrompido
            # 2. Retorna os valores do contexto salvo 
            # Os atributos do processo já guardam o estado.
            return self.programa_contador, self.progresso_execucao
        
        return None, None # Se não estava rodando, não  salva

    def restaura_processo(self, pc_retorno, progresso_retorno):
        """
        Restaura o estado do PCB e o move de volta para o estado de RODANDO.
        """
        if self.estado != 'FINALIZADO':
            # 1. Restaura os valores (PC e Progresso)
            self.programa_contador = pc_retorno
            self.progresso_execucao = progresso_retorno
            
            # 2. Atualiza o estado para retomar a execução
            self.estado = 'RODANDO'
            return True
        return False

    # representação pro Membro 4
    def __str__(self):
        """Retorna o estado formatado, essencial para o log."""
        return (f"PID: {self.pid} | Estado: {self.estado:^10} | "
                f"PC: {self.programa_contador:04} | Progresso: {self.progresso_execucao:.1f}%")