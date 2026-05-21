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
