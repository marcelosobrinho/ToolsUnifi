# ToolsUnifi

**ToolsUnifi** é uma aplicação em Python com interface gráfica que facilita o gerenciamento de dispositivos UniFi da Ubiquiti. Esta ferramenta permite conexões SSH simultâneas e a execução automatizada de comandos em múltiplos dispositivos UniFi, exibindo os resultados em tempo real.

## 📥 Download

Para baixar o executável diretamente, clique no link abaixo:

- [Baixar ToolsUnifi.exe](https://github.com/marcelosobrinho/ToolsUnifi/releases/download/Produ%C3%A7%C3%A3o/ToolsUnifi.exe)

## ⚙️ Funcionalidades Principais

- **Conexão SSH Automatizada**: Realiza conexões simultâneas com dispositivos UniFi usando credenciais padrão ou personalizadas.
  
- **Execução de Comandos Pré-Definidos**:
  - **Info**: Coleta informações detalhadas do dispositivo, incluindo:
    - Modelo do dispositivo
    - Versão do firmware
    - Endereço MAC
    - Hostname
    - Tempo de atividade (uptime)
  - **Set-Inform**: Configura a URL do controlador UniFi e verifica se o dispositivo está "Pendente de Adoção".

- **Exibição em Tempo Real**: Mostra o retorno dos comandos em tempo real, com status colorido para fácil acompanhamento:
  - Verde para sucesso
  - Vermelho para falha
  - Amarelo para "Pendente de Adoção"

- **Exportação de Dados**: Exporta os resultados para um arquivo CSV, facilitando a documentação e análise.

- **Gerenciamento de IPs**: Suporta:
  - IP único
  - Intervalo de IPs (ex.: `192.168.1.1-192.168.1.10`)
  - Importação de listas de IPs de arquivos `.txt`

- **Interface Intuitiva**: Desenvolvida com `PyQt5`, a interface gráfica é fácil de usar e inclui um botão discreto para informações de contato do desenvolvedor.

## 🎯 Público-Alvo

**ToolsUnifi** é ideal para administradores de rede que buscam uma solução centralizada e prática para o gerenciamento de dispositivos UniFi, automatizando tarefas repetitivas e oferecendo uma visão detalhada dos dispositivos da rede.

## 🚀 Como Usar

1. **Baixe o executável** pelo link acima ou clone o repositório e execute o código-fonte diretamente.
2. **Instale as dependências** (se estiver executando o código-fonte):
   ```bash
   pip install -r requirements.txt
