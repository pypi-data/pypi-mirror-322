"""
Created on 07/04/2024
Author: D-one
"""
import importlib.util
import requests
from typing import Optional


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram"""
    
    def __init__(self, secrets_path: str = None):
        """
        Инициализация с данными из secrets файла
        
        Args:
            secrets_path: Путь к файлу с секретами
        """
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            
            # Получаем учетные данные из secrets
            telegram_cred = secrets.telegram_cred
            self.token = telegram_cred.get('token')
            self._chat_id = telegram_cred.get('admin_chat_id')
        else:
            raise ValueError("secrets_path must be provided")
    
    @property
    def chat_id(self) -> Optional[str]:
        """Получение chat_id"""
        return self._chat_id
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Отправка сообщения в Telegram
        
        Args:
            message: Текст сообщения
            parse_mode: Режим форматирования (HTML/Markdown)
            
        Returns:
            bool: True если сообщение успешно отправлено
        """
        if not self.chat_id:
            print("Error: No chat_id available")
            return False
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=data)
            return response.ok
        except Exception as e:
            print(f"Error sending telegram message: {e}")
            return False

    def send_success(self, task_name: str, details: str = "") -> bool:
        """Отправка сообщения об успешном выполнении задачи"""
        message = f"✅ <b>{task_name}</b>\n{details}"
        return self.send_message(message)
    
    def send_error(self, task_name: str, error_details: str) -> bool:
        """Отправка сообщения об ошибке"""
        message = f"❌ <b>{task_name}</b>\n{error_details}"
        return self.send_message(message)
