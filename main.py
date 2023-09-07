import cv2
import carla 
import time 
import numpy as np

################################################### carla kodları ############################################################################

client = carla.Client('localhost', 2000)

client.set_timeout(10.0)

# Carla dünyası yükleniyor ve hava durumu ayarlanıyor
world = client.load_world('Town04')  # Şehri seç
bp_lib = world.get_blueprint_library() 

spawn_points = world.get_map().get_spawn_points() 

weather = carla.WeatherParameters( # Hava durumunu ayarlama
    cloudiness=80.0,
    precipitation=30.0,
    sun_altitude_angle=70.0)

world.set_weather(weather)

# Kullanılacak araç belirleniyor ve bir spawn noktasında oluşturuluyor
vehicle_bp = bp_lib.find('vehicle.audi.a2') # Kullanılacak araçı belirle 
#320
spawn = spawn_points[320] # Aracın başlangıç noktası
vehicle = world.try_spawn_actor(vehicle_bp,spawn) # Aracın başlangıç noktasını seç

# Bakış açısı kamerası oluşturuluyor 
spectator = world.get_spectator() 
transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-5, z=2.5)),vehicle.get_transform().rotation) 
spectator.set_transform(transform)

# Araç kamerası oluşturuluyor
camera_bp = bp_lib.find('sensor.camera.rgb') 
camera_init_trans = carla.Transform(carla.Location(x=6, z=5),carla.Rotation(pitch=-90))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

# Kamera verileri için bir veri yapısı oluşturuluyor
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
camera_data = {'image': np.zeros((image_h, image_w, 3), dtype=np.uint8)}  # 3 kanallı RGB görüntü

time.sleep(0.2)

# Kamera verileri için callbeck fonkisonu oluşturuluyor
def camera_callback(image, data_dict):

    raw_data = np.copy(image.raw_data)
    rgba_image = np.reshape(raw_data, (image.height, image.width, 4))
    rgb_image = rgba_image[:, :, :3]  
    data_dict['image'] = rgb_image                     

camera.listen(lambda image: camera_callback(image, camera_data))

################################################################################################################################################

################################################# şerit tespiti için kullanılan fonksiyonlar ###################################################

# resimde kırpma işlemi yapılıyor
def get_perspective_matrices(img):

    src = np.float32([(200, 600), (200, 0), (630, 0), (630, 600)])
    w, h = image_w, image_h
    img_size=(w, h)
    dst = np.float32([(0, h), (0, 0), (w, 0), (w, h)])
    M = cv2.getPerspectiveTransform(src, dst)
    M_inv = cv2.getPerspectiveTransform(dst, src)
    img = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)

    return cv2.warpPerspective(img, M_inv, img_size, flags=cv2.INTER_LINEAR)

# Yolun tamamının histogramını hesaplar.
def hist(img):

    full_image = img[:,:] # full_image = img[:,:] Resmin alt yarısını almak için bottom_half = img[img.shape[0]//2:,:]
    return np.sum(full_image, axis=0)

# Pencere içindeki pikselleri bulur.
def pixels_in_window(center, margin, height, nonzerox, nonzeroy):

    topleft = (center[0] - margin, center[1] - height//2)
    bottomright = (center[0] + margin, center[1] + height//2)
    condx = (topleft[0] <= nonzerox) & (nonzerox <= bottomright[0])
    condy = (topleft[1] <= nonzeroy) & (nonzeroy <= bottomright[1])
    return nonzerox[condx & condy], nonzeroy[condx & condy]

# Görüntüden özelliklerin çıkarılmasını sağlar.
def extract_features(img):

    window_height = int(img.shape[0] // nwindows)
    nonzero = img.nonzero()
    nonzerox = np.array(nonzero[1])
    nonzeroy = np.array(nonzero[0])

    return nonzerox, nonzeroy, window_height

# Yolun sol ve sağ şeritlerini bulur.
def find_lane_pixels(img, nwindows, margin, minpix,nonzerox, nonzeroy, window_height):

    out_img = np.dstack((img, img, img))
    histogram = hist(img)
    midpoint = histogram.shape[0] // 2
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    leftx_current = leftx_base
    rightx_current = rightx_base
    y_current = img.shape[0] + window_height // 2
    leftx, lefty, rightx, righty = [], [], [], []

    for _ in range(nwindows):
        y_current -= window_height
        center_left = (leftx_current, y_current)
        center_right = (rightx_current, y_current)
        good_left_x, good_left_y = pixels_in_window(center_left, margin, window_height, nonzerox, nonzeroy)
        good_right_x, good_right_y = pixels_in_window(center_right, margin, window_height, nonzerox, nonzeroy)
        leftx.extend(good_left_x)
        lefty.extend(good_left_y)
        rightx.extend(good_right_x)
        righty.extend(good_right_y)

        if len(good_left_x) > minpix:
            leftx_current = np.int32(np.mean(good_left_x))

        if len(good_right_x) > minpix:
            rightx_current = np.int32(np.mean(good_right_x))

    return leftx, lefty, rightx, righty, out_img

# Şerit eğrilerini hesaplar
def fit_poly(img, leftx, lefty, rightx, righty):

    maxy = img.shape[0] - 1
    miny = img.shape[0] // 3

    if len(lefty):
        maxy = max(maxy, np.max(lefty))
        miny = min(miny, np.min(lefty))

    if len(righty):
        maxy = max(maxy, np.max(righty))
        miny = min(miny, np.min(righty))

    ploty = np.linspace(miny, maxy, img.shape[0])

    if len(lefty) > 500: # if len(lefty) > 0 and len(leftx) > 0:
        left_fit = np.polyfit(lefty, leftx, 2)
    else:
        left_fit = [0, 0, 0]  

    if len(righty) > 500: # if len(righty) > 0 and len(rightx) > 0:
        right_fit = np.polyfit(righty, rightx, 2)
    else:
        right_fit = [0, 0, 0]  

    left_fitx = left_fit[0] * ploty**2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty**2 + right_fit[1] * ploty + right_fit[2]

    out_img = np.dstack((img, img, img))

    for i, y in enumerate(ploty):
        l = int(left_fitx[i])
        r = int(right_fitx[i])
        y = int(y)
        cv2.line(out_img, (l, y), (r, y), (0, 255, 0))

    return out_img

# Şerit eğrilerinin kıvrılma yarıçapını hesaplar.
def measure_curvature(left_fit, right_fit):

    ym = 30 / 720
    xm = 3.7 / 700

    y_eval = 700 * ym

    left_curveR = ((1 + (2 * left_fit[0] * y_eval + left_fit[1])**2)**1.5) / np.absolute(2 * left_fit[0])
    right_curveR = ((1 + (2 * right_fit[0] * y_eval + right_fit[1])**2)**1.5) / np.absolute(2 * right_fit[0])

    xl = np.dot(left_fit, [700**2, 700, 1])
    xr = np.dot(right_fit, [700**2, 700, 1])
    pos = (1280 // 2 - (xl + xr) // 2) * xm

    return left_curveR, right_curveR, pos

# Çıkış görüntüsüne yön ve kontrol bilgilerini ekler ve bilgilere göre aracı hareket ettirir.
def plot(out_img, left_curveR, right_curveR, pos, left_fit, right_fit):

    np.set_printoptions(precision=6, suppress=True)
    lR, rR, pos = measure_curvature(left_fit, right_fit)

    value = None

    if abs(left_fit[0]) > abs(right_fit[0]):
        value = left_fit[0]
    else:
        value = right_fit[0]

    if abs(value) <= 0.00015:
        directions.append('F') 
    elif value < 0:
        directions.append('L')
    else:
        directions.append('R')  

    if len(directions) > 10:
        directions.pop(0)

    H, W = out_img.shape[:2]
    widget = np.copy(out_img[:H, :W])
    widget //= 2
    widget[0, :] = [0, 0, 255]
    widget[-1, :] = [0, 0, 255]
    widget[:, 0] = [0, 0, 255]
    widget[:, -1] = [0, 0, 255]
    out_img[:H, :W] = widget

    direction = max(set(directions), key=directions.count)

    throttle = 0.4 # Gaz
    steer = 0.0     # Direksiyon açısı (-1 ile 1 arasında)
    brake = 0.0     # Fren

    if direction == 'L':
        steer = 0.1
        time.sleep(0.2)
        print("Sol")

    if direction == 'R':
        steer = -0.1
        time.sleep(0.2)
        print("Sağ")

    if direction == 'F':
        steer = 0.0
        print("İleri")

    if direction in 'LR':
        print("LR")

    control = carla.VehicleControl(throttle=throttle, steer=steer, brake=brake)
    vehicle.apply_control(control)

    return out_img

# Şerit tespiti için gerekli değişkenler ve işlevler tanımlanıyor
nwindows = 9
margin = 100
minpix = 50
directions = [] 

# Ana fonksiyon
def main():

    while True:

        image = camera_data['image']

        img_pers= get_perspective_matrices(image)
 
        img = cv2.cvtColor(img_pers, cv2.COLOR_RGB2GRAY)
        _, img = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
        
        nonzerox, nonzeroy, window_height = extract_features(img)

        leftx, lefty, rightx, righty, out_img = find_lane_pixels(img, nwindows, margin, minpix,nonzerox, nonzeroy, window_height)

        out_img = fit_poly(img, leftx, lefty, rightx, righty)

        if len(lefty) > 0 and len(leftx) > 0:
            left_fit = np.polyfit(lefty, leftx, 2)
        else:
            left_fit = [0, 0, 0]

        if len(righty) > 0 and len(rightx) > 0:
            right_fit = np.polyfit(righty, rightx, 2)
        else:
            right_fit = [0, 0, 0]  

        left_curveR, right_curveR, pos = measure_curvature(left_fit, right_fit)
        final_output = plot(out_img, left_curveR, right_curveR, pos,left_fit, right_fit)

        result = cv2.addWeighted(image, 0.7, final_output, 0.3, 0)
        lane_mask = (final_output[:, :, 0] == 0) & (final_output[:, :, 1] == 255) & (final_output[:, :, 2] == 0)
        result[lane_mask] = (0, 255, 0)

        cv2.imshow("winname", result)
        #cv2.imshow("line", final_output)
        cv2.imshow("pers", img_pers)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()

#####################################################################################################################

if __name__ == "__main__":

    main()