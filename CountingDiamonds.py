def count_diamonds(diamond_map, num_of_diamonds):

    parcels = []
    minPlotSize = 9999

    def traverseField(startPos, mPS):
        plotDiamondCount = []
        plotHeight = 1
        for y1 in range(startPos[1], len(diamond_map)):  # Outer Diamond Map Loop
            plotDiamondCount.append([])  # Creates diamond count arr for each new tract analyzed
            plotWidth = 1
            for i in range(len(diamond_map[startPos[1]])):
                plotDiamondCount[-1].append(0)  # Populates diamond count arr with zeros

            for x1 in range(startPos[0], len(diamond_map[y1])):  # Inner Diamond Map Loop
                lookBack = 0 if x1 == 0 else 1
                plotDiamondCount[-1][x1] += diamond_map[y1][x1] + plotDiamondCount[-1][x1 - lookBack]
                # print(f"{diamond_map[y1][x1]} + {plotDiamondCount[-1][x1 - lookBack]}")
                # print(f"Result: {plotDiamondCount[-1][x1]}")

            for x1 in range(startPos[0], len(diamond_map[y1])):
                if len(plotDiamondCount) > 1:
                    northPlot = plotDiamondCount[len(plotDiamondCount) - 2][x1]
                else:
                    northPlot = 0
                plotDiamondCount[-1][x1] += northPlot
                # print(f" + {northPlot}")
                # print(f"Final Result: {plotDiamondCount[-1][x1]}")
                currPlotSize = plotWidth * plotHeight
                # print(f"currentPlotSize: {currPlotSize}")
                plotWidth += 1

                if plotDiamondCount[-1][x1] == num_of_diamonds:
                    # print(f"currentPlotSize: {currPlotSize}")
                    data = "Plot found containing {} diamonds at ({},{})"
                    # print(data.format(plotDiamondCount[-1][x1], (startPos[1], startPos[0]), (y1, x1)))
                    if currPlotSize < mPS:
                        data = "Smaller plot size {} acres found, clearing {} acre data."
                        # print(data.format(currPlotSize, mPS))
                        mPS = currPlotSize
                        parcels.clear()
                    if currPlotSize == mPS:
                        data = "{} diamonds at ({},{}) added to parcel"
                        # print(data.format(plotDiamondCount[-1][x1], (startPos[0], startPos[1]), (x1, y1)))
                        parcels.append([(startPos[1], startPos[0]), (y1, x1)])

            plotHeight += 1
        # print(plotDiamondCount)
        return mPS

    for y in range(len(diamond_map)):
        for x in range(len(diamond_map[y])):
            minPlotSize = traverseField((x, y), minPlotSize)

    # print(parcels)
    return parcels


diamond_maps1 = [[4, 5, 0, 2],
                 [10, 1, 2, 0],
                 [1, 0, 2, 1],
                 [0, 0, 1, 0]]

diamond_maps = [[8, 4, 2, 9, 9, 4, 5, 6, 10, 9],
                [3, 3, 6, 9, 7, 7, 5, 7, 7, 3],
                [0, 9, 8, 5, 5, 8, 0, 3, 9, 2]]

count_diamonds(diamond_maps1, 3)
