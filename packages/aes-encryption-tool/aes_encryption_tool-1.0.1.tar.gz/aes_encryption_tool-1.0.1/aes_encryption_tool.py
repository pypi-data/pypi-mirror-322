import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QComboBox, QMessageBox, QGraphicsOpacityEffect, QProgressBar, QHBoxLayout, QGroupBox
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, pyqtSignal
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password, salt):
    """Derive a key from the given password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_decrypt_file(input_file, output_file, password, mode, progress_callback):
    """Encrypt or decrypt a file using AES with the provided password."""
    try:
        if mode == 'encrypt':
            salt = os.urandom(16)
            iv = os.urandom(16)
            key = derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
                outfile.write(salt)
                outfile.write(iv)
                total_size = os.path.getsize(input_file)
                processed = 0
                while chunk := infile.read(1024):
                    outfile.write(encryptor.update(chunk))
                    processed += len(chunk)
                    progress_callback(int((processed / total_size) * 100))
                outfile.write(encryptor.finalize())

        elif mode == 'decrypt':
            with open(input_file, 'rb') as infile:
                salt = infile.read(16)
                iv = infile.read(16)
                key = derive_key(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                total_size = os.path.getsize(input_file) - 32
                processed = 0

                with open(output_file, 'wb') as outfile:
                    while chunk := infile.read(1024):
                        outfile.write(decryptor.update(chunk))
                        processed += len(chunk)
                        progress_callback(int((processed / total_size) * 100))
                    outfile.write(decryptor.finalize())
        else:
            raise ValueError("Invalid mode! Use 'encrypt' or 'decrypt'.")

    except FileNotFoundError:
        raise FileNotFoundError("The input file does not exist.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

class EncryptDecryptThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_file, output_file, password, mode):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.password = password
        self.mode = mode

    def run(self):
        try:
            encrypt_decrypt_file(self.input_file, self.output_file, self.password, self.mode, self.progress.emit)
            self.finished.emit(True, f"File {self.mode}ed successfully!")
        except Exception as e:
            self.finished.emit(False, str(e))

class AESApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Set background color and styling
        self.setStyleSheet("""
            background-color: #282c34;
            color: #ffffff;
            font-family: Arial, sans-serif;
        """)

        # Input file
        input_group = QGroupBox("Input File")
        input_layout = QHBoxLayout()
        self.input_file_edit = QLineEdit(self)
        self.input_file_edit.setPlaceholderText("Select input file")
        self.input_file_button = QPushButton("Browse", self)
        self.input_file_button.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.input_file_edit)
        input_layout.addWidget(self.input_file_button)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Output file
        output_group = QGroupBox("Output File")
        output_layout = QHBoxLayout()
        self.output_file_edit = QLineEdit(self)
        self.output_file_edit.setPlaceholderText("Select output file")
        self.output_file_button = QPushButton("Browse", self)
        self.output_file_button.clicked.connect(self.select_output_file)
        output_layout.addWidget(self.output_file_edit)
        output_layout.addWidget(self.output_file_button)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Password
        password_group = QGroupBox("Password")
        password_layout = QVBoxLayout()
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)  # Mask input for security
        self.password_edit.setPlaceholderText("Enter password")
        self.password_strength_label = QLabel("Password Strength: ")
        self.password_edit.textChanged.connect(self.check_password_strength)
        password_layout.addWidget(self.password_edit)
        password_layout.addWidget(self.password_strength_label)
        password_group.setLayout(password_layout)
        layout.addWidget(password_group)

        # Mode selection
        mode_group = QGroupBox("Mode")
        mode_layout = QVBoxLayout()
        self.mode_combo = QComboBox(self)
        self.mode_combo.addItems(["encrypt", "decrypt"])
        mode_layout.addWidget(self.mode_combo)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_process)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle('AES Encryption/Decryption Tool')
        self.setGeometry(300, 300, 600, 400)

    def select_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "All Files (*)")
        if file:
            self.input_file_edit.setText(file)

    def select_output_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "All Files (*)")
        if file:
            self.output_file_edit.setText(file)

    def check_password_strength(self):
        password = self.password_edit.text()
        strength = "Weak"
        if len(password) > 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password):
            strength = "Medium"
        if len(password) > 12 and any(c in "!@#$%^&*()-_+=<>?/|{}[]~" for c in password):
            strength = "Strong"
        self.password_strength_label.setText(f"Password Strength: {strength}")

    def start_process(self):
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()
        password = self.password_edit.text().strip()
        mode = self.mode_combo.currentText()

        if not input_file or not output_file or not password:
            QMessageBox.warning(self, "Missing Information", "Please provide all inputs.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Weak Password", "Password must be at least 8 characters long.")
            return

        self.thread = EncryptDecryptThread(input_file, output_file, password, mode)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.process_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def process_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        self.progress_bar.setValue(0)

def main():
    app = QApplication(sys.argv)
    ex = AESApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

