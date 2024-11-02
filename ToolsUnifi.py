import paramiko
import time
import sys
import csv
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor

class SSHWorker(QThread):
    result_signal = pyqtSignal(str, str, bool, str)  # Envia IP, resultado, sucesso, e comando original

    def __init__(self, ip, username, password, command):
        super().__init__()
        self.ip = ip
        self.username = username
        self.password = password
        self.command = command

    def run(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, username=self.username, password=self.password, timeout=5)
            shell = ssh.invoke_shell()

            # Enviar o comando inicial (set-inform ou info)
            shell.send(self.command + "\n")
            time.sleep(3)
            initial_output = shell.recv(65535).decode("utf-8")

            # Se o comando foi set-inform, executar info em seguida para validação
            if "set-inform" in self.command:
                shell.send("info\n")
                time.sleep(3)
                output = shell.recv(65535).decode("utf-8")
            else:
                output = initial_output

            ssh.close()
            self.result_signal.emit(self.ip, output, True, self.command)  # Sucesso

        except Exception as e:
            self.result_signal.emit(self.ip, f"Erro ao conectar: {e}", False, self.command)  # Falha

class SSHClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.threads = []
        self.data = []  # Armazena dados para exportação CSV

    def init_ui(self):
        self.setWindowTitle("SSH Command Executor")
        self.setGeometry(100, 100, 900, 600)

        ip_label = QLabel("Single IP or IP Range (e.g., 192.168.1.1-254):")
        self.ip_input = QLineEdit()
        self.file_button = QPushButton("Select IP List File")
        self.file_button.clicked.connect(self.select_file)
        self.selected_file_path = None

        username_label = QLabel("Username:")
        self.username_input = QLineEdit("ubnt")
        password_label = QLabel("Password:")
        self.password_input = QLineEdit("ubnt")
        self.password_input.setEchoMode(QLineEdit.Password)

        command_label = QLabel("Command:")
        self.command_box = QComboBox()
        self.command_box.addItems(["INFO", "SET-INFORM"])
        self.command_box.currentIndexChanged.connect(self.set_default_command)

        self.custom_command_input = QLineEdit()
        self.custom_command_input.setDisabled(True)

        self.run_button = QPushButton("Run Command")
        self.run_button.clicked.connect(self.run_command)

        self.export_button = QPushButton("Exportar CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.export_button.setDisabled(True)

        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Adicionamos uma coluna para o status
        self.table.setHorizontalHeaderLabels(["IP", "Modelo", "Versão", "MAC Address", "Hostname", "Uptime", "Status"])
        self.table.setRowCount(0)

        # Caixa de texto para exibir retorno bruto do SSH em tempo real
        self.command_output_display = QTextEdit()
        self.command_output_display.setReadOnly(True)

        # Botão discreto "Dev." no rodapé
        self.dev_button = QPushButton("Dev.")
        self.dev_button.setStyleSheet("background-color: transparent; color: gray; border: none;")  # Aparência discreta
        self.dev_button.clicked.connect(self.show_dev_info)

        # Layouts
        main_layout = QVBoxLayout()
        
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_button)

        username_layout = QHBoxLayout()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        command_layout = QHBoxLayout()
        command_layout.addWidget(command_label)
        command_layout.addWidget(self.command_box)

        custom_command_layout = QHBoxLayout()
        custom_command_layout.addWidget(self.custom_command_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.export_button)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()  # Empurra o botão "Dev." para o canto direito
        footer_layout.addWidget(self.dev_button)

        # Adicionar layouts ao layout principal
        main_layout.addLayout(ip_layout)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(password_layout)
        main_layout.addLayout(command_layout)
        main_layout.addLayout(custom_command_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.command_output_display)
        main_layout.addLayout(footer_layout)  # Adiciona o layout do rodapé

        self.setLayout(main_layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select IP List File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            self.selected_file_path = file_path

    def set_default_command(self):
        """Define o comando padrão com base na seleção."""
        selected_command = self.command_box.currentText()
        if selected_command == "INFO":
            self.custom_command_input.setText("info")
        elif selected_command == "SET-INFORM":
            self.custom_command_input.setText("set-inform http://10.59.104.71:8080/inform")
        self.custom_command_input.setDisabled(False)

    def show_dev_info(self):
        """Exibe informações do desenvolvedor."""
        QMessageBox.information(self, "Informações do Desenvolvedor", "Dev: Marcelo\nContato: marcelo.sobrinho@triatti.com")

    def parse_info_output(self, ip, output, success, original_command):
        """Extrai dados do comando INFO e adiciona à tabela, incluindo o status de sucesso/falha."""
        model = re.search(r"Model:\s+(.+)", output)
        version = re.search(r"Version:\s+(.+)", output)
        mac_address = re.search(r"MAC Address:\s+(.+)", output)
        hostname = re.search(r"Hostname:\s+(.+)", output)
        uptime = re.search(r"Uptime:\s+(.+)", output)
        status_line = re.search(r"Status:\s+(.+)", output)

        status_text = "OK" if success else "Falha"
        status_color = "green" if success else "red"

        # Verifica se o comando foi "set-inform" e valida o status
        if "set-inform" in original_command and status_line and success:
            sent_url = re.search(r"set-inform\s+(http[^\s]+)", original_command)
            if sent_url and sent_url.group(1) in status_line.group(1):
                status_text = "Pendente de Adoção"
                status_color = "orange"

        # Remover quebras de linha e espaços adicionais dos dados extraídos
        row = [
            ip,
            model.group(1).strip() if model else "N/A",
            version.group(1).strip() if version else "N/A",
            mac_address.group(1).strip() if mac_address else "N/A",
            hostname.group(1).strip() if hostname else "N/A",
            uptime.group(1).strip() if uptime else "N/A",
            status_text
        ]
        
        self.data.append(row)  # Adiciona dados à lista para exportação
        self.add_row_to_table(row, status_color)  # Adiciona dados à tabela

    def add_row_to_table(self, row_data, status_color):
        """Adiciona uma linha com dados à tabela e aplica cor ao status."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for col, data in enumerate(row_data):
            item = QTableWidgetItem(data)
            if col == 6:  # Coluna de status
                item.setForeground(QColor(status_color))
            self.table.setItem(row_position, col, item)

    def run_command(self):
        username = self.username_input.text()
        password = self.password_input.text()
        command = self.custom_command_input.text()

        if not command:
            QMessageBox.warning(self, "Error", "Digite um comando personalizado!")
            return

        self.data.clear()  # Limpa os dados da última execução
        self.table.setRowCount(0)  # Limpa a tabela da última execução
        self.command_output_display.clear()  # Limpa a saída de comando bruto anterior
        self.export_button.setDisabled(True)

        ip_input = self.ip_input.text()
        ip_list = []

        if ip_input:
            ip_list = self.parse_ip_range(ip_input)
        elif self.selected_file_path:
            with open(self.selected_file_path, 'r') as file:
                ip_list = [line.strip() for line in file if line.strip()]
        else:
            QMessageBox.warning(self, "Error", "Forneça um intervalo de IP ou selecione um arquivo de lista de IPs!")
            return

        for ip in ip_list:
            thread = SSHWorker(ip, username, password, command)
            thread.result_signal.connect(self.handle_result)
            thread.start()
            self.threads.append(thread)

    def handle_result(self, ip, output, success, original_command):
        # Exibir retorno completo em tempo real na caixa de exibição
        self.command_output_display.append(f"Resultado do comando para {ip}:\n{output}\n")
        
        selected_command = self.command_box.currentText()
        if selected_command == "INFO" or selected_command == "SET-INFORM":
            self.parse_info_output(ip, output, success, original_command)
            self.export_button.setDisabled(False)

    def export_to_csv(self):
        """Exporta os dados da tabela para um arquivo CSV."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar para CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["IP", "Modelo", "Versão", "MAC Address", "Hostname", "Uptime", "Status"])  # Cabeçalho
                writer.writerows(self.data)
            QMessageBox.information(self, "Exportado", "Arquivo CSV exportado com sucesso!")

    def parse_ip_range(self, ip_range):
        start_ip, end = ip_range.rsplit('.', 1)[0], ip_range.rsplit('.', 1)[1]
        if '-' in end:
            start, stop = map(int, end.split('-'))
            return [f"{start_ip}.{i}" for i in range(start, stop + 1)]
        else:
            return [ip_range]

# Inicialização do aplicativo
app = QApplication(sys.argv)
window = SSHClientApp()
window.show()
sys.exit(app.exec_())
