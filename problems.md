class NotificationSystem:
    def __init__(self):
        self.email_smtp_server = "smtp.proje-team.local"
        self.sms_api_key = "PROJE-SMS-KEY-9988"
        self.push_auth_token = "firebase-token-12345"

    def send_alert(self, alert_type, message, recipient):
        if alert_type == "email":
            print(f"[BAĞLANTI] {self.email_smtp_server} sunucusuna bağlanılıyor...")
            print("[FORMAT] Mesaj HTML formatına çevriliyor...")
            print(f"[GÖNDERİM] Email başarıyla gönderildi -> Alıcı: {recipient}")
            print(f"[İÇERİK] <h1>{message}</h1>\n")

        elif alert_type == "sms":
            print(f"[KİMLİK DOĞRULAMA] SMS API Anahtarı doğrulanıyor: {self.sms_api_key}")
            if len(message) > 160:
                print("[UYARI] Mesaj 160 karakterden uzun, bölünüyor...")
                message = message[:157] + "..."
            print(f"[GÖNDERİM] SMS başarıyla gönderildi -> Tel: {recipient}")
            print(f"[İÇERİK] {message}\n")

        elif alert_type == "push":
            print(f"[BAĞLANTI] Firebase sunucusuna {self.push_auth_token} ile bağlanılıyor...")
            print("[FORMAT] JSON payload'u oluşturuluyor...")
            print(f"[GÖNDERİM] Mobil cihaza Push Notification iletildi -> Cihaz: {recipient}")
            print(f"[İÇERİK] {message}\n")

        elif alert_type == "discord":
            print("[BAĞLANTI] Discord Webhook URL'sine istek atılıyor...")
            print(f"[GÖNDERİM] Discord kanalına mesaj atıldı -> {recipient}")
            print(f"[İÇERİK] {message}\n")

        else:
            print(f"[HATA] '{alert_type}' adında bilinmeyen bir bildirim tipi!\n")



if __name__ == "__main__":
    system = NotificationSystem()

    system.send_alert("email", "Haftalık sistem raporu hazır.", "admin@proje-team.com")
    system.send_alert("sms", "ACİL: Sunucu sıcaklığı kritik seviyede!", "+905551234567")
    system.send_alert("push", "Otomatik yedekleme aktifleştirildi.", "sistem_ekrani_01")
    system.send_alert("discord", "Yeni log kayıtları sisteme yüklendi.", "#yazilim-loglari")

    system.send_alert("telegram", "Bu bildirim gitmeyecek.", "@kullanici")


Tespit edilen tasarım sorunları

1. Tek Sorumluluk İhlali (God Class)
NotificationSystem sınıfı hem yapılandırmayı, hem kimlik doğrulamayı, hem formatlamayı, hem de her kanal için gönderim mantığını tek başına yönetiyor. Bir değişiklik her şeyi bozabilir.
Çözüm:Strategy Pattern— her kanal kendi sınıfına ayrılmalı.

3. Açık/Kapalı İlkesi İhlali (if-else zinciri)
Yeni bir kanal (ör. Telegram) eklemek için mevcut send_alert metodunu değiştirmek zorundayız. Kodun genişletilmesi, değiştirilmesine yol açıyor.
Çözüm:Strategy + Factory Pattern— yeni kanal = yeni sınıf, eski kod değişmiyor.

5. Sabit Kodlanmış Kimlik Bilgileri
API anahtarları ve token'lar doğrudan sınıf içine yazılmış: "PROJE-SMS-KEY-9988", "firebase-token-12345". Bu hem güvenlik açığı hem de esneklik sorunudur.
Çözüm:Dependency Injectionveya ortam değişkenleri ile dışarıdan geçirilmeli.

7. Soyutlama Eksikliği (Ortak Arayüz Yok)
Her bildirim tipi farklı mantıkla çalışıyor ama bunları birleştiren ortak bir sözleşme (interface/soyut sınıf) yok. Tip güvenliği ve öngörülebilirlik sıfır.
Çözüm:Strategy Pattern— soyut birNotifierarayüzü tanımlanmalı.

9. Nesne Oluşturma Mantığı İç İçe
İstemci kod, "email" gibi string'lerle doğrudan hangi sistemi kullanacağına karar vermek zorunda. Somut sınıflar arasındaki bağımlılık yüksek.
Çözüm:Factory Pattern— nesne oluşturma ayrı bir fabrika sınıfına taşınmalı.
