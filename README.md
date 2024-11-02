
Aqui está um README.md bem organizado e visualmente agradável para o projeto ToolsUnifi:

ToolsUnifi
ToolsUnifi é uma aplicação em Python com interface gráfica que facilita o gerenciamento de dispositivos UniFi da Ubiquiti. Ela permite realizar conexões SSH em múltiplos dispositivos UniFi simultaneamente, executando comandos de forma automatizada e exibindo os resultados em tempo real.

📥 Download
Para fazer o download direto do executável, clique no link abaixo:

Baixar ToolsUnifi.exe
Nota: Substitua URL_DIRETA_PARA_TOOLSUNIFI.EXE pela URL copiada do link direto do .exe após o envio do arquivo para o repositório.

⚙️ Funcionalidades Principais
Conexão SSH Automatizada: Conecta-se a múltiplos dispositivos UniFi automaticamente, utilizando credenciais padrão ou personalizadas.

Execução de Comandos Pré-Definidos:

Info: Coleta informações detalhadas do dispositivo, incluindo modelo, versão, endereço MAC, hostname e uptime.
Set-Inform: Configura a URL do controlador UniFi para o dispositivo e verifica o status de "Pendente de Adoção".
Exibição em Tempo Real: Mostra o retorno dos comandos em tempo real, com status de sucesso ou falha em cores intuitivas, facilitando o monitoramento do processo.

Exportação de Dados: Exporta os resultados para um arquivo CSV, incluindo dados do dispositivo e status, ideal para documentação e análise.

Gerenciamento de IPs: Permite o uso de um IP único, intervalo de IPs, ou importação de uma lista de IPs, proporcionando flexibilidade para redes de diferentes tamanhos.

Interface Intuitiva: Interface gráfica fácil de usar, com botão discreto para informações do desenvolvedor e opções de configuração personalizáveis.

🎯 Público-Alvo
ToolsUnifi é ideal para administradores de rede que buscam uma solução centralizada e prática para o gerenciamento de dispositivos UniFi. A ferramenta simplifica tarefas repetitivas e oferece uma visão detalhada e organizada dos dispositivos na rede.

🚀 Instruções para Execução
Baixe o executável pelo link acima ou clone o repositório e execute o script Python diretamente.
Instale as dependências (se estiver executando o código-fonte):
bash
Copiar código
pip install -r requirements.txt
Inicie a aplicação:
No Windows: Execute o arquivo .exe ou rode o script ToolsUnifi.py em um terminal com Python.
📂 Estrutura do Projeto
bash
Copiar código
|-- ToolsUnifi.py           # Código principal do aplicativo
|-- ToolsUnifi.exe          # Executável para download
|-- requirements.txt        # Dependências do projeto
|-- triat.ico               # Ícone personalizado
|-- dist/                   # Pasta gerada com o executável
|-- build/                  # Pasta gerada temporariamente durante a compilação
🛠 Tecnologias Utilizadas
Python: Linguagem de programação principal.
Paramiko: Para conexões SSH.
PyQt5: Para a interface gráfica.
👨‍💻 Desenvolvedor
Marcelo Sobrinho
📧 marcelo.sobrinho@triatti.com
