<div align="center">

# Autonomous Driving with Lane Detection

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![CARLA](https://img.shields.io/badge/CARLA-Simulator-yellow.svg)](https://carla.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Latest-013243.svg)](https://numpy.org/)

https://github.com/koesan/Serit_tespit_ile_otonom_surus/assets/96130124/8671b396-9942-4727-b576-17d8e283beb7

---

**[English](#english)** | **[Türkçe](#turkish)**

</div>

---

## <a name="english"></a>🇬🇧 English

# Lane Detection for Autonomous Driving with CARLA Simulator

This project implements a real-time lane detection system using the CARLA simulator. The system detects lane markings using computer vision and autonomously controls the vehicle to stay centered within the lane.

## Overview

The project combines computer vision techniques with autonomous vehicle control. It captures camera images from a virtual vehicle, processes them to detect lane lines, and automatically steers the vehicle based on the detected lanes. This is a practical demonstration of how autonomous vehicles use vision systems for navigation.

## How It Works

**1. Simulation Setup**
- Connects to CARLA server on `localhost:2000`
- Configures weather conditions and spawns a vehicle
- Sets up a camera with bird's-eye view perspective

**2. Lane Detection**
- Captures images from the vehicle camera
- Applies perspective transformation for bird's-eye view
- Uses sliding window technique to find lane pixels
- Fits polynomial curves to detected lane lines
- Calculates lane curvature and vehicle position

**3. Vehicle Control**
- Analyzes lane geometry to determine steering direction
- Adjusts steering angle to keep vehicle centered
- Controls throttle for steady forward motion

## Installation

**Requirements:**
- CARLA Simulator 0.9.x or higher
- Python 3.7+
- Required packages:
  ```bash
  pip install opencv-python numpy carla
  ```

## Running the Project

1. Start CARLA Simulator

2. Run the lane detection system:
   ```bash
   python main.py
   ```

3. Press `q` to stop the program

## Key Functions

- `get_perspective_matrices()` - Creates bird's-eye view transformation
- `find_lane_pixels()` - Detects lane pixels using sliding windows
- `fit_poly()` - Fits polynomial curves to lane boundaries
- `measure_curvature()` - Calculates lane curvature
- `plot()` - Visualizes lanes and controls the vehicle

---

## <a name="turkish"></a>🇹🇷 Türkçe

# CARLA Simülatörü ile Şerit Tespiti ve Otonom Sürüş

Bu proje, CARLA simülatörü kullanarak gerçek zamanlı şerit tespit sistemi geliştirmektedir. Sistem, bilgisayarlı görü teknikleri ile şerit çizgilerini tespit eder ve aracı şeridin ortasında tutacak şekilde otonom olarak kontrol eder.

## Genel Bakış

Proje, bilgisayarlı görü tekniklerini otonom araç kontrolü ile birleştirir. Sanal bir araçtan kamera görüntüleri alır, şerit çizgilerini tespit etmek için işler ve tespit edilen şeritlere göre aracı otomatik olarak yönlendirir. Bu, otonom araçların navigasyon için görüntü sistemlerini nasıl kullandığının pratik bir gösterimidir.

## Nasıl Çalışır

**1. Simülasyon Kurulumu**
- `localhost:2000` adresindeki CARLA sunucusuna bağlanır
- Hava koşullarını yapılandırır ve araç oluşturur
- Kuş bakışı perspektifine sahip kamera ayarlar

**2. Şerit Tespiti**
- Araç kamerasından görüntüler yakalar
- Kuş bakışı görünüm için perspektif dönüşümü uygular
- Kayan pencere tekniği ile şerit piksellerini bulur
- Tespit edilen şerit çizgilerine polinom eğrileri uydurur
- Şerit eğriliğini ve araç pozisyonunu hesaplar

**3. Araç Kontrolü**
- Şerit geometrisini analiz ederek direksiyon yönünü belirler
- Aracı merkezde tutmak için direksiyon açısını ayarlar
- Sabit ileri hareket için gazı kontrol eder

## Kurulum

**Gereksinimler:**
- CARLA Simülatörü 0.9.x veya üzeri
- Python 3.7+
- Gerekli paketler:
  ```bash
  pip install opencv-python numpy carla
  ```

## Projeyi Çalıştırma

1. CARLA Simülatörünü başlatın

2. Şerit tespit sistemini çalıştırın:
   ```bash
   python main.py
   ```

3. Programı durdurmak için `q` tuşuna basın

## Önemli Fonksiyonlar

- `get_perspective_matrices()` - Kuş bakışı görünüm dönüşümü oluşturur
- `find_lane_pixels()` - Kayan pencereler kullanarak şerit piksellerini tespit eder
- `fit_poly()` - Şerit sınırlarına polinom eğrileri uydurur
- `measure_curvature()` - Şerit eğriliğini hesaplar
- `plot()` - Şeritleri görselleştirir ve aracı kontrol eder
