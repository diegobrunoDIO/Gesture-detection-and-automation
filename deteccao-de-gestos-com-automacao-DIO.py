import cv2 #importando o OPenCV
import os
import numpy as np
import math
cap = cv2.VideoCapture(0)
     
while(1):
        
    try:  #um erro ocorre se não encontrar nada na janela, pois não 
        #pode encontrar o contorno da área máxima #portanto, esta instrução de erro try
          
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
        
        #Define a região de interesse - máscara de análise do objeto
        roi=frame[100:300, 100:300] #tamanho da máscara
        
        
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)  #leitura da máscara  
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) #conversão do padrão RGB para HSV
        
        
         
    # definir gama de cor da pele em HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
     ##extrair imagem do contorno da pele em relação ao fundo do objeto
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
   
    #dilatação na mão para preencher manchas escuras dentro
        mask = cv2.dilate(mask,kernel,iterations = 4)
        
    #preencher mão com blur "borrar" na imagem
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
        
        
    #Encontrando os contornos
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
   #Encontre o contorno máximo da mão
        cnt = max(contours, key = lambda x: cv2.contourArea(x)) 
        #função aplicada para detectar o contorno do objeto binarizado
        
    #aproximação do contorno ao objeto
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        
    #fazer um objeto convexo ao redor da mão
        hull = cv2.convexHull(cnt)
        
     #define area of hull 
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
      
    #define área do objeto e área da mão
        arearatio=((areahull-areacnt)/areacnt)*100
    
     #encontre os defeitos no objeto convexo em relação à mão
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
    # l = sem defeitos
        l=0
        
    #definindo a região de interesse
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)
            
            
            # encontrar o comprimento de todos os lados do triângulo
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

            #calculo do perimetro do objeto
            
            #distância entre o ponto e o casco convexo
            d=(2*ar)/a
            
            # distância entre o ponto e o objeto convexo
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
            # ignore ângulos > 90 e ignore pontos muito próximos ao objeto convexo (geralmente vêm devido ao ruído)
            if angle <= 90 and d>30:
                l += 1
                cv2.circle(roi, far, 3, [255,0,0], -1)
            
            #desenhar linhas ao redor da mão
            cv2.line(roi,start, end, [0,255,0], 2)
            #o ROI define uma região de interesse
            
            
        l+=1
        
        #imprimir gestos correspondentes que estão em seus intervalos
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l==1:

            if areacnt<2000: #significa que não existe objeto na região
                cv2.putText(frame,'Esperando dados',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            else:
                executado = False
                if arearatio<12 and not executado:
                    cv2.putText(frame,'0 = Navegador',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    #os.system("start Chrome.exe --window-size=800,600")
                    executado = True
                    #break
                    
                    
                
                elif arearatio<17.5:
                    cv2.putText(frame,'',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    #os.system("start Arduino IDE.exe")

                   
                else:
                    cv2.putText(frame,'1 = Word',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    #os.system("start WINWORD.EXE --window-size=600,400")
                    #break
                    
        elif l==2:
            cv2.putText(frame,'2 = Excel',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
          #os.system("start Excel.exe --window-size=600,400")
            #break
            
            
        elif l==3:
         
              if arearatio<27:
                    cv2.putText(frame,'3 = Power Point',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    #os.system("start POWERPNT.EXE --window-size=600,400")
                    
              else:
                    cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                    
        elif l==4:
            cv2.putText(frame,'',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            #os.system("start firefox.exe")
            
        elif l==5:
            cv2.putText(frame,'',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            #os.system("start Spyder.launch.pyw")
            
        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        #show the windows
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
    except:
        pass
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
cap.release()    
    