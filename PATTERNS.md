Factory Method Uygulaması

Factory Method tasarım örüntüsü, sistemin nesne yaratma sorumluluğunu üstlenen `NotifierFactory` sınıfı içerisinde uygulandı.
Ortak bir `Notifier` arayüzünden türetilen `EmailNotifier`, `SMSNotifier`, `PushNotifier` ve `DiscordNotifier` 
gibi somut sınıfların oluşturulma süreci bu fabrika sınıfına devredildi. `NotifierFactory` içerisindeki `get_notifier` statik metodu, 
if-else zincirleri kullanmak yerine bir sözlük (dictionary) yapısı üzerinden, istemciden gelen metin tabanlı anahtara ("email", "sms" vb.)
göre uygun nesneyi örneklendirerek (instantiate) döndürdü.

Başlangıç kodunda tüm bildirim türlerinin sunucu bağlantıları, 
API doğrulama işlemleri ve gönderim detayları tek bir metodun içine sıkıştırılmıştı. 
Bu durum, hem kodun okunabilirliğini düşürüyor hem de sınıfın her işi yapmaya çalışan bir 
"God Class" haline gelmesine neden oluyordu. Sisteme yeni bir bildirim türü eklenmek istendiğinde mevcut kodun sürekli değiştirilmesi 
gerekiyordu ve bu da hata riskini artırıyordu. Nesne yaratma mantığını asıl iş mantığından (bildirim gönderme işleminden) soyutlamak 
ve sistemi esnek bir yapıya kavuşturmak için Factory Method tercih edildi.

**Ne Kazandık**
Bu örüntünün uygulanmasıyla birlikte, bildirim nesnelerinin nasıl yaratıldığı ile nasıl kullanıldığı (Client) birbirinden tamamen ayrıldı. 
İstemci kod, artık API anahtarları veya sunucu ayarları gibi alt seviye detaylarla ilgilenmeyip sadece fabrikadan bir nesne talep ediyor. 
En büyük kazanım ise Açık/Kapalı Prensibinin (Open/Closed Principle) sisteme entegre edilmesi oldu; ilerleyen süreçte sisteme örneğin bir 
"Slack" bildirimi eklemek istediğimizde, ana sistemin kodunu değiştirmeden yalnızca yeni bir alt sınıf oluşturup fabrikanın sözlüğüne eklememiz yeterli olacak.
