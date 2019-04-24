import requests
import json
import PySimpleGUI as sg

# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "c7009e27d6c84ee9be917ea132162fcf"
assert subscription_key

layout = [
              [sg.Text('Enter URL of image')], # key='_TEXT_')],      
              [sg.Input()],      
              [sg.Submit(), sg.Cancel()]
             ]

    
event1 = ''
values = ''


#event loop
while True and event1 != "Yes":
    window = sg.Window('The best GUI',size=(400,200), 
    background_color ='blue', font='Arial').Layout(layout)
    event, values = window.Read()
    if event is None or event == 'Cancel':
        break

        
    else:
        window.Close()
        validate = [
            [sg.Text('Is this the correct URL?')],
            [sg.Text(values[0])],
            [sg.Yes(), sg.No()]
            ]
        window1 = sg.Window('The best GUI',size=(400,200), background_color
                        ='blue', font='Arial').Layout(validate)
        event1, values1 = window1.Read()
                
                
                
        window1.Close()
        if event1 == "Yes": 
            break        

window.Close()


# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"

ocr_url = vision_base_url + "ocr"

# Set image_url to the URL of an image that you want to analyze.
image_url = values[0]

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params  = {'language': 'unk', 'detectOrientation': 'true'}
data    = {'url': image_url}
response = requests.post(ocr_url, headers=headers, params=params, json=data)
response.raise_for_status()

analysis = response.json()

#print(json.dumps(analysis, indent=4, sort_keys=True))

#print(analysis['regions'][0]['lines'][0])

#print(analysis['regions'][0]['lines'][0]['words'][0]['text'] + ' ' +analysis['regions'][0]['lines'][0]['words'][1]['text']+ ' ' +analysis['regions'][0]['lines'][0]['words'][2]['text'])

# Extract the word bounding boxes and text.
#extracts all lines in each region
line_infos = [region["lines"] for region in analysis["regions"]]
#print (line_infos)

word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)

#arrays for accumulating data
points = []
textArr = []

# Display the image and overlay it with the extracted text.
plt.figure(figsize=(5, 5))
image = Image.open(BytesIO(requests.get(image_url).content))
ax = plt.imshow(image, alpha=0.5)
for word in word_infos:
    #Here is the bounding box extraction
    bbox= [int(num) for num in word["boundingBox"].split(",")]
    points.append(bbox)
    #Here is the text extraction
    text = word["text"]
    textArr.append(text)
    #Top left corner coordinates
    origin = (bbox[0], bbox[1])
    patch  = Rectangle(origin, bbox[2], bbox[3], fill=False, linewidth=1, color='y')
    ax.axes.add_patch(patch)
    plt.text(origin[0], origin[1], text, fontsize=8, weight="bold", va="top")
plt.axis("off")

points
print(textArr)

pointFin = []
textFin =[]
#merge coordinates with similar y-vals
for i in range (len(points)):
    for j in range (i+1, len(points)):
        if abs(points[i][1] - points[j][1]) <= 3:
            points[i][2] = points[i][2]+points[j][2]
            if textArr[j] not in textArr[i]:
                textArr[i] = textArr[i]+" "+textArr[j] 
                
                
textFin.append(textArr[0])
                
for p in range (len(textArr)-1):
    
    if textArr[p+1] not in textArr[p]:
        textFin.append(textArr[p+1])
        pointFin.append(points[p+1])

#print(textFin)
#pointFin

company = textFin[0]
name = ""
idNum = ""
for m in range(len(textFin)-1):
    if 'Name' in textFin[m]:
        name = textFin[m+1]
    if 'Member' in textFin[m]:
        name = textFin[m+1]
        
        
for z in range(len(textFin)-1):
    if 'Number' in textFin[z]:
        idNum = textFin[z+1]
    if 'ID'in textFin[z]:
        idNum = textFin[z+1]
    if 'Identificaton'in textFin[z]:
        idNum = textFin[z+1]
        
            
#for k in textFin:
for i in range(len(textFin)):
    if textFin[i] == textFin[i].upper():
        print(textFin[i])

# layout = [
#               [sg.Text('Please enter your Name, ID, Insurance')],
#               [sg.Text('Name', size=(15, 1)), sg.InputText()],      
#               [sg.Text('ID Number', size=(15, 1)), sg.InputText()],      
#               [sg.Text('Insurance', size=(15, 1)), sg.InputText()],      
#               [sg.Submit(), sg.Cancel()]
#              ]

# validate1 = [
#             [sg.Text('Is the following information correct?')],
#             [sg.Text('Company:'), sg.Text(textFin[0])],
#             [sg.Text('Name'), sg.Text(name)],
#             [sg.Text('ID Number'), sg.Text(idNum)],
#             [sg.Yes(), sg.No()]
#             ]
# window2 = sg.Window('The best GUI',size=(400,200), background_color
#                         ='blue', font='Arial').Layout(validate1)
# event2, values2 = window2.Read()

validate2 = [
        [sg.Text('Is the following information correct?')],
        [sg.Text('Company:'), sg.InputText(textFin[0])],
        [sg.Text('Name'), sg.InputText(name)],
        [sg.Text('ID Number'), sg.InputText(idNum)],
        [sg.Yes(), sg.No()]
        ]           

window3 = sg.Window('Another great GUI').Layout(validate2)  
event3, values3 = window3.Read() 
event3 = ''

while event3 != "Yes":
    # window2 = sg.Window('Another great GUI').Layout(validate)  
    # event2, values2 = window2.Read() 
    if event3 is None or event3 == 'Yes':
        break
            
    else:
        window3.Close()
    
        validate2 = [
        [sg.Text('Is the following information correct?')],
        [sg.Text('Company:'), sg.InputText(textFin[0])],
        [sg.Text('Name'), sg.InputText(name)],
        [sg.Text('ID Number'), sg.InputText(idNum)],
        [sg.Yes(), sg.No()]
        ]           

        window3 = sg.Window('Another great GUI').Layout(validate2)  
        event3, values3 = window3.Read() 

        window3.Close()
        if event3 == "Yes":
            break

window.Close()
    
#for i in range(len(values)):
 #   print(values[i])
        
# print('Insurer: '+company)
# print('Name: ' + name)
# print('ID: ' + idNum)