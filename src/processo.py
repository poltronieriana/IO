class Processo:
    """
    Representa um processo no sistema operacional simulado.
    """

    def __init__(self, pid):
        self.estado = 'pronto' 
        self.pid = pid
        self.programa_contador = 0
        self.progresso_execucao = 0
        self.ponto_pilha = 0

        def executa_processo(self):
            """
                Simula a execução do processo incrementando o progresso de execução.
            """
            if self.estado == 'pronto':
                if self.progresso_execucao < 100:
                    self.progresso_execucao += 1
                    if self.progresso_execucao >+ 100:
                        self.estado = 'finalizado'
                self.programa_contador += 1
                self.estado = 'pronto'

                return True # execução bem sucedida
            return False # processo não está pronto para execução

    def backup_processo(self):

        """
        Salva o estado atual do processo em um backup no PBC 
        """
        pass

    def restaura_processo(self):
        pass

    def __str__(self):
        pass