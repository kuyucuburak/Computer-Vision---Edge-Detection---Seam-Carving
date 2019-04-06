import numpy

from PIL import Image
from math import e
from math import pi


def main():
    image = Image.open('gray.jpg').convert('L')

    print("SobelOperator(image) is started!")
    resultImage = sobelOperator(image)
    resultImage.save("Sobel_Operator.png")
    resultImage.show()
    print("\"Sobel_Operator.png\" is saved successfully!")
    print("SobelOperator(image) is finished!\n")

    number = input("Enter the filter size such as \"3\", \"5\": ")
    try:
        number = int(number)
    except ValueError:
        print("Please enter an integer such as \"3\", \"5\"")
        exit(1)

    print("\napplyFilter(LoGFilter, image) started!")
    resultImage = LoGFilter(image, getLoGFilter(number))
    resultImage.save('Laplacian_Gaussian.png')
    resultImage.show()
    print("\"Laplacian_Gaussian.png\" is saved successfully!")
    print("applyFilter(LoGFilter, image) finished!")


def sobelOperator(image):
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
    G = G.astype(numpy.uint8)

    for n in range(number):
        G = numpy.delete(G, 0, axis=0)

    for n in range(number):
        G = numpy.insert(G, 0, G[0], axis=0)

    for n in range(number):
        G = numpy.delete(G, 0, axis=1)

    for n in range(number):
        G = numpy.insert(G, 0, G[:, 0], axis=1)

    image = Image.fromarray(G)

    return image


def LoGFilter(image, myFilter):
    matrix = numpy.array(image)

    number = len(myFilter)

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

    resultArray = resultArray.astype(numpy.uint8)

    for i in range(number):
        resultArray = numpy.delete(resultArray, 0, axis=0)

    for i in range(number):
        resultArray = numpy.insert(resultArray, 0, resultArray[0], axis=0)

    for i in range(number):
        resultArray = numpy.delete(resultArray, 0, axis=1)

    for i in range(number):
        resultArray = numpy.insert(resultArray, 0, resultArray[:, 0], axis=1)

    image = Image.fromarray(resultArray)

    return image


def getLoGFilter(number):
    shape = (number, number)

    array = numpy.zeros(shape)
    sigma = 0.50
    for x in range(number):
        for y in range(number):
            firstTemp = ((-1) / (pi * sigma ** 4))
            secondTemp = (-1) * ((x ** 2 + y ** 2) / (2 * sigma ** 2))
            array[x][y] = firstTemp * (1 + secondTemp) * (e ** secondTemp)

    return array


if __name__ == "__main__":
    main()
