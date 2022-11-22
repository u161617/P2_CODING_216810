import subprocess
import cv2
import mimetypes

# EX 1
# aquesta linea ensenya la duració, temps on comença el video i el bitrate
subprocess('ffmpeg -i bbb.mp4 2>&1 | grep Duration')

# EX 2
# la seguent linea talla el video al minut 1
subprocess('ffmpeg -i bbb.mp4 -ss 00:00:00 -t 00:01:00 -c:v copy -c:a copy cut_bbb.mp4')
# a continuació extreiem l'audio en mp3
subprocess('ffmpeg -i cut_bbb.mp4 -q:a 0 -map a audio_mp3.mp3')
# la linea seguent resueix el bitrate de l'audio a 128k bps
subprocess('ffmpeg -i cut_bbb.mp4 -b:a 128k audio_lowbirate.aac')
# la seguent linea agrupa l'audio 'audio_mp3.mp3' amb el video tallat
subprocess('ffmpeg -i cut_bbb.mp4 -i audio_mp3.mp3 -map 0:v -map 1:a -c:v copy -shortest bbb_mp3.mp4')
# la seguent linea agrupa l'audio 'audio_lowbirate.aac' i el video tallat
subprocess('ffmpeg -i cut_bbb.mp4 -i audio_lowbirate.aac -map 0:v -map 1:a -c:v copy -shortest bbb_lowbitrate.mp4')

# EX 3
mimetypes.init()
file = input('Escriu el nom de larxiu que vols canviar la mida')
mimestart = mimetypes.guess_type("c/Users/tomas/Downloads/"+file)[0]
res = input('Choose the resolution you want:'
                    '\n# 1: 720p'
                    '\n# 2: 480p'
                    '\n# 3: 360x240'
                    '\n# 4: 160x120'
                    '\n')
# en funcion del input, se escoge una resolución
if res == '1':
   resolution = (1280, 720)
elif res == '2':
   resolution = (852, 480)
elif res == '3':
   resolution = (360, 240)
elif res == '4':
   resolution = (160, 120)

if mimestart != None:
    mimestart = mimestart.split('/')[0]
    if mimestart == 'image':
        img = cv2.imread("c/Users/tomas/Downloads/"+file)
        cv2.resize(img, resolution)
        cv2.write("c/Users/tomas/Downloads/image_resize.jpg", img)
    if mimestart == 'video':
        cap = cv2.VideoCapture("c/Users/tomas/Downloads/"+file)
        video_out = cv2.VideoWriter("c/Users/tomas/Downloads/video_resize.mp4", 0, 30, resolution)
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                b = cv2.resize(frame, resolution)
                video_out.write(b)
            else:
                break

        cap.release()
        video_out.release()
        cv2.destroyAllWindows()

