import re


def create_qr_code(text):
    bits = "0100"  # indicates byte mode
    # Convert length of text to 8 bit binary string and append to bits
    bits += '{0:08b}'.format(len(text))
    messagePolynomial = [0 for x in range(9)]

    for char in text:  # Append binary Ascii value of each character in text to bit
        bits += '{0:08b}'.format(ord(char))

    bitLength = len(bits)
    bitRemainder = 8 - bitLength % 8
    bits += "0" * bitRemainder

    def incBitLength(fBits, switch):  # Inc bits length to 72 by appending 11101100 and 00010001 alternating
        bitExtender = ["11101100", "00010001"]
        if len(fBits) == 72:
            return fBits
        else:
            fBits += bitExtender[switch]
            switch ^= 1
            return incBitLength(fBits, switch)

    bits = incBitLength(bits, 0)

    bitSeqGroups = re.findall('........', bits)  # Split bits into groups of 8
    for i, x in enumerate(bitSeqGroups):  # Encode bits as base 10
        messagePolynomial[i] = int(x, 2)


    gPxaEArr = []
    xOrArr = []
    genPoly = [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136]

    def errorCorrection(mP, repetitions):
        if repetitions == 0:
            return mP
        if mP[0] == 0:
            mP.pop(0)
            repetitions -= 1
            return errorCorrection(mP, repetitions)
        alphaExponent = alphaTable[mP[0]]  # Table Conversion
        newMP = []
        for term in genPoly:  # Exponent multiplication
            exponent = alphaExponent + term
            if exponent > 254:
                exponent = exponent % 255
            gPxaEArr.append(exponent)
        for term in gPxaEArr:  # Table Conversion
            xOrArr.append(alphaTable.index(term))
        for ind, convertedExp in enumerate(xOrArr):
            if ind < len(mP):
                newMP.append(convertedExp ^ mP[ind])
            else:
                newMP.append(convertedExp)
        if newMP[0] == 0:
            # print("Lead term is zero!")
            newMP.pop(0)
            xOrArr.clear()
            gPxaEArr.clear()
            repetitions -= 1
            return errorCorrection(newMP, repetitions)
        else:
            print("Error, lead term not equal to zero")

    messagePolynomial = errorCorrection(messagePolynomial, len(messagePolynomial))
    # print(messagePolynomial)!
    while len(messagePolynomial) < 17:
        messagePolynomial.insert(0, 0)
    for x in messagePolynomial:
        bits += '{0:08b}'.format(x)
    # print(bits)!

    # Hard Coded Table
    qrTable = [[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
               [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
               [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
               [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1]]

    def modifyQRTable(qrT):
        for y in range(6):
            for x in range(9, 13):
                qrT[y][x] = 9
        for y in range(7, len(qrT)):
            for x in range(9, 13):
                qrT[y][x] = 9
        for y in range(9, 13):
            for x in range(0, 6):
                qrT[y][x] = 9
        for y in range(9, 13):
            for x in range(7, 9):
                qrT[y][x] = 9
        for y in range(9, len(qrT)):
            for x in range(13, 21):
                qrT[y][x] = 9
        return qrT
    qrTable = modifyQRTable(qrTable)

    def checkInvert(x, y, bit, bitsIndex):
        # print("Checking Inversion")
        bitsIndex += 1
        intBit = int(bit)
        invert = (x + y) % 2 == 0
        if invert:
            intBit ^= 1
        # print(f"Modifying {y} {x}")
        return intBit, bitsIndex

    def lookAhead(qrT, x, y):
        # print(f"Checking x:{x}, y{y} for legality")
        if x < 0:
            return False
        if y > 20 or y < 0:
            return False
        if qrT[y][x] == 9:
            return True
        else:
            return False

    def buildFinalQRTable(qrT, x, y, trend, bitsIndex, stopFound, stopLoc):  # dirMod (x, y)
        if stopFound:
            return qrT, bitsIndex
        legalMoves = True
        dirMod = [[-1, 0], [1, -1]]
        dirMod[1][1] *= trend
        qrT[y][x], bitsIndex = checkInvert(x, y, bits[bitsIndex], bitsIndex)  # Adding value to qrTable
        while legalMoves:
            x += dirMod[0][0]
            y += dirMod[0][1]
            qrT[y][x], bitsIndex = checkInvert(x, y, bits[bitsIndex], bitsIndex)  # Adding value to qrTable
            if x == stopLoc[0] and y == stopLoc[1]:
                return buildFinalQRTable(qrT, x, y, trend, bitsIndex, True, stopLoc)
                break
            x += dirMod[1][0]
            y += dirMod[1][1]
            legalMoves = lookAhead(qrT, x, y)
            if legalMoves:
                qrT[y][x], bitsIndex = checkInvert(x, y, bits[bitsIndex], bitsIndex)  # Adding value to qrTable
            else:
                x -= dirMod[1][0]
                y -= dirMod[1][1]
                x -= 1
                trend *= -1
                return buildFinalQRTable(qrT, x, y, trend, bitsIndex, stopFound, stopLoc)

    # Table, startx, starty, switch, startingBitIndex, stopFound, stopLoc
    qrTable, bitsIndex = buildFinalQRTable(qrTable, 20, 20, 1, 0, False, [11, 7])
    qrTable, bitsIndex = buildFinalQRTable(qrTable, 12, 5, 1, bitsIndex, False, [9, 5])
    qrTable, bitsIndex = buildFinalQRTable(qrTable, 10, 7, -1, bitsIndex, False, [9, 20])
    qrTable, bitsIndex = buildFinalQRTable(qrTable, 8, 12, 1, bitsIndex, False, [7, 9])
    qrTable, bitsIndex = buildFinalQRTable(qrTable, 5, 9, -1, bitsIndex, False, [0, 12])

    for x1 in qrTable:
        print(x1)
    # htmlTable = htmlize(qrTable)
    # print(htmlTable)
    return qrTable


alphaTable = [-1, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28,
              193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29,
              181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253,
              226, 152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70,
              64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21,
              121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49,
              197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91,
              149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60,
              57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108,
              161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 169, 160, 81,
              11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80,
              88, 175]

create_qr_code("Hey Dad")

# α0x25+α43x24+α139x23+α206x22+α78x21+α43x20+α239x19+α123x18+α206x17+α214x16+α147x15+α24x14+α99x13+α150x12+α39x11+α243x10+α163x9+α136x8

# There are 2 arrays. Message Polynomial and generator polynomial.
# Take coefficient of lead term in MP and convert with table.
# Take this value and add(multiply) it with all values in gP.
# If a value is bigger than 254 do % 255
# Now convert all values back with table index
# Now Xor these values with the coeff of mP
# The lead term should now be zero. Drop it. This is the new messagePolynomia
# If next term is a zero drop it, but repeating this process len(mP) times
#
#          [[ 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1 ],
#           [ 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1 ],
#           [ 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ],
#           [ 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1 ],
#           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ],
#           [ F, F, F, F, F, F, F, F, F, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1 ],
#         9 [ 1, 1, 0, 1, 1, 0, B, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1 ],
#           [ 1, 0, 0, 0, 0, 0, B, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1 ],
#           [ 1, 1, 1, 1, 1, 1, B, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0 ],
#           [ 1, 1, 0, 0, 0, 0, B, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0 ],
#           [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0 ],
#           [ 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1 ],
#           [ 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0 ],
#           [ 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1 ],
#           [ 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0 ],
#           [ 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1 ]]
