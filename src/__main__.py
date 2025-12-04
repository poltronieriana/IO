import time
from simulacao import Simulador

def main():
    # recebe o tempo total da simulação
    tempo_total = int(input("Defina o tempo total da simulação: "))
   
    # recebe o nome do arquivo de log (ou usa o padrão se não for informado)
    nome_arquivo = input("Defina o nome do arquivo de log (padrão: log_simulacao.txt): ")
    if not nome_arquivo:
        nome_arquivo = "log_simulacao.txt"
    
    arquivo = open(nome_arquivo, "w")
    arquivo.write("=== LOG DE EXECUÇÃO ===\n")
    
    # Cria o simulador com o tempo total
    simulador = Simulador(tempo_total=tempo_total)
    
    # Mapa para mostrar as prioridades em texto
    mapa_prioridade = {
        'teclado': 'Alta',
        'impressora': 'Média',
        'disco': 'Baixa'
    }

    print(f" Simulação iniciada. Log em {nome_arquivo}")

    executando = True

    while executando:
        time.sleep(0.05)  # pequeno atraso só para facilitar a visualização
        
        status = simulador.processar_ciclo()
        dados = simulador.obter_estado_atual()
        tempo = dados['tempo']
        mensagem = ""

        if status == 'INTERRUPCAO_INICIADA':
            # Interrupção detectada, pega o dispositivo envolvido
            obj_inte = dados['interrupcao_ativa']
            
            # Descobre texto da prioridade de acordo com o dispositivo
            prio_texto = mapa_prioridade.get(obj_inte.tipo, "Desconhecida")
            
            mensagem = f"Interrupção: {obj_inte.tipo.capitalize()} - Prioridade: {prio_texto} - Armazenando contexto..."

        elif status == 'TRATANDO_INTERRUPCAO':
            # Sistema está tratando a interrupção
            obj_inte = dados['interrupcao_ativa']
            mensagem = f"Tratando a interrupção do {obj_inte.tipo}..."

        elif status == 'INTERRUPCAO_FINALIZADA':
            # Tratamento concluído, processo principal pode continuar
            mensagem = "Interrupção tratada. Restaurando o contexto do processo principal."
            msg = f"[Tempo {tempo}] - Processo principal retomado."
            print(msg)
            arquivo.write(msg + "\n")

        elif status == 'PROCESSO_EXECUTANDO':
            # Processo principal está rodando
            proc = dados['processo']
            mensagem = f"Processo principal em execução. (Progresso: {proc.progresso_execucao:.1f}%)"

        elif status == 'PROCESSO_FINALIZADO':
            # Processo terminou
            mensagem = "Processo principal finalizado."
            executando = False

        # Exibe e registra a mensagem do ciclo
        if mensagem:
            linha = f"[Tempo {tempo}] - {mensagem}"
            print(linha)
            arquivo.write(linha + "\n")
            arquivo.flush()

        # Avança o tempo da simulação; se não avançar, termina
        if not simulador.avancar_tempo():
            executando = False

    arquivo.close()
    print("\n Fim da simulação.")

if __name__ == "__main__":
    main()
