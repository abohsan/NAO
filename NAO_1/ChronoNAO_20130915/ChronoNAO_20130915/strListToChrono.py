# -*- encoding: UTF-8 -*-

from time import mktime
from datetime import datetime
from math import sqrt


class StrListToChrono():
    """  Compute chronometric data from a list of string which contain timestamp  """
    
    def __init__(self, listOfTimeString, dateFormat):
        # Class initialization: transform date format and keep microsecond value
        self.list = []
        for d in listOfTimeString:
            tmp = datetime.strptime(d, dateFormat)
            self.list.append(mktime(tmp.timetuple()) * 1000 + tmp.microsecond / 1000)
        
    def __convert(self, microSecondValue):
        # Convert an integer representing microsecond in a list containing [hours, minutes, seconds, hundredth of a second]
        result = []
        curr = microSecondValue
        ratio = [36e5, 6e4, 1e3, 10] # conversion ratio [ms -> h, ms -> min, ms -> s, ms -> hos]
        for i in range(4):
            result.append(int(curr / ratio[i]))
            curr -= result[i] * ratio[i]
        return result
        
    def __translate(self, timeList):
        # Translate a list from self.__convert format to a string to speech for NAO
        unitStr = ["hours", "minutes", "seconds", "hundredth"]
        mess = ""
        for i in range(4):
            if timeList[i] > 0:
                mess += str(timeList[i]) + " " + unitStr[i] + " "
        return mess

    def __average(self, list):
        # Compute the average value of the data in the list
        return sum(list) / len(list)
        
    def __variance(self, list):
        # Compute the variance of the data in the list
        squareSum = sum([x**2 for x in list])        
        return squareSum / len(list) - self.__average(list)**2
        
    def __stdDeviation(self, list):
        # Compute the standard deviation of the data in the list
        return sqrt(self.__variance(list))
        
    def compute(self):
        try:
            # Compute statistics data
            self.delta = []
            for i in range(len(self.list)):
                if i > 0: self.delta.append(self.list[i] - self.list[i-1])
            self.isComputed = True
            return True
        except:
            return False
        
    def getStrNbOfLoops(self):
        # Return the number of loops stored in string format
        return str(len(self.delta))
    
    def getStrTotalValue(self):
        # Return sum of delta in string format
        totVal = int(sum(self.delta)) # in microsecond
        return self.__translate(self.__convert(totVal))
    
    def getStrTotalValue(self):
        # Return sum of delta in string format
        totVal = int(sum(self.delta)) # in microsecond
        return self.__translate(self.__convert(totVal))
    
    def getStrMaxValue(self):
        # Return max delta in string format
        maxVal = int(max(self.delta)) # in microsecond
        return self.__translate(self.__convert(maxVal))

    def getStrMinValue(self):
        # Return min delta in string format
        minVal = int(min(self.delta)) # in microsecond
        return self.__translate(self.__convert(minVal))

    def getStrAverageValue(self):
        # Return average delta in string format
        avgVal = int(self.__average(self.delta)) # in microsecond
        return self.__translate(self.__convert(avgVal))

    def getStrStdDeviationValue(self):
        # Return standard deviation of delta in string format
        stdDevVal = int(self.__stdDeviation(self.delta)) # in microsecond
        return self.__translate(self.__convert(stdDevVal))
