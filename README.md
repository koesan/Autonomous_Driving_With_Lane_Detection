# Lane Detection Project with Carla Simulator (Carla Simülatörü Şerit Tespiti Projesi).

***

This project demonstrates a lane detection system using the Carla autonomous driving simulator. The goal is to detect lane lines and steer the vehicle within the detected lane.

***
Bu proje, Carla otonom sürüş simülatörünü kullanarak bir şerit tespit sistemi göstermektedir. Amacımız, şerit çizgilerini tespit ederek simülasyondaki bir aracı tespit edilen şeride göre yönlendirmektir.

***
## Project Overview

The project consists of these main components:

- **Carla Simulator Setup**: The code connects to the Carla server, loads a map, spawns a vehicle, and attaches a camera sensor to capture images.
- **Lane Detection**: Camera images from the vehicles perspective are processed to detect lane markings.
- **Perspective Transformation**: images are transformed into a bird-eye view to make lane detection easier.
- **Sliding Window Technique**: A sliding window algorithm is applied to locate lane pixels in the processed images.
- **Polynomial Fitting**: Detected lane pixels are fitted to a second-degree polynomial representing lane lines.
- **Curvature Calculation**: curvature of the lane lines and the vehicle’s position within lane are calculated.
- **Vehicle Control**: steering and speed of vehicle are controlled based on detected lane to keep the vehicle centered.

***
## Proje Genel Bakış

Proje şu ana bileşenlerden oluşmaktadır:

- **Carla Simülatörü Kurulumu**: Kod, Carla sunucusuna bağlanır, bir harita yükler, bir araç oluşturur ve görüntü yakalamak için araca bir kamera sensörü ekler.
- **Şerit Tespiti**: Araç perspektifinden kamera görüntüleri alınır ve şerit çizgilerini tespit etmek için işlenir.
- **Perspektif Dönüşümü**: Görüntüler, şerit tespitini kolaylaştırmak için kuş bakışı görünümüne dönüştürülür.
- **Kaydırma Penceresi Yöntemi**: İşlenen görüntülerde şerit piksellerini bulmak için kaydırma penceresi algoritması uygulanır.
- **Polinom Uydurma**: Tespit edilen şerit pikselleri, şerit çizgilerini temsil eden ikinci dereceden bir polinoma uydurulur.
- **Eğrilik Hesaplama**: Şerit çizgilerinin eğriliği ve aracın şeritteki pozisyonu hesaplanır.
- **Araç Kontrolü**: Tespit edilen şerit çizgilerine göre aracın direksiyonu ve hızı kontrol edilir ve araç şeridin ortasında tutulur.

***

## How It Works?

1. **Simulation Setup**:
   - The Carla client connects to the server at `localhost:2000`.
   - Weather and environmental conditions (cloudiness, precipitation, etc.) are set.
   - A vehicle is spawned at a predefined point in the simulation.

2. **Camera Setup**:
   - A RGB camera sensor is attached to vehicle to capture front-facing images.

3. **Lane Detection**:
   - images are transformed into a top-down view.
   - Sliding window method is used to identify lane pixels.
   - A second-degree polynomial curve is fitted to the lane pixels.
   - The curvature of lane is calculated, showing how sharply lane is curving.

4. **Vehicle Control**:
   - Based on the detected lane, the vehicles position is adjusted.
   - vehicle receives steering, throttle, and brake commands to stay centered in lane.
   - vehicle will turn left, right, or go straight based on lane curvature.

***
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

***
## How To Run

1. **Requirements**:
   - Carla Simulator (Make sure the server is running on `localhost:2000`).
   - Python dependencies: `cv2`, `carla`, `numpy`, and other necessary libraries.

2. **Steps**:
   - Start the Carla simulator.
   - Run the main Python script:
     ```bash
     python main.py
     ```
   - vehicle will start driving in the Carla environment, and lane detection system will guide it based on detected lane lines.

3. **Stopping the Program**:
   - Press `q` on the OpenCV window to stop the program.

***

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

***

## Key Functions

- **get_perspective_matrices()**: Applies perspective transformation to make lane detection easier.
- **hist()**: Computes a pixel intensity histogram to identify lane lines.
- **find_lane_pixels()**: Detects lane pixel points using a sliding window technique.
- **fit_poly()**: Fits a second-degree polynomial curve to the detected lane pixel points.
- **measure_curvature()**: Calculates the curvature off lane lines.
- **plot()**: Draws lane lines on the output image and applies vehicle control based on lane detection.

***

## Önemli Fonksiyonlar

- **get_perspective_matrices()**: Şeritleri daha kolay tespit edebilmek için perspektif dönüşümü uygular.
- **hist()**: Şerit çizgilerini belirlemek için piksel yoğunluğu histogramını hesaplar.
- **find_lane_pixels()**: Kaydırma penceresi yöntemiyle şerit piksel noktalarını tespit eder.
- **fit_poly()**: Tespit edilen şerit piksel noktalarına ikinci dereceden bir polinom eğrisi uydurur.
- **measure_curvature()**: Şerit çizgilerinin eğrilik yarıçapını hesaplar.
- **plot()**: Çıkış görüntüsüne şerit çizgilerini çizer ve şerit tespitine dayalı araç kontrolünü uygular.

***
Feel free to customize and expand this lane detection system in your own Carla simulation projects!

***

Carla simülatörü projelerinizde bu şerit tespit sistemini özelleştirip genişletmekten çekinmeyin!
***

https://github.com/koesan/Serit_tespit_ile_otonom_surus/assets/96130124/8671b396-9942-4727-b576-17d8e283beb7

