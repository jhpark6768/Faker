import cv2
import dlib
from scipy.spatial import distance
#경고음성 재생을 위한 추가 import
import winsound
from pathlib import Path
import os
from project import settings

def calculate_EAR(eye):
  A = distance.euclidean(eye[1], eye[5])
  B = distance.euclidean(eye[2], eye[4])
  C = distance.euclidean(eye[0], eye[3])
  ear_aspect_ratio = (A+B)/(2.0*C)
  return ear_aspect_ratio

#srcPath =-> image 경로로 하고
def drowsy(filename):
  # 주석처리(#~~~되있는 코드들은 모두 웹캠으로 실행할때 하게끔 하는것들, 똑같지만 frame과 img로 구분되있는 코드들을 서로 바꾸면 웹캠,이미지 변환 가능)
  #cap = cv2.VideoCapture(0)
  FILE = Path(__file__).resolve()
  ROOT = FILE.parents[0] 
  save_dir = ROOT.parents[0]/'static/detect'
  ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
  filepath = ROOT / settings.MEDIA_ROOT / filename
  img = cv2.imread(filepath)
  hog_face_detector = dlib.get_frontal_face_detector()
  datafile = 'shape_predictor_68_face_landmarks.dat'
  dlib_facelandmark = dlib.shape_predictor(str(ROOT/datafile))
  #경로 지정해줘야함(경로 \ 로 되있으면 오류 / 로 바꿔야함)

  
  #while True:
# _, frame = cap.read() #한프레임씩 가져오기
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #색변환? 왜하는거지?
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  faces = hog_face_detector(gray)
  for face in faces:

    face_landmarks = dlib_facelandmark(gray, face)
    leftEye = []
    rightEye = []

    for n in range(36,42):
      x = face_landmarks.part(n).x
      y = face_landmarks.part(n).y
      leftEye.append((x,y))
      next_point = n+1
      if n == 41:
        next_point = 36 
      x2 = face_landmarks.part(next_point).x
      y2 = face_landmarks.part(next_point).y
    #cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)#RGB(0, 255, 0)
    #cv2.line(img, (x,y),(x2,y2),(0,255,0),1)
    for n in range(42,48):
      x = face_landmarks.part(n).x
      y = face_landmarks.part(n).y
      rightEye.append((x,y))
      next_point = n+1
    if n == 47:
      next_point = 42
    x2 = face_landmarks.part(next_point).x
    y2 = face_landmarks.part(next_point).y
    #cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)
    #cv2.line(img, (x,y),(x2,y2),(0,255,0),1)

    left_ear = calculate_EAR(leftEye)
    right_ear = calculate_EAR(rightEye)
   #양눈의 종횡비 합/2
    EAR = (left_ear+right_ear)/2
    EAR = round(EAR,2)
    print("EAR 값이 몇?", EAR)
    if EAR < 0.26:#종횡비가 0.2미만일때 문구출력(눈작은 사람이면 계속 경고)
    #cv2.putText(frame,"DROWSY",(20,100),
      img2 = cv2.putText(img, "Alert",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
      #cv2.putText(frame,"Are you Sleepy?",(20,400),
      img2 = cv2.putText(img2, "Are you Sleepy?",(20,400),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
      save_img = save_dir/'result.jpg'
      cv2.imwrite(save_dir/'result.jpg',img2)
      return True
    else:
      img2 = cv2.putText(img, "",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
      #cv2.putText(frame,"Are you Sleepy?",(20,400),
      img2 = cv2.putText(img2, "SAFE",(20,300),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
      save_img = save_dir/'result.jpg'
      cv2.imwrite(save_dir/'result.jpg',img2)
      return False
    #print("Drowsy")#터미널에서 나오는거니까 없앰
    #여기에 output

    #영상에선 일정시간이상 감겻을때 경고하게 만들기
    #경고음 재생
    #winsound.Beep(1000,1000)

#cv2.imshow("Are you Sleepy", frame)


  # key = cv2.waitKey(1)
  # if key == 27:#esc키
  #   break
  # #cap.release()
  # cv2.destroyAllWindows() 