# Carla Simülatörü Şerit Tespiti Projesi

Bu proje, Carla otonom sürüş simülatörünü kullanarak bir şerit tespit sistemi göstermektedir. Amacımız, şerit çizgilerini tespit ederek simülasyondaki bir aracı tespit edilen şeride göre yönlendirmektir.

## Proje Genel Bakış

Proje şu ana bileşenlerden oluşmaktadır:

- **Carla Simülatörü Kurulumu**: Kod, Carla sunucusuna bağlanır, bir harita yükler, bir araç oluşturur ve görüntü yakalamak için araca bir kamera sensörü ekler.
- **Şerit Tespiti**: Araç perspektifinden kamera görüntüleri alınır ve şerit çizgilerini tespit etmek için işlenir.
- **Perspektif Dönüşümü**: Görüntüler, şerit tespitini kolaylaştırmak için kuş bakışı görünümüne dönüştürülür.
- **Kaydırma Penceresi Yöntemi**: İşlenen görüntülerde şerit piksellerini bulmak için kaydırma penceresi algoritması uygulanır.
- **Polinom Uydurma**: Tespit edilen şerit pikselleri, şerit çizgilerini temsil eden ikinci dereceden bir polinoma uydurulur.
- **Eğrilik Hesaplama**: Şerit çizgilerinin eğriliği ve aracın şeritteki pozisyonu hesaplanır.
- **Araç Kontrolü**: Tespit edilen şerit çizgilerine göre aracın direksiyonu ve hızı kontrol edilir ve araç şeridin ortasında tutulur.

## Nasıl Çalışır?

1. **Simülasyon Kurulumu**:
   - Carla istemcisi, `localhost:2000` adresindeki sunucuya bağlanır.
   - Hava durumu ve çevre parametreleri (bulutluluk, yağış vb.) ayarlanır.
   - Simülasyonda belirlenmiş bir noktada araç oluşturulur.

2. **Kamera Kurulumu**:
   - Araca RGB görüntüler yakalayan bir ön kamera sensörü eklenir.

3. **Şerit Tespiti**:
   - Görüntüler, şerit tespiti için kuş bakışı görünümüne dönüştürülür.
   - Kayan pencere(solidi windows) tekniği ile şerit pikselleri belirlenir.
   - Şerit piksellerine ikinci dereceden bir polinom eğrisi uydurulur.
   - Şeridin eğrilik yarıçapı hesaplanarak şeridin ne kadar keskin bir şekilde kıvrıldığı ölçülür.

4. **Araç Kontrolü**:
   - Araç şeride göre konumlandırılır ve uygun direksiyon, gaz ve fren komutları uygulanarak araç şeridin ortasında tutulur.
   - Şerit eğriliğine göre araç sola, sağa döner veya ileri doğru devam eder.

## Projenin Çalıştırılması

1. **Gereksinimler**:
   - Carla Simülatörü (sunucunun `localhost:2000` üzerinde çalıştığından emin olun).
   - Python bağımlılıkları: `cv2`, `carla`, `numpy` ve diğer gerekli kütüphaneler.

2. **Adımlar**:
   - Carla simülatörünü başlatın.
   - Ana Python dosyasını çalıştırın: 
     ```bash
     python main.py
     ```
   - Araç, Carla ortamında sürüşe başlayacak ve şerit tespit sistemi, tespit edilen şerit çizgilerine göre aracı yönlendirecektir.

3. **Durdurma**:
   - Programı durdurmak için OpenCV penceresinde `q` tuşuna basın.

## Önemli Fonksiyonlar

- **get_perspective_matrices()**: Şeritleri daha kolay tespit edebilmek için perspektif dönüşümü uygular.
- **hist()**: Şerit çizgilerini belirlemek için piksel yoğunluğu histogramını hesaplar.
- **find_lane_pixels()**: Kaydırma penceresi yöntemiyle şerit piksel noktalarını tespit eder.
- **fit_poly()**: Tespit edilen şerit piksel noktalarına ikinci dereceden bir polinom eğrisi uydurur.
- **measure_curvature()**: Şerit çizgilerinin eğrilik yarıçapını hesaplar.
- **plot()**: Çıkış görüntüsüne şerit çizgilerini çizer ve şerit tespitine dayalı araç kontrolünü uygular.

---

Carla simülatörü projelerinizde bu şerit tespit sistemini özelleştirip genişletmekten çekinmeyin!


https://github.com/koesan/Serit_tespit_ile_otonom_surus/assets/96130124/8671b396-9942-4727-b576-17d8e283beb7

