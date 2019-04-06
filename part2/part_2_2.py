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

    methodNum = input("\n1) Decrease Width \n2) Decrease Height \n3) Increase Width \n4) Increase Width\nEnter the method: ")
    try:
        methodNum = int(methodNum)

        if methodNum != 1 and methodNum != 2 and methodNum != 3 and methodNum != 4:
            raise ValueError
    except ValueError:
        print("Please enter an integer \"1\" or \"2\" or \"3\" or \"4\"")
        exit(1)



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



    pixelNum = input("\nEnter the pixel number: ")
    try:
        pixelNum = int(pixelNum)
    except ValueError:
        print("Please enter an integer!")
        exit(1)
    print("")


    if methodNum == 1:
        decreaseWidth(image, pixelNum, operator, importance)
    elif methodNum == 2:
        decreaseHeight(image, pixelNum, operator, importance)
    elif methodNum == 3:
        increaseWidth(image, pixelNum, operator, importance)
    elif methodNum == 4:
        increaseHeight(image, pixelNum, operator, importance)


def decreaseWidth(image, numberOfPixels, operator, importance):
    if importance == 1:
        imageMatrix = removeVerticalSeamLeast(image, operator, numberOfPixels)
    else:
        imageMatrix = removeVerticalSeamMost(image, operator, numberOfPixels)

    imageMatrix = numpy.array(imageMatrix)
    resultImage = Image.fromarray(imageMatrix)

    name1 = os.path.splitext(image.filename)[0]
    if operator == 1:
        name2 = "Sobel"
    else:
        name2 = "LoG"
    if importance == 1:
        name3 = "Least"
    else:
        name3 = "Most"
    name = name1 + "_" + name2 + "_" + name3 + "_" + str(numberOfPixels) + "_wd.jpg"

    resultImage.save(name)

    print("\n" + name + " is saved!")


def decreaseHeight(image, numberOfPixels, operator, importance):
    if importance == 1:
        imageMatrix = removeHorizontalSeamLeast(image, operator, numberOfPixels)
    else:
        imageMatrix = removeHorizontalSeamMost(image, operator, numberOfPixels)

    imageMatrix = numpy.array(imageMatrix)
    resultImage = Image.fromarray(imageMatrix)

    name1 = os.path.splitext(image.filename)[0]
    if operator == 1:
        name2 = "Sobel"
    else:
        name2 = "LoG"
    if importance == 1:
        name3 = "Least"
    else:
        name3 = "Most"
    name = name1 + "_" + name2 + "_" + name3 + "_" + str(numberOfPixels) + "_hd.jpg"

    resultImage.save(name)

    print("\n" + name + " is saved!")


def increaseWidth(image, numberOfPixels, operator, importance):
    if importance == 1:
        imageMatrix = addVerticalSeamLeast(image, operator, numberOfPixels)
    else:
        imageMatrix = addVerticalSeamMost(image, operator, numberOfPixels)

    imageMatrix = numpy.array(imageMatrix)
    resultImage = Image.fromarray(imageMatrix)

    name1 = os.path.splitext(image.filename)[0]
    if operator == 1:
        name2 = "Sobel"
    else:
        name2 = "LoG"
    if importance == 1:
        name3 = "Least"
    else:
        name3 = "Most"
    name = name1 + "_" + name2 + "_" + name3 + "_" + str(numberOfPixels) + "_wu.jpg"

    resultImage.save(name)

    print("\n" + name + " is saved!")


def increaseHeight(image, numberOfPixels, operator, importance):
    if importance == 1:
        imageMatrix = addHorizontalSeamLeast(image, operator, numberOfPixels)
    else:
        imageMatrix = addHorizontalSeamMost(image, operator, numberOfPixels)

    imageMatrix = numpy.array(imageMatrix)
    resultImage = Image.fromarray(imageMatrix)

    name1 = os.path.splitext(image.filename)[0]
    if operator == 1:
        name2 = "Sobel"
    else:
        name2 = "LoG"
    if importance == 1:
        name3 = "Least"
    else:
        name3 = "Most"
    name = name1 + "_" + name2 + "_" + name3 + "_" + str(numberOfPixels) + "_hu.jpg"

    resultImage.save(name)

    print("\n" + name + " is saved!")


def removeVerticalSeamLeast(image, operator, numberOfPixels):
    print("\nRemove Vertical Seam Least is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignVerticalWeightsLeast(matrix)

        row = len(matrix)
        column = len(matrix[0])

        smallest_index = 0
        smallest_value = matrix[0][0]
        for j in range(1, column):
            if matrix[0][j] < smallest_value:
                smallest_index = j
                smallest_value = matrix[0][j]

        lastRowIndex = column - 1
        j = smallest_index

        indexList = [j]

        for i in range(1, row - 1):
            secondValue = matrix[i + 1][j]

            firstValue = -1
            thirdValue = -1

            if j != 0:
                firstValue = matrix[i + 1][j - 1]

            if j != lastRowIndex:
                thirdValue = matrix[i + 1][j + 1]

            if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
                j = j - 1
            elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
                j = j + 1
            else:
                j = j

            indexList.append(j)
        indexList.append(j)

        newImageMatrix = numpy.delete(imageMatrix, 0, axis=1)
        for i in range(len(indexList)):
            newImageMatrix[i] = numpy.delete(imageMatrix[i], indexList[i], axis=0)
        imageMatrix = newImageMatrix

        print(str(iteration + 1) + ". vertical seam is removed.")

    print("\nRemove Vertical Seam Least is finished...\n")

    return imageMatrix


def removeVerticalSeamMost(image, operator, numberOfPixels):
    print("\nRemove Vertical Seam Most is started...")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignVerticalWeightsMost(matrix)

        row = len(matrix)
        column = len(matrix[0])

        largest_index = 0
        largest_value = matrix[0][0]
        for j in range(1, column):
            if matrix[0][j] > largest_value:
                largest_index = j
                largest_value = matrix[0][j]

        lastRowIndex = column-1
        j = largest_index

        indexList = [j]

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

            indexList.append(j)
        indexList.append(j)

        newImageMatrix = numpy.delete(imageMatrix, 0, axis=1)
        for i in range(len(indexList)):
            newImageMatrix[i] = numpy.delete(imageMatrix[i], indexList[i], axis=0)
        imageMatrix = newImageMatrix

        print(str(iteration + 1) + ". vertical seam is removed.")

    print("Remove Vertical Seam Most is finished...\n")

    return imageMatrix


def addVerticalSeamLeast(image, operator, numberOfPixels):
    print("\nAdd Vertical Seam Least is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignVerticalWeightsLeast(matrix)

        row = len(matrix)
        column = len(matrix[0])

        smallest_index = 0
        smallest_value = matrix[0][0]
        for j in range(1, column):
            if matrix[0][j] < smallest_value:
                smallest_index = j
                smallest_value = matrix[0][j]

        lastRowIndex = column - 1
        j = smallest_index

        indexList = [j]

        for i in range(1, row - 1):
            secondValue = matrix[i + 1][j]

            firstValue = -1
            thirdValue = -1

            if j != 0:
                firstValue = matrix[i + 1][j - 1]

            if j != lastRowIndex:
                thirdValue = matrix[i + 1][j + 1]

            if firstValue != -1 and firstValue < secondValue and (thirdValue == -1 or firstValue < thirdValue):
                j = j - 1
            elif thirdValue != -1 and thirdValue < secondValue and (firstValue == -1 or thirdValue < firstValue):
                j = j + 1
            else:
                j = j

            indexList.append(j)
        indexList.append(j)

        imageMatrix = numpy.insert(imageMatrix, column-1, imageMatrix[:, column-1], axis=1)
        for i in range(row):
            for j in range(column, indexList[i]-1, -1):
                imageMatrix[i][j] = imageMatrix[i][j-1]

        for i in range(row):
            def getGaussianFilter():
                array = numpy.zeros((3, 3))
                sigma = 0.421
                for x in range(3):
                    for y in range(3):
                        firstTemp = (1 / (2 * pi * sigma**2))
                        secondTemp = (-1) * ((x**2 + y**2) / (2 * sigma**2))
                        array[x][y] = firstTemp * (e**secondTemp)

                return array

            gaussianFilter = getGaussianFilter()

            if i - 1 > 0 and (indexList[i] - 1) > 0:
                tuple1 = tuple([z * gaussianFilter[0][0] for z in imageMatrix[i - 1][indexList[i] - 1]])
            else:
                tuple1 = (0, 0, 0)

            if i - 1 > 0 and (indexList[i] + 1) < (column + 1):
                tuple2 = tuple([z * gaussianFilter[0][1] for z in imageMatrix[i - 1][indexList[i] + 1]])
            else:
                tuple2 = (0, 0, 0)

            if i - 1 > 0 and (indexList[i] + 2) < (column + 1):
                tuple3 = tuple([z * gaussianFilter[0][2] for z in imageMatrix[i - 1][indexList[i] + 2]])
            else:
                tuple3 = (0, 0, 0)

            if (indexList[i] - 1) > 0:
                tuple4 = tuple([z * gaussianFilter[1][0] for z in imageMatrix[i][indexList[i] - 1]])
            else:
                tuple4 = (0, 0, 0)

            if (indexList[i] + 1) < (column + 1):
                tuple5 = tuple([z * gaussianFilter[1][1] for z in imageMatrix[i][indexList[i] + 1]])
            else:
                tuple5 = (0, 0, 0)

            if (indexList[i] + 2) < (column + 1):
                tuple6 = tuple([z * gaussianFilter[1][2] for z in imageMatrix[i][indexList[i] + 2]])
            else:
                tuple6 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] - 1) > 0:
                tuple7 = tuple([z * gaussianFilter[2][0] for z in imageMatrix[i + 1][indexList[i] - 1]])
            else:
                tuple7 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] + 1) < (column + 1):
                tuple8 = tuple([z * gaussianFilter[2][1] for z in imageMatrix[i + 1][indexList[i] + 1]])
            else:
                tuple8 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] + 2) < (column + 1):
                tuple9 = tuple([z * gaussianFilter[2][2] for z in imageMatrix[i + 1][indexList[i] + 2]])
            else:
                tuple9 = (0, 0, 0)

            tuplesList = [tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9]
            imageMatrix[i][indexList[i]] = tuple(map(lambda y: int(sum(y)), zip(*tuplesList)))

        print(str(iteration + 1) + ". vertical seam is added.")

    print("\nAdd Vertical Seam Least is finished...\n")

    return imageMatrix


def addVerticalSeamMost(image, operator, numberOfPixels):
    print("\nAdd Vertical Seam Most is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignVerticalWeightsMost(matrix)

        row = len(matrix)
        column = len(matrix[0])

        largest_index = 0
        largest_value = matrix[0][0]
        for j in range(1, column):
            if matrix[0][j] > largest_value:
                largest_index = j
                largest_value = matrix[0][j]

        lastRowIndex = column - 1
        j = largest_index

        indexList = [j]

        for i in range(1, row - 1):
            secondValue = matrix[i + 1][j]

            firstValue = -1
            thirdValue = -1

            if j != 0:
                firstValue = matrix[i + 1][j - 1]

            if j != lastRowIndex:
                thirdValue = matrix[i + 1][j + 1]

            if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
                j = j - 1
            elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
                j = j + 1
            else:
                j = j

            indexList.append(j)
        indexList.append(j)

        imageMatrix = numpy.insert(imageMatrix, column-1, imageMatrix[:, column-1], axis=1)
        for i in range(row):
            for j in range(column, indexList[i]-1, -1):
                imageMatrix[i][j] = imageMatrix[i][j-1]

        for i in range(row):
            def getGaussianFilter():
                array = numpy.zeros((3, 3))
                sigma = 0.423
                for x in range(3):
                    for y in range(3):
                        firstTemp = (1 / (2 * pi * sigma**2))
                        secondTemp = (-1) * ((x**2 + y**2) / (2 * sigma**2))
                        array[x][y] = firstTemp * (e**secondTemp)

                return array

            gaussianFilter = getGaussianFilter()

            if i - 1 > 0 and (indexList[i] - 1) > 0:
                tuple1 = tuple([z * gaussianFilter[0][0] for z in imageMatrix[i - 1][indexList[i] - 1]])
            else:
                tuple1 = (0, 0, 0)

            if i - 1 > 0 and (indexList[i] + 1) < (column + 1):
                tuple2 = tuple([z * gaussianFilter[0][1] for z in imageMatrix[i - 1][indexList[i] + 1]])
            else:
                tuple2 = (0, 0, 0)

            if i - 1 > 0 and (indexList[i] + 2) < (column + 1):
                tuple3 = tuple([z * gaussianFilter[0][2] for z in imageMatrix[i - 1][indexList[i] + 2]])
            else:
                tuple3 = (0, 0, 0)

            if (indexList[i] - 1) > 0:
                tuple4 = tuple([z * gaussianFilter[1][0] for z in imageMatrix[i][indexList[i] - 1]])
            else:
                tuple4 = (0, 0, 0)

            if (indexList[i] + 1) < (column + 1):
                tuple5 = tuple([z * gaussianFilter[1][1] for z in imageMatrix[i][indexList[i] + 1]])
            else:
                tuple5 = (0, 0, 0)

            if (indexList[i] + 2) < (column + 1):
                tuple6 = tuple([z * gaussianFilter[1][2] for z in imageMatrix[i][indexList[i] + 2]])
            else:
                tuple6 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] - 1) > 0:
                tuple7 = tuple([z * gaussianFilter[2][0] for z in imageMatrix[i + 1][indexList[i] - 1]])
            else:
                tuple7 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] + 1) < (column + 1):
                tuple8 = tuple([z * gaussianFilter[2][1] for z in imageMatrix[i + 1][indexList[i] + 1]])
            else:
                tuple8 = (0, 0, 0)

            if (i + 1) < row and (indexList[i] + 2) < (column + 1):
                tuple9 = tuple([z * gaussianFilter[2][2] for z in imageMatrix[i + 1][indexList[i] + 2]])
            else:
                tuple9 = (0, 0, 0)

            tuplesList = [tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9]
            imageMatrix[i][indexList[i]] = tuple(map(lambda y: int(sum(y)), zip(*tuplesList)))

        print(str(iteration + 1) + ". vertical seam is added.")

    print("\nAdd Vertical Seam Most is finished...\n")

    return imageMatrix


def assignVerticalWeightsLeast(matrix):
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

    return matrix


def assignVerticalWeightsMost(matrix):
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

    return matrix


def removeHorizontalSeamLeast(image, operator, numberOfPixels):
    print("\nRemove Horizontal Seam Least is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignHorizontalWeightsLeast(matrix)

        row = len(matrix)
        column = len(matrix[0])

        smallest_index = 0
        smallest_value = matrix[0][0]
        for i in range(1, row):
            if matrix[i][0] < smallest_value:
                smallest_index = i
                smallest_value = matrix[0][i]

        lastColumnIndex = row-1
        i = smallest_index

        indexList = [i]

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

            indexList.append(i)
        indexList.append(i)

        for j in range(column):
            for k in range(indexList[j], row-2):
                imageMatrix[k][j] = imageMatrix[k+1][j]
        imageMatrix = numpy.delete(imageMatrix, -1, axis=0)

        print(str(iteration + 1) + ". horizontal seam is removed.")

    print("\nRemove Horizontal Seam Least is finished...\n")

    return imageMatrix


def removeHorizontalSeamMost(image, operator, numberOfPixels):
    print("\nRemove Horizontal Seam Most is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignHorizontalWeightsMost(matrix)

        row = len(matrix)
        column = len(matrix[0])

        largest_index = 0
        largest_value = matrix[0][0]
        for i in range(1, row):
            if matrix[i][0] > largest_value:
                largest_index = i
                largest_value = matrix[0][i]

        lastColumnIndex = row - 1
        i = largest_index

        indexList = [i]

        for j in range(1, column - 1):
            secondValue = matrix[i][j + 1]

            firstValue = -1
            thirdValue = -1

            if i != 0:
                firstValue = matrix[i - 1][j + 1]

            if i != lastColumnIndex:
                thirdValue = matrix[i + 1][j + 1]

            if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
                i = i - 1
            elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
                i = i + 1
            else:
                i = i

            indexList.append(i)
        indexList.append(i)

        for j in range(column):
            for k in range(indexList[j], row-2):
                imageMatrix[k][j] = imageMatrix[k+1][j]
        imageMatrix = numpy.delete(imageMatrix, -1, axis=0)

        print(str(iteration + 1) + ". horizontal seam is removed.")

    print("\nRemove Horizontal Seam Least is finished...\n")

    return imageMatrix


def addHorizontalSeamLeast(image, operator, numberOfPixels):
    print("\nAdd Horizontal Seam Least is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignHorizontalWeightsLeast(matrix)

        row = len(matrix)
        column = len(matrix[0])

        smallest_index = 0
        smallest_value = matrix[0][0]
        for i in range(1, row):
            if matrix[i][0] < smallest_value:
                smallest_index = i
                smallest_value = matrix[0][i]

        lastColumnIndex = row-1
        i = smallest_index

        indexList = [i]

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

            indexList.append(i)
        indexList.append(i)

        imageMatrix = numpy.insert(imageMatrix, row-1, imageMatrix[row-1], axis=0)
        for j in range(column):
            for i in range(row, indexList[i] - 1, -1):
                imageMatrix[i][j] = imageMatrix[i-1][j]

        for j in range(column):
            def getGaussianFilter():
                array = numpy.zeros((3, 3))
                sigma = 0.425
                for x in range(3):
                    for y in range(3):
                        firstTemp = (1 / (2 * pi * sigma**2))
                        secondTemp = (-1) * ((x**2 + y**2) / (2 * sigma**2))
                        array[x][y] = firstTemp * (e**secondTemp)

                return array

            gaussianFilter = getGaussianFilter()

            if (indexList[j] + 1) < row and (j - 1) > 0:
                tuple1 = tuple([z * gaussianFilter[0][0] for z in imageMatrix[indexList[j] + 1][j - 1]])
            else:
                tuple1 = (0, 0, 0)

            if (j - 1) > -1:
                tuple2 = tuple([z * gaussianFilter[1][0] for z in imageMatrix[indexList[j]][j - 1]])
            else:
                tuple2 = (0, 0, 0)

            if (indexList[j] - 1) > -1 and (j - 1) > 0:
                tuple3 = tuple([z * gaussianFilter[2][0] for z in imageMatrix[indexList[j] - 1][j - 1]])
            else:
                tuple3 = (0, 0, 0)

            if (indexList[j] + 1) < row:
                tuple4 = tuple([z * gaussianFilter[0][1] for z in imageMatrix[indexList[j] + 1][j]])
            else:
                tuple4 = (0, 0, 0)

            if (indexList[j] + 1) < row:
                tuple5 = tuple([z * gaussianFilter[1][1] for z in imageMatrix[indexList[j]][j]])
            else:
                tuple5 = (0, 0, 0)

            if (indexList[j] - 1) < -1:
                tuple6 = tuple([z * gaussianFilter[2][1] for z in imageMatrix[indexList[j] - 1][j]])
            else:
                tuple6 = (0, 0, 0)

            if (indexList[j] + 1) < row and (j + 1) < column:
                tuple7 = tuple([z * gaussianFilter[0][2] for z in imageMatrix[indexList[j] + 1][j + 1]])
            else:
                tuple7 = (0, 0, 0)

            if (j + 1) < column:
                tuple8 = tuple([z * gaussianFilter[1][2] for z in imageMatrix[indexList[j]][j + 1]])
            else:
                tuple8 = (0, 0, 0)

            if (indexList[j] - 1) > -1 and (j + 1) < column:
                tuple9 = tuple([z * gaussianFilter[2][2] for z in imageMatrix[indexList[j] - 1][j + 1]])
            else:
                tuple9 = (0, 0, 0)

            tuplesList = [tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9]
            imageMatrix[indexList[j]][j] = tuple(map(lambda y: int(sum(y)), zip(*tuplesList)))

        print(str(iteration + 1) + ". horizontal seam is added.")

    print("\nAdd Horizontal Seam Least is finished...\n")

    return imageMatrix


def addHorizontalSeamMost(image, operator, numberOfPixels):
    print("\nAdd Horizontal Seam Most is started...\n")

    imageMatrix = numpy.array(image)
    for iteration in range(numberOfPixels):
        resultImage = Image.fromarray(imageMatrix)
        if operator == 1:
            matrix = applySobelOperatorFilter(resultImage.convert("L"))
        else:
            matrix = applyLoGFilter(resultImage.convert("L"))

        matrix = assignHorizontalWeightsMost(matrix)

        row = len(matrix)
        column = len(matrix[0])

        largest_index = 0
        largest_value = matrix[0][0]
        for i in range(1, row):
            if matrix[i][0] > largest_value:
                largest_index = i
                largest_value = matrix[0][i]

        lastColumnIndex = row - 1
        i = largest_index

        indexList = [i]

        for j in range(1, column - 1):
            secondValue = matrix[i][j + 1]

            firstValue = -1
            thirdValue = -1

            if i != 0:
                firstValue = matrix[i - 1][j + 1]

            if i != lastColumnIndex:
                thirdValue = matrix[i + 1][j + 1]

            if firstValue != -1 and firstValue > secondValue and (thirdValue == -1 or firstValue > thirdValue):
                i = i - 1
            elif thirdValue != -1 and thirdValue > secondValue and (firstValue == -1 or thirdValue > firstValue):
                i = i + 1
            else:
                i = i

            indexList.append(i)
        indexList.append(i)

        imageMatrix = numpy.insert(imageMatrix, row-1, imageMatrix[row-1], axis=0)
        for j in range(column):
            for i in range(row, indexList[i] - 1, -1):
                imageMatrix[i][j] = imageMatrix[i-1][j]

        for j in range(column):
            def getGaussianFilter():
                array = numpy.zeros((3, 3))
                sigma = 0.423
                for x in range(3):
                    for y in range(3):
                        firstTemp = (1 / (2 * pi * sigma**2))
                        secondTemp = (-1) * ((x**2 + y**2) / (2 * sigma**2))
                        array[x][y] = firstTemp * (e**secondTemp)

                return array

            gaussianFilter = getGaussianFilter()

            if (indexList[j] + 1) < row and (j - 1) > 0:
                tuple1 = tuple([z * gaussianFilter[0][0] for z in imageMatrix[indexList[j] + 1][j - 1]])
            else:
                tuple1 = (0, 0, 0)

            if (j - 1) > -1:
                tuple2 = tuple([z * gaussianFilter[1][0] for z in imageMatrix[indexList[j]][j - 1]])
            else:
                tuple2 = (0, 0, 0)

            if (indexList[j] - 1) > -1 and (j - 1) > 0:
                tuple3 = tuple([z * gaussianFilter[2][0] for z in imageMatrix[indexList[j] - 1][j - 1]])
            else:
                tuple3 = (0, 0, 0)

            if (indexList[j] + 1) < row:
                tuple4 = tuple([z * gaussianFilter[0][1] for z in imageMatrix[indexList[j] + 1][j]])
            else:
                tuple4 = (0, 0, 0)

            if (indexList[j] + 1) < row:
                tuple5 = tuple([z * gaussianFilter[1][1] for z in imageMatrix[indexList[j]][j]])
            else:
                tuple5 = (0, 0, 0)

            if (indexList[j] - 1) < -1:
                tuple6 = tuple([z * gaussianFilter[2][1] for z in imageMatrix[indexList[j] - 1][j]])
            else:
                tuple6 = (0, 0, 0)

            if (indexList[j] + 1) < row and (j + 1) < column:
                tuple7 = tuple([z * gaussianFilter[0][2] for z in imageMatrix[indexList[j] + 1][j + 1]])
            else:
                tuple7 = (0, 0, 0)

            if (j + 1) < column:
                tuple8 = tuple([z * gaussianFilter[1][2] for z in imageMatrix[indexList[j]][j + 1]])
            else:
                tuple8 = (0, 0, 0)

            if (indexList[j] - 1) > -1 and (j + 1) < column:
                tuple9 = tuple([z * gaussianFilter[2][2] for z in imageMatrix[indexList[j] - 1][j + 1]])
            else:
                tuple9 = (0, 0, 0)

            tuplesList = [tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9]
            imageMatrix[indexList[j]][j] = tuple(map(lambda y: int(sum(y)), zip(*tuplesList)))

        print(str(iteration + 1) + ". horizontal seam is added.")

    print("\nAdd Horizontal Seam Most is finished...\n")

    return imageMatrix


def assignHorizontalWeightsLeast(matrix):
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

    return matrix


def assignHorizontalWeightsMost(matrix):
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
