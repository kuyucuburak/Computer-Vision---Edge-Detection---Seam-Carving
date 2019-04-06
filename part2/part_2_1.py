import os
import numpy

from PIL import Image
from math import e
from math import pi


filterSize = 5


def main():
    imageNum = input("1) Istanbul.jpg\n2) KizKulesi.jpg\n3) Lake.jpg\nChoose the image: ")
    try:
        imageNum = int(imageNum)

        if imageNum != 1 and imageNum != 2 and imageNum != 3:
            raise ValueError
    except ValueError:
        print("Please enter an integer \"1\" or \"2\"")
        exit(1)

    if imageNum == 1:
        image = Image.open('Istanbul.jpg')
    elif imageNum == 2:
        image = Image.open('KizKulesi.jpg')
    else:
        image = Image.open('Lake.jpg')


    operator = input("\n1) Sobel\n2) LoG\nChoose the operator type: ")
    try:
        operator = int(operator)

        if operator != 1 and operator != 2:
            raise ValueError
    except ValueError:
        print("Please enter an integer \"1\" or \"2\"")
        exit(1)


    importance = input("\n1) Least Important \n2) Most Important\nEnter the importance: ")
    try:
        importance = int(importance)

        if importance != 1 and importance != 2:
            raise ValueError
    except ValueError:
        print("Please enter an integer \"1\" or \"2\"")
        exit(1)


    print("")
    operate(image, operator, importance)


def operate(image, operator, importance):
    if operator == 1:
        matrix = applySobelOperatorFilter(image.convert('L'))
        name2 = "Sobel"
    else:
        matrix = applyLoGFilter(image.convert('L'))
        name2 = "LoG"

    copied_matrix = numpy.copy(matrix)

    imageMatrix = numpy.array(image)
    if importance == 1:
        matrix = assignVerticalWeightsLeast(matrix)
        carveVerticalSeamLeast(matrix, imageMatrix)

        copied_matrix = assignHorizontalWeightsLeast(copied_matrix)
        carveHorizontalSeamLeast(copied_matrix, imageMatrix)

        name3 = "Least"
    else:
        matrix = assignVerticalWeightsMost(matrix)
        carveVerticalSeamMost(matrix, imageMatrix)

        copied_matrix = assignHorizontalWeightsMost(copied_matrix)
        carveHorizontalSeamMost(copied_matrix, imageMatrix)

        name3 = "Most"

    imageMatrix = numpy.array(imageMatrix)
    resultImage = Image.fromarray(imageMatrix)
    name1 = os.path.splitext(image.filename)[0]

    name = name1 + "_" + name2 + "_" + name3 + ".jpg"
    resultImage.save(name)

    print("\n" + name + " is saved!")


def carveVerticalSeamLeast(matrix, imageMatrix):
    print("\nCarving Vertical Seam Least is started...")

    row = len(matrix)
    column = len(matrix[0])

    smallest_index = 0
    smallest_value = matrix[0][0]
    for j in range(1, column):
        if matrix[0][j] < smallest_value:
            smallest_index = j
            smallest_value = matrix[0][j]

    imageMatrix[0][smallest_index] = (255, 0, 0)

    lastRowIndex = column-1
    j = smallest_index

    for i in range(1, row-1):
        secondValue = matrix[i+1][j]

        firstValue = -1
        thirdValue = -1

        if j != 0:
            firstValue = matrix[i+1][j-1]

        if j != lastRowIndex:
            thirdValue = matrix[i+1][j+1]

        if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
            j = j-1
        elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
            j = j+1
        else:
            j = j

        imageMatrix[i][j] = (255, 0, 0)
    imageMatrix[row-1][j] = (255, 0, 0)

    print("Carving Vertical Seam Least is finished...\n")

    return imageMatrix


def carveVerticalSeamMost(matrix, imageMatrix):
    print("\nCarving Vertical Seam Most is started...")

    row = len(matrix)
    column = len(matrix[0])

    largest_index = 0
    largest_value = matrix[0][0]
    for j in range(1, column):
        if matrix[0][j] > largest_value:
            largest_index = j
            largest_value = matrix[0][j]

    imageMatrix[0][largest_index] = (255, 0, 0)

    lastRowIndex = column-1
    j = largest_index
    for i in range(1, row-1):
        secondValue = matrix[i+1][j]

        firstValue = -1
        thirdValue = -1

        if j != 0:
            firstValue = matrix[i+1][j-1]

        if j != lastRowIndex:
            thirdValue = matrix[i+1][j+1]

        if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
            j = j-1
        elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
            j = j+1
        else:
            j = j

        imageMatrix[i][j] = (255, 0, 0)
    imageMatrix[row-1][j] = (255, 0, 0)

    print("Carving Vertical Seam Most is finished...\n")

    return imageMatrix


def assignVerticalWeightsLeast(matrix):
    print("\nAssign Vertical Weights is started...")

    row = len(matrix)
    column = len(matrix[0])

    for x in range(row - 2, -1, -1):
        for y in range(0, column):
            secondValue = matrix[x+1][y]

            firstValue = -1
            thirdValue = -1

            if y != 0:
                firstValue = matrix[x+1][y-1]

            if y != column-1:
                thirdValue = matrix[x+1][y+1]

            if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
                matrix[x][y] = matrix[x][y] + firstValue
            elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
                matrix[x][y] = matrix[x][y] + thirdValue
            else:
                matrix[x][y] = matrix[x][y] + secondValue

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[0], axis=0)

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[:, 0], axis=1)

    print("Assign Vertical Weights is finished...\n")

    return matrix


def assignVerticalWeightsMost(matrix):
    print("\nAssign Vertical Weights Most is started...")

    row = len(matrix)
    column = len(matrix[0])

    for x in range(row - 2, -1, -1):
        for y in range(0, column):
            secondValue = matrix[x+1][y]

            firstValue = -1
            thirdValue = -1

            if y != 0:
                firstValue = matrix[x+1][y-1]

            if y != column-1:
                thirdValue = matrix[x+1][y+1]

            if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
                matrix[x][y] = matrix[x][y] + firstValue
            elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
                matrix[x][y] = matrix[x][y] + thirdValue
            else:
                matrix[x][y] = matrix[x][y] + secondValue

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[0], axis=0)

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[:, 0], axis=1)

    print("Assign Vertical Weights Most is finished...\n")

    return matrix


def carveHorizontalSeamLeast(matrix, imageMatrix):
    print("\nCarving Horizontal Seam Least is started...")

    row = len(matrix)
    column = len(matrix[0])

    smallest_index = 0
    smallest_value = matrix[0][0]
    for i in range(1, row):
        if matrix[i][0] < smallest_value:
            smallest_index = i
            smallest_value = matrix[0][i]

    imageMatrix[smallest_index][0] = (0, 255, 0)

    lastColumnIndex = row-1
    i = smallest_index
    for j in range(1, column-1):
        secondValue = matrix[i][j+1]

        firstValue = -1
        thirdValue = -1

        if i != 0:
            firstValue = matrix[i-1][j+1]

        if i != lastColumnIndex:
            thirdValue = matrix[i+1][j+1]

        if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
            i = i-1
        elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
            i = i+1
        else:
            i = i

        imageMatrix[i][j] = (0, 255, 0)
    imageMatrix[i][column-1] = (255, 0, 0)

    print("Carving Horizontal Seam Least is finished...\n")

    return imageMatrix


def carveHorizontalSeamMost(matrix, imageMatrix):
    print("\nCarving Horizontal Seam Most is started...")

    row = len(matrix)
    column = len(matrix[0])

    largest_index = 0
    largest_value = matrix[0][0]
    for i in range(1, row):
        if matrix[i][0] > largest_value:
            largest_index = i
            largest_value = matrix[0][i]

    imageMatrix[largest_index][0] = (0, 255, 0)

    lastColumnIndex = row-1
    i = largest_index
    for j in range(1, column-1):
        secondValue = matrix[i][j+1]

        firstValue = -1
        thirdValue = -1

        if i != 0:
            firstValue = matrix[i-1][j+1]

        if i != lastColumnIndex:
            thirdValue = matrix[i+1][j+1]

        if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
            i = i-1
        elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
            i = i+1
        else:
            i = i

        imageMatrix[i][j] = (0, 255, 0)
    imageMatrix[i][column-1] = (255, 0, 0)

    print("Carving Horizontal Seam Most is finished...\n")
    return imageMatrix


def assignHorizontalWeightsLeast(matrix):
    print("\nAssign Horizontal Weights is started...")

    row = len(matrix)
    column = len(matrix[0])

    for y in range(1, column):
        for x in range(0, row):
            secondValue = matrix[x][y-1]

            firstValue = -1
            thirdValue = -1

            if x != 0:
                firstValue = matrix[x-1][y-1]

            if x != row-1:
                thirdValue = matrix[x+1][y-1]

            if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
                matrix[x][y] = matrix[x][y] + firstValue
            elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
                matrix[x][y] = matrix[x][y] + thirdValue
            else:
                matrix[x][y] = matrix[x][y] + secondValue

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[0], axis=0)

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[:, 0], axis=1)

    print("Assign Horizontal Weights is started...\n")

    return matrix


def assignHorizontalWeightsMost(matrix):
    print("\nAssign Horizontal Weights Most is started...")

    row = len(matrix)
    column = len(matrix[0])

    for y in range(1, column):
        for x in range(0, row):
            secondValue = matrix[x][y-1]

            firstValue = -1
            thirdValue = -1

            if x != 0:
                firstValue = matrix[x-1][y-1]

            if x != row-1:
                thirdValue = matrix[x+1][y-1]

            if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
                matrix[x][y] = matrix[x][y] + firstValue
            elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
                matrix[x][y] = matrix[x][y] + thirdValue
            else:
                matrix[x][y] = matrix[x][y] + secondValue

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[0], axis=0)

    for i in range(filterSize):
        matrix = numpy.insert(matrix, 0, matrix[:, 0], axis=1)

    print("Assign Horizontal Weights Most is started...\n")

    return matrix


def applySobelOperatorFilter(image):
    number = 3

    def getResultArray(myFilter):
        matrix = numpy.array(image)

        resultArray = numpy.zeros((len(matrix), len(matrix[0])))
        for i in range(number):
            tempArray = numpy.copy(matrix)
            for k in range(i):
                tempArray = numpy.c_[numpy.zeros(len(tempArray)), tempArray]
                tempArray = numpy.delete(tempArray, -1, axis=1)
            for j in range(number):
                resultArray = resultArray + tempArray * myFilter[number-j-1][number-i-1]
                tempArray = numpy.r_[numpy.zeros((1, len(tempArray[0]))), tempArray]
                tempArray = numpy.delete(tempArray, -1, axis=0)

        return resultArray

    GxFilter = [[-1, 0, +1],
                [-2, 0, +2],
                [-1, 0, +1]]
    Gx = getResultArray(GxFilter)

    GyFilter = [[+1, +2, +1],
                [0, 0, 0],
                [-1, -2, -1]]
    Gy = getResultArray(GyFilter)

    G = (Gx**2 + Gy**2) ** (1/2)
    G = G.astype(int)

    for n in range(filterSize):
        G = numpy.delete(G, 0, axis=0)

    for n in range(filterSize):
        G = numpy.delete(G, 0, axis=1)

    return G


def applyLoGFilter(image):
    def getLoGFilter():
        shape = (number, number)

        array = numpy.zeros(shape)
        sigma = 0.75
        for x in range(number):
            for y in range(number):
                firstTemp = ((-1) / (pi * sigma**4))
                secondTemp = (-1) * ((x**2 + y**2) / (2 * sigma**2))
                array[x][y] = firstTemp * (1 + secondTemp) * (e**secondTemp)

        return array

    matrix = numpy.array(image)

    number = filterSize
    myFilter = getLoGFilter()

    resultArray = numpy.zeros((len(matrix), len(matrix[0])))
    for i in range(number):
        tempArray = numpy.copy(matrix)
        for k in range(i):
            tempArray = numpy.c_[numpy.zeros(len(tempArray)), tempArray]
            tempArray = numpy.delete(tempArray, -1, axis=1)
        for j in range(number):
            resultArray = resultArray + tempArray * myFilter[number-j-1][number-i-1]
            tempArray = numpy.r_[numpy.zeros((1, len(tempArray[0]))), tempArray]
            tempArray = numpy.delete(tempArray, -1, axis=0)

    resultArray = resultArray.astype(int)

    for i in range(number):
        resultArray = numpy.delete(resultArray, 0, axis=0)

    for i in range(number):
        resultArray = numpy.delete(resultArray, 0, axis=1)

    return resultArray


if __name__ == "__main__":
    main()
