from abc import ABC, abstractmethod

# ==========================================
# FAZ 1: CREATIONAL ÖRÜNTÜ (FACTORY METHOD)
# ==========================================

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str):
        pass

class EmailNotifier(Notifier):
    def send(self, message: str, recipient: str):
        print(f"[BAĞLANTI] SMTP sunucusuna bağlanılıyor...")
        print(f"[GÖNDERİM] Email başarıyla gönderildi -> Alıcı: {recipient}")
        print(f"[İÇERİK] {message}\n")

class SMSNotifier(Notifier):
    def send(self, message: str, recipient: str):
        print(f"[KİMLİK DOĞRULAMA] SMS API Anahtarı doğrulanıyor...")
        print(f"[GÖNDERİM] SMS başarıyla gönderildi -> Tel: {recipient}")
        print(f"[İÇERİK] {message}\n")

class DiscordNotifier(Notifier):
    def send(self, message: str, recipient: str):
        print("[BAĞLANTI] Discord Webhook URL'sine istek atılıyor...")
        print(f"[GÖNDERİM] Discord kanalına mesaj atıldı -> {recipient}")
        print(f"[İÇERİK] {message}\n")
        
# ==========================================
# FAZ 2: STRUCTURAL ÖRÜNTÜLER (ADAPTER & DECORATOR)
# ==========================================
# --- Adapter Pattern ---
class ExternalWhatsAppAPI:
    def dispatch_message(self, phone_number: str, text: str):
        print(f"[WHATSAPP API] Dış sunucuya iletiliyor: {phone_number} -> {text}\n")

class WhatsAppAdapter(Notifier):
    def __init__(self):
        self.whatsapp_service = ExternalWhatsAppAPI()

    def send(self, message: str, recipient: str):
        print("[ADAPTER] İç sistem formatı WhatsApp formatına dönüştürülüyor...")
        self.whatsapp_service.dispatch_message(recipient, message)

# --- Decorator Pattern ---
class NotifierDecorator(Notifier):
    def __init__(self, wrapped_notifier: Notifier):
        self._wrapped_notifier = wrapped_notifier

    def send(self, message: str, recipient: str):
        self._wrapped_notifier.send(message, recipient)

class EncryptedNotifier(NotifierDecorator):
    def send(self, message: str, recipient: str):
        print("[ŞİFRELEME] Mesaj içeriği AES-256 ile şifrelendi.")
        encrypted_message = f"***ENCRYPTED[{message}]***"
        super().send(encrypted_message, recipient)

class NotifierFactory:
    @staticmethod
    def get_notifier(alert_type: str) -> Notifier:
        notifiers = {
            "email": EmailNotifier,
            "sms": SMSNotifier,
            "discord": DiscordNotifier,
            "whatsapp": WhatsAppAdapter
        }
        notifier_class = notifiers.get(alert_type)
        if not notifier_class:
            raise ValueError(f"[HATA] '{alert_type}' adında bilinmeyen bir bildirim tipi!\n")
        return notifier_class()
        
# ==========================================
# FAZ 3: BEHAVIORAL ÖRÜNTÜLER (STRATEGY & OBSERVER)
# ==========================================

# --- Strategy Pattern (Açık/Kapalı - OCP Prensibi Gösterimi) ---
class MessageStrategy(ABC):
    @abstractmethod
    def format_message(self, message: str) -> str:
        pass

class PlainTextStrategy(MessageStrategy):
    def format_message(self, message: str) -> str:
        return f"[DÜZ METİN] {message}"

class HTMLStrategy(MessageStrategy):
    def format_message(self, message: str) -> str:
        return f"<html><body><p><b>[UYARI]</b> {message}</p></body></html>"

class JSONStrategy(MessageStrategy):
    def format_message(self, message: str) -> str:
        return f'{{"status": "alert", "message": "{message}"}}'

# --- Observer Pattern ---
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, message: str):
        pass

class SystemMonitor:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, event_type: str, message: str):
        for observer in self._observers:
            observer.update(event_type, message)

    def trigger_event(self, event_type: str, message: str):
        print(f"\n==========================================")
        print(f"[MONİTÖR] Yeni Sistem Olayı: {event_type}")
        print(f"==========================================")
        self.notify(event_type, message)

class ITDepartmentObserver(Observer):
    def __init__(self, notifier: Notifier, strategy: MessageStrategy):
        self.notifier = notifier
        self.strategy = strategy

    def update(self, event_type: str, message: str):
        if event_type == "CRITICAL":
            formatted_msg = self.strategy.format_message(message)
            self.notifier.send(formatted_msg, "it-acil@proje-team.local")

class LoggingObserver(Observer):
    def __init__(self, notifier: Notifier, strategy: MessageStrategy):
        self.notifier = notifier
        self.strategy = strategy

    def update(self, event_type: str, message: str):
        formatted_msg = self.strategy.format_message(f"LOG KAYDI: {message}")
        self.notifier.send(formatted_msg, "#sistem-loglari")


if __name__ == "__main__":
    monitor = SystemMonitor()
    sms_notifier = NotifierFactory.get_notifier("sms")
    discord_notifier = NotifierFactory.get_notifier("discord")
    
    secure_sms = EncryptedNotifier(sms_notifier)

    html_format = HTMLStrategy()
    json_format = JSONStrategy()

    it_observer = ITDepartmentObserver(notifier=secure_sms, strategy=html_format)
    log_observer = LoggingObserver(notifier=discord_notifier, strategy=json_format)

    monitor.attach(it_observer)
    monitor.attach(log_observer)

    monitor.trigger_event("INFO", "Sistem yedeklemesi başarıyla tamamlandı.")

    monitor.trigger_event("CRITICAL", "Veritabanı bağlantısı koptu!")

