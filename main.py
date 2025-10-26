import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import PhotoImage

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"
faceNet=cv2.dnn.readNet(faceModel, faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(8-12)', '(15-20)', '(15-20)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

def faceBox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            bboxs.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (232, 92, 49), 1)
    return frame, bboxs

def open_webcam():
    video = cv2.VideoCapture(0)
    process_video(video)

def open_video():
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        video = cv2.VideoCapture(file_path)
        process_video(video)

def open_image():
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        process_image(file_path)
def process_video(video):
    padding = 20
    while True:
        ret, frame = video.read()
        if not ret:
            break

            # Giảm kích thước của frame
            resized_frame = resize_video(frame, target_width=400)  # Sử dụng hàm resize_image
            frame, bboxs = faceBox(faceNet, resized_frame)
        frame, bboxs = faceBox(faceNet, frame)
        for bbox in bboxs:
            face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
                   max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            genderNet.setInput(blob)
            genderPred = genderNet.forward()
            gender = genderList[genderPred[0].argmax()]

            ageNet.setInput(blob)
            agePred = ageNet.forward()
            age = ageList[agePred[0].argmax()]

            label = "{}{}".format(gender, age)

            cv2.rectangle(frame, (bbox[0], bbox[1] - 30), (bbox[2], bbox[1]), (232, 92, 49), -1)
            cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2,
                        cv2.LINE_AA)

        cv2.imshow("Age-Gender", frame)
        k = cv2.waitKey(1)
        if k == 27:  # Esc key
            break

def resize_image(image, target_width):
    height, width = image.shape[:2]
    aspect_ratio = target_width / float(width)
    target_height = int(height * aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height))
    return resized_image

def process_image(file_path):
    original_image = cv2.imread(file_path)
    resized_image = resize_image(original_image, target_width=600)  # Thay đổi target_width theo ý muốn
    frame, bboxs = faceBox(faceNet, resized_image)
    padding = 20
    for bbox in bboxs:
        face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
               max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPred = genderNet.forward()
        gender = genderList[genderPred[0].argmax()]

        ageNet.setInput(blob)
        agePred = ageNet.forward()
        age = ageList[agePred[0].argmax()]

        label = "{},{}".format(gender, age)
        cv2.rectangle(frame, (bbox[0], bbox[1] - 30), (bbox[2], bbox[1]), (232, 92, 49), -1)
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2,
                    cv2.LINE_AA)
    display_image(frame)

def display_image(frame):
    frame, _ = faceBox(faceNet, frame)
    cv2.imshow("Age-Gender",frame  )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def UI():
    root = tk.Tk()
    root.title("Face Age-Gender Detection")

    # Không cho phép thay đổi kích thước cửa sổ bằng cách kéo thả
    root.resizable(width=False, height=False)

    # Tạo background bằng ảnh
    background_image = Image.open("hinhanh_videos/bgs.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    canvas = tk.Canvas(root, width=background_image.width, height=background_image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

    # Điều chỉnh các nút chức năng ở giữa màn hình
    canvas_width = background_image.width
    canvas_height = background_image.height

    # Tiêu đề
    heading_label = ttk.Label(root, text="Face Age - Gender Detection", font=('Helvetica', 30, 'bold'), foreground='#2554C7')
    canvas.create_window(canvas_width // 2, 100, window=heading_label)  # Center horizontally

    # Chèn icon và resize icon
    icon_size = (2,2)  # icon size
    webcam_icon = PhotoImage(file="hinhanh_videos/webcam.png").subsample(*icon_size)
    video_icon = PhotoImage(file="hinhanh_videos/video.png").subsample( *icon_size)
    image_icon = PhotoImage(file="hinhanh_videos/image.png").subsample(*icon_size)

    # Style cho nút chức năng
    root.style = ttk.Style()
    root.style.configure('Colorful.TButton', background='#2554C7', foreground='#2554C7', font=('Helvetica', 12, 'bold'),
                         padding=(20, 10), width=15)
    # Các nút có bố cục, màu sắc và icon
    webcam_button = ttk.Button(root, text="Webcam (W)", command=open_webcam, style='Colorful.TButton', image=webcam_icon,
                               compound=tk.LEFT)
    canvas.create_window(canvas_width // 4, canvas_height // 2, window=webcam_button)

    video_button = ttk.Button(root, text="Video (V)", command=open_video, style='Colorful.TButton', image=video_icon,
                              compound=tk.LEFT)
    canvas.create_window(canvas_width // 2, canvas_height // 2,
                         window=video_button)

    image_button = ttk.Button(root, text="Image (I)", command=open_image, style='Colorful.TButton', image=image_icon,
                              compound=tk.LEFT)
    canvas.create_window(3 * canvas_width // 4, canvas_height // 2, window=image_button)

    # Thêm một dòng ghi chú dưới các nút
    note_text = ("Lưu ý: Khi sử dụng Webcam hoặc Video bạn cần nhấn nút ESC để có thể dừng thực thi, sau đó mới có thể thoát khỏi cửa sổ ."
                 "\nNote: When using Webcam or Video, you need to press the ESC button to stop execution, then you can exit the window.")
    note_label = canvas.create_text(
        canvas_width // 2, canvas_height - 30, text=note_text, font=('Helvetica', 15),
        fill='#FFFFFF', anchor=tk.CENTER, justify=tk.CENTER
    )

    # Gán các phím tắt
    root.bind('w', lambda event: open_webcam())
    root.bind('v', lambda event: open_video())
    root.bind('i', lambda event: open_image())

    # Đổi màu các nút
    root.style = ttk.Style()
    root.style.configure('Colorful.TButton', background='#2554C7', foreground='#2554C7', font=('Helvetica', 12, 'bold'))
    root.mainloop()
UI()