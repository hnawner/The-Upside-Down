class Level(object):
    def __init__(self, overworld, upsideDown, persistent, player):
        self.overworld = overworld
        self.upsideDown = upsideDown
        self.persistent = persistent
        self.player = player

    def __repr__(self):
        #Taken from CMU 15-112 Lecture Notes
        def maxItemLength(a):
            maxLen = 0
            rows = len(a)
            cols = len(a[0])
            for row in range(rows):
                for col in range(cols):
                    maxLen = max(maxLen, len(str(a[row][col])))
            return maxLen

        #Adapted from CMU 15-112 Lecture Notes
        def strFrom2dList(a):
            strOut = ""

            if (a == []):
                strOut += ("[]")
                return
            rows = len(a)
            cols = len(a[0])
            fieldWidth = maxItemLength(a)
            strOut += ("[ ")
            for row in range(rows):
                if (row > 0): strOut += ("\n  ")
                strOut += ("[ ")
                for col in range(cols):
                    if (col > 0): strOut += (", ")
                    # The next 2 lines print a[row][col] with the given fieldWidth
                    formatSpec = "%" + str(fieldWidth) + "s"
                    strOut += (formatSpec % str(a[row][col]))
                strOut += (" ]")
            strOut += ("]")

            return strOut

        strOut = (strFrom2dList(self.overworld) + "\n" + 
                  strFrom2dList(self.persistent) + "\n" + 
                  strFrom2dList(self.upsideDown))
        
        return strOut