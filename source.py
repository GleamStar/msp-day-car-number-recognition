import sys
import cv2
import os

import algorithms.utils
from algorithms.knearest import DetectChars, DetectPlates

from algorithms.simple.cv_image_preparation import ImagePreparation
from cv_service_interaction import AzureCVService

def startSimpleAlgorithm(path):
    image_service = ImagePreparation()
    cv_service = AzureCVService()
    image_service.process_image(path, 0, type='rect')

    image_data = cv_service.read_local_image('./filtered/sofwinres.png')
    response = cv_service.make_cv_request(image_data)

    cv_service.print_response(response=response)

def startKNearestAlgorith(path):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print "\nerror: KNN traning was not successful\n"  # show error message
        return  # and exit program


    imgOriginalScene = cv2.imread(path)  # open image

    if imgOriginalScene is None:  # if image was not read successfully
        print "\nerror: image not read from file \n\n"  # print error message to std out
        os.system("pause")  # pause so user can see error message
        return  # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

   # cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print "\nno license plates were detected\n"  # inform user no plates were found
    else:  # else
        # if we get in here list of possible plates has at leat one plate

        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

       # cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
       # cv2.imshow("imgThresh", licPlate.imgThresh)

        cv2.imwrite('./filtered/imgPlate.png', licPlate.imgPlate)

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate

        azure_service = AzureCVService()
        response = azure_service.make_cv_request(azure_service.read_local_image('./filtered/imgPlate.png'))

        azure_service.print_response(response)

    # end if else

    cv2.waitKey(0)  # hold windows open until user presses a key


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), algorithms.utils.SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), algorithms.utils.SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), algorithms.utils.SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), algorithms.utils.SCALAR_RED, 2)

if len(sys.argv) < 2:
    print 'usage:\n python source.py <image_file_path>'
    exit(0)

path = sys.argv[1]
mode = sys.argv[2]

print 'Mode ' + mode

if int(mode) == 0:
    startSimpleAlgorithm(path)
else:
    startKNearestAlgorith(path)


