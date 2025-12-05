# Sistema gerenciador de I/O

Trabalho prático desenvolvido para a disciplina de **Sistemas Operacionais**.

Alunos: 

1. Ana Carolina Poltronieri 
2. Gabriel Gonsalez 
3. Graziela Espindola
4. Lucie Grillo 

## Descrição do Projeto

Este software simula o comportamento do kernel de um Sistema Operacional gerenciando a execução de um processo principal e o tratamento de interrupções de hardware. O simulador implementa:

1.  **Execução de Processo:** Um processo "user-mode" que consome ciclos de CPU.
2.  **Geração de Interrupções:** Dispositivos (Teclado, Impressora, Disco) geram eventos estocásticos.
3.  **Sistema de Prioridades:** Tratamento preemptivo onde:
    * **Teclado:** Prioridade Alta
    * **Impressora:** Prioridade Média
    * **Disco:** Prioridade Baixa
4.  **Troca de Contexto:** Mecanismo de salvar e restaurar o estado (PC e progresso) do processo interrompido.
5.  **Log:** Registro detalhado de eventos em arquivo e console.

## Integrantes e Responsabilidades

* **MEMBRO 1:** Gerenciamento de Contexto.
* **MEMBRO 2:** Escalonador de Interrupções.
* **MEMBRO 3:** Simulação de Dispositivos.
* **MEMBRO 4:** Motor de Simulação, Integração e Sistema de Log.

## Como Executar

1. Certifique-se de que todos os arquivos do projeto estejam na mesma pasta.
2. Execute o arquivo main.py
3. Insira as informações pedidas
4. aguarde o funcionamento
