import pyroomacoustics as pra



def initializeRoom(roomDimensions,sampleRate,order):
    
    #Initilializes a shoebox room with the given dimensions, sample rate and Order.
    
    room=pra.ShoeBox(roomDimensions,fs=sampleRate,max_order=order)

    return room


def updateMicPosition(roomDimensions,currenPosition,jumpFactor):
    #Update Mic Postion based on room geometry and jump Factor
    
    
    return newPosition
    
    
def randomizeSourcePositions(room,roomDimensions):
    #Randomizes Sources Postions for a new Scenario
    #Also resets mic postion to default
