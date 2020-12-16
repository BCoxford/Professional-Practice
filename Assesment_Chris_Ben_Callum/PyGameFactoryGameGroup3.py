import pygame
from pygame.locals import *
import sys
import time

def calculateFuelCost(fuelCost, trucks):
    averageFuel = 1020 #Miles per month average on 60 miles per day.
    cost = averageFuel * fuelCost * trucks
    return cost

def calculateElectricityCost(electricCost, electricUsed):
    cost = electricCost*electricUsed
    return cost

def calculateEmployeeCost(employees, wage):
    cost = employees*wage
    return cost

def calculateMatCost(materialUsed, materialCost):
    cost = materialUsed*materialCost
    return cost

def calculateOutput(temperature, pressure, outputMult):
    optimumTemp = 230 #Celcius
    optimumPressure = 200 #Tonnes

    maxValue = outputMult * 5000
    out = (temperature+pressure)/(optimumTemp+optimumPressure)*outputMult*5000
    waste = maxValue-out
    return out, waste

def calculateSales(output, productPerBox, employees, loadTime, trucks, salesBudget, reputation):
    numberSets = (output/250)*100
    boxesPerMonth = int(numberSets/productPerBox)
    speed = (employees/loadTime)
    deliveredBoxesPerMonth = (boxesPerMonth/trucks)*speed

    setsPerMonth = deliveredBoxesPerMonth * numberSets

    salesEffectiveness = (salesBudget*reputation)/10 #Ten being the cut-off point affecting sales.

    sales = setsPerMonth/salesEffectiveness

    return sales

def calculateCashOut(matCost, employeeCost, electricityCost, fuelCost):
    cashOut = matCost + employeeCost + electricityCost + fuelCost
    return cashOut

def calculateProfit(sales, setCost, cashPerMonth):
    profit = (sales*setCost)-cashPerMonth
    return profit

def main():
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        w, h = pygame.display.get_surface().get_size()
        pygame.display.set_caption('Workflow Management Game')
        pygame.font.init()

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((30, 30, 30))

        #All Based Per Month
        cash = 100000
        electricKWatt = 10
        electricityCostPer = 160
        employees = 1
        wage = 5.60
        materialUsed = 10
        materialCostPer = 3000
        outMult = 1
        wastage = 0
        productPerBox = 20
        temperature = 100
        pressure = 100
        loadTime = 5
        productQuality = 10
        maxStorage = 1000
        numColours = 1
        salesBudget = 100
        numSilos = 1
        reputation = 1
        fuelCostPer = 1.30
        profitPer = 40
        trucks = 1

        data = [1,1,1,1,1,1,1,1,1,1]
        #affects = [temperature, pressure, electricityCost, employeeCost, matCost, outputTime, loadTime, wastage, productPerBox, productQuality, maxStorage, numColours, salesBudget, numSilos, reputation, fuelCost]
        #infoGrid = [Name, BaseCost, IncreasePerLevel, levelIndex, Affects]

        infoGrid = [["+1 Line", 35000, 15000, 0, [None, None, ["+1000kW/m", 1000, False], None, None, ["x2 Output", 2, True], None, None, None, None, None, None, None, None, None, None]],
        ["-1 Line", 5000, 0, 0, [None, None, ["-300kW/m", -1000, True], None, None, ["x0.5 Output", 0.5, False], None, None, None, None, None, None, None, None, None, None]],
        ["+1 Conveyor Speed", 10000, 0, 1, [None, None, ["+300kW/m", 300, False], None, None, ["x1.25 Output", 1.25, True], None, None, None, None, None, None, None, None, None, None]],
        ["-1 Conveyor Speed", 10000, 0, 1, [None, None, ["-300kW/m", -300, True], None, None, ["x0.8 Output", 0.8, False], None, None, None, None, None, None, None, None, None, None]],
        ["+1 Silo", 15000, 0, 2, [None, None, None, None, None, None, None, None, None, None, ["+1000 Tonnes", 1000, True], ["+1 Colour", 1, True], None, ["+1 Silo", 1, True], None, None]],
        ["-1 Silo", 5000, 0, 2, [None, None, None, None, None, None, None, None, None, None, ["-1000 Tonnes", -1000, False], ["-1 Colour", -1, False], None, ["-1 Silo", -1, False], None, None]],
        ["+10C Temperature", 0, 0, 3, [["+10C", 10, True], None, ["+100kW/m", 100, False], None, None, ["-5s Production",-5, True], None, None, None, ["-1 Quality", -1, False], None, None, None, None, None, None]],
        ["-10C Temperature", 0, 0, 3, [["-10C", -10, False], None, ["-100kW/m", -100, True], None, None, ["+5s Production", 5, False], None, None, None, ["+1 Quality", 1, True], None, None, None, None, None, None]],
        ["+50T Pressure", 0, 0, 4, [None, ["+50T", 50, True], None, ["+100kW/m", 100, False], None, ["-5s Production",-5, True], None, None, None, ["-1 Quality", -1, False], None, None, None, None, None, None]],
        ["-50T Pressure", 0, 0, 4, [None, ["-50T", -50, False], None, ["-100kW/m", -100, True], None, ["+5s Production", 5, False], None, None, None, ["+1 Quality", 1, True], None, None, None, None, None, None]],
        ["+1 Truck", 25000, 0, 5, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ["+£1000 p/m", 1000, False]]],
        ["-1 Truck", 8000, 0, 5, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ["-£1000 p/m", -1000, True]]],             
        ["+1 Box Size", 5000, 0, 6, [None, None, None, None, None, None, None, None, ["x2 Product", 2, True], None, None, None, None, None, None, None]],
        ["-1 Box Size", 5000, 0, 6, [None, None, None, None, None, None, None, None, ["/2 Product", 2, True], None, None, None, None, None, None, None]],
        ["+1 Storage Size", 10000, 0, 7, [None, None, None, None, None, None, None, None, None, None, ["x2 Storage Size", 2, True], None, None, None, None, None]],
        ["-1 Storage Size", 4000, 0, 7, [None, None, None, None, None, None, None, None, None, None, ["/2 Storage Size", 2, False], None, None, None, None, None]],
        ["+ Marketing Budget", 5000, 0, 8, [None, None, None, None, None, None, None, None, None, None, None, None, ["+£5000 Budget", 5000, False], None, None, None]],
        ["- Marketing Budget", 5000, 0, 8, [None, None, None, None, None, None, None, None, None, None, None, None, ["-£5000 Budget", -5000, True], None, None, None]], 
        ["+5 Packers", 5000, 0, 9, [None, None, None, None, None, None, ["/2 Load Time", 2, True], None, None, None, None, None, None, None, None, None]],
        ["-5 Packers", 5000, 0, 9, [None, None, None, None, None, None, ["x2 Load Time", 2, False], None, None, None, None, None, None, None, None, None]],
        ["+ Material Budget", 5000, 0, 10, [None, None, None, None, ["x0.9 Cost", 0.9, True], None, None, None, None, None, None, None, None, None, None, None]],
        ["- Material Budget", 5000, 0, 10, [None, None, None, None, ["x1.1 cost", 1.1, False], None, None, None, None, None, None, None, None, None, None, None]],
        ["+1 Truck Speed", 10000, 0, 11, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]],#Need to add this
        ["-1 Truck Speed", 4000, 0, 11, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]], #Need to add this
        ["+1 Robot Upgrade", 500000, 0, 12, [None, None, None, ["/4 Employee Cost", 4, True], None, None, None, None, None, None, None, None, None, None, ["-5 Rep", -5, False], None]],
        ["-1 Waste Machine", 250000, 0, 12, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, ["+10 Rep", 10, True], None]],               
        ["+ Solar Panel", 5000, 0, 13, [None, None, ["+500kW/m", +500, True], None, None, None, None, None, None, None, None, None, None, None, ["+1 Rep", 1, True], None]],
        ["- Solar Panel", 2000, 0, 13, [None, None, ["-500kW/m", -500, False], None, None, None, None, None, None, None, None, None, None, None, ["-1 Rep", -1, False], None]],
        ["+1 Electricity", 5000, 0, 14, [None, None, ["+500kW/m", +500, True], None, None, None, None, None, None, None, None, None, None, None, None, None]],
        ["-1 Electricity", 5000, 0, 14, [None, None, ["-500kW/m", -500, False], None, None, None, None, None, None, None, None, None, None, None, None, None]]
        ]

        grid = []
        gridSurfaces = []
        w = w - 160 - 320
        h = h - 160

        total = 0
        
        fontSize = int((w/h)*10)
        font = pygame.font.SysFont('Comic Sans MS', fontSize)

        for column in range(0,5):
                    for row in range(0,4):
                        surface = pygame.Surface(((w/5/1.25), (h/4/1.25)))
                        surface.fill((0,0,0))
                        surface.set_alpha(220)
                        gridSurfaces.append([surface, (((column*(w/5)))+20, ((row*(h/4)))+100)])

        while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.locals.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = event.pos
                        button = None
                        for i in grid:
                            if i.collidepoint(mousePos):
                                button = i

                        if not (button is None):
                            index = grid.index(button)
                            info = infoGrid[index]
                            levelIndex = info[3]
                            cost = info[1] + (data[levelIndex]-1)*info[2]
                            if((cash - cost) >= 0):
                                affects = info[4]
                                levelIndex = info[3]
                                data[levelIndex] = data[levelIndex] + 1
                                cash = cash - cost
                                for x in affects:
                                    if not (x is None):
                                        #Affects
                                        continue
                            else:
                                print("Not Enough")

                output, wastage = calculateOutput(temperature, pressure, outMult)
                fuelCost = calculateFuelCost(fuelCostPer, trucks)
                materialCost = calculateMatCost(materialUsed, materialCostPer)
                electricCost = calculateElectricityCost(electricKWatt, electricityCostPer)
                empCost = calculateEmployeeCost(employees, wage)
                numSales = calculateSales(output, productPerBox, employees, loadTime, trucks, salesBudget, reputation)
                cashOut = calculateCashOut(materialCost, empCost, electricCost, fuelCost)
                profit = calculateProfit(numSales, profitPer, cashOut)
                cash = cash + profit

                nWidth = int(w/8/1.25*4)-120
                nHeight = int(h-45)
                surfaceStats = pygame.Surface((nWidth, nHeight))
                surfaceStats.fill((0,0,0))
                surfaceStats.set_alpha(220)

                csh = "Cash: £" + str(int(cash))
                TextCash = font.render(csh, True, (255,255,255))
                surfaceStats.blit(TextCash, ((20,20)))
                        
                for n in gridSurfaces:
                        surface = n[0]
                        try:
                                info = infoGrid[total]
                                level = data[info[3]]-1
                                price = info[1] + level*int(info[2])
                                price = "£" + str(price)

                                arrayAffects = []
                                for x in info[4]:
                                        if not (x is None):
                                             arrayAffects.append(x)

                                try:
                                        if(arrayAffects[0][2] == True):
                                                TextSurface1 = font.render(arrayAffects[0][0], True, (0,255,0))
                                                surface.blit(TextSurface1, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-20-(fontSize*4)))
                                        else:
                                                TextSurface1 = font.render(arrayAffects[0][0], True, (255,0,0))
                                                surface.blit(TextSurface1, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-20-(fontSize*4)))
                                except:
                                        e = sys.exc_info()[0]
                                        #print(e)

                                try:
                                        if(arrayAffects[1][2] == True):
                                                TextSurface2 = font.render(arrayAffects[1][0], True, (0,255,0))
                                                surface.blit(TextSurface2, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-30-(fontSize*5)))
                                        else:
                                                TextSurface2 = font.render(arrayAffects[1][0], True, (255,0,0))
                                                surface.blit(TextSurface2, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-30-(fontSize*5)))
                                except:
                                        e = sys.exc_info()[0]
                                        #print(e)

                                try:
                                        if(arrayAffects[2][2] == True):
                                                TextSurface3 = font.render(arrayAffects[2][0], True, (0,255,0))
                                                surface.blit(TextSurface3, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-40-(fontSize*6)))
                                        else:
                                                TextSurface3 = font.render(arrayAffects[2][0], True, (255,0,0))
                                                surface.blit(TextSurface3, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-40-(fontSize*6)))
                                except:
                                        e = sys.exc_info()[0]
                                        #print(e)

                                try:
                                        if(arrayAffects[3][2] == True):
                                                TextSurface4 = font.render(arrayAffects[3][0], True, (0,255,0))
                                                surface.blit(TextSurface4, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-50-(fontSize*7)))
                                        else:
                                                TextSurface4 = font.render(arrayAffects[3][0], True, (255,0,0))
                                                surface.blit(TextSurface4, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-50-(fontSize*7)))
                                except:
                                        e = sys.exc_info()[0]
                                        #print(e)


                                TextSurface = font.render(price, True, (133,187,101))

                                TextSurface5 = font.render(str(info[0]), True, (255,255,255))
                                surface.blit(TextSurface, (((w/5/1.25)-(fontSize*14)),((h/4/1.25)-10-(fontSize*3))))
                                surface.blit(TextSurface5, (((w/5/1.25)-(fontSize*14)),(h/4/1.25)-60-(fontSize*8)))
                        except:
                                e = sys.exc_info()[0]
                                #print(e)

                        grid.append(background.blit(surface, n[1]))
                        total = total+1

                background.blit(surfaceStats, (w,100) )
                screen.blit(background, (0, 0))

                pygame.display.update()
                time.sleep(1)

if __name__ == '__main__':
        main()
