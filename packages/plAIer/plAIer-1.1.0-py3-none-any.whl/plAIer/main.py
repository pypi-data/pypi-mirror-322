import json
import threading
import os

lock = threading.Lock()

class game():
    jsonDataFile = None
    data = None
    outcomesRating = None
    gameStates = None
    isFinished = None
    
    def __init__(self, jsonDataFile, outcomesRating):
        if not os.path.exists(jsonDataFile): # If the database file doesn't exist
            raise FileNotFoundError("Database file not found !")
        
        try:
            self.jsonDataFile = jsonDataFile
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError("The JSON file is malformed !")
        
        self.data = eval(str(json.load(open(jsonDataFile))))
        
        if not list(outcomesRating.keys()) == self.data["outcomes"]:
            raise ValueError("The outcomes model is not properly filled out.")
        for outcome in self.data["outcomes"]:
            if type(outcomesRating[outcome]) != int and if type(outcomesRating[outcome]) != float:
                raise ValueError("The outcomes model is not properly filled out.")
        self.outcomesRating = outcomesRating
        self.gameStates = []
        self.isFinished = False


    def findBestMove(self, possibleMoves):
        """Find the best move based on the game state."""
        
        if self.isFinished: # If the game is already finished
            raise RuntimeError("This game is already finished !")
        
        if possibleMoves == []: # If there are no possible moves
            raise ReferenceError("No possible move has been proposed.")

        # If the AI does not recognize one of the proposed moves, create an empty model
        emptyJson = {}
        for outcome in self.data["outcomes"]:
            emptyJson[outcome] = 0
        for possibleMove in possibleMoves:
            if not possibleMove["stateAfterMove"] in self.data["moves"]:
                self.data["moves"][possibleMove["stateAfterMove"]] = dict(emptyJson)

        # Find the common characters among all the boards
        commonCharIndexes = []
        try:
            for i in range(len(possibleMoves[0]["stateAfterMove"])):
                char = possibleMoves[0]["stateAfterMove"][i]
                matchingChar = True
                for move in possibleMoves:
                    if move["stateAfterMove"][i] != char:
                        matchingChar = False
                if matchingChar:
                    commonCharIndexes.append(i)
        except IndexError:
            pass
        
        # Determine the best move
        expectation = None
        plannedMove = None
        stateAfterMove = None
        for possibleMove in possibleMoves:
            moveStatistics = self.data["moves"][possibleMove["stateAfterMove"]]
            moveExpectation = 0
            for i in range(len(moveStatistics)):
                moveExpectation += self.outcomesRating[list(moveStatistics.keys())[i]] * list(moveStatistics.values())[i]
            try:
                moveExpectation = moveExpectation/sum(list(moveStatistics.values()))
            except ZeroDivisionError:
                pass

            sumOutcomes = 0
            denominator = 0
            for i in range(len(possibleMove["stateAfterMove"])):
                if not i in commonCharIndexes:
                    for possibleMove1 in self.data["moves"].keys():
                        try:
                            if possibleMove1[i] == possibleMove["stateAfterMove"][i]:
                                for outcome in self.data["outcomes"]:
                                    sumOutcomes += self.outcomesRating[outcome] * self.data["moves"][possibleMove1][outcome]
                                    denominator += self.data["moves"][possibleMove1][outcome]
                        except IndexError:
                            pass
            try:
                moveExpectation += sumOutcomes/denominator
            except ZeroDivisionError:
                moveExpectation = 0
            
            if expectation == None or expectation < moveExpectation:
                expectation = moveExpectation
                plannedMove = possibleMove["move"]
                stateAfterMove = possibleMove["stateAfterMove"]
        
        self.gameStates.append(stateAfterMove) # Save the move to know if it was a successful move
        return plannedMove


    def setOutcome(self, outcome):
        """Tell the AI what the outcome of the game is."""
        
        if not outcome in self.outcomesRating.keys(): # If the provided outcome doesn't exist
            raise ValueError(f"The item '{outcome}' is not in the expected outcomes list.")
        
        lock.acquire() # In case the file is used by two different instances of the program
        self.isFinished = True
        importedJson = eval(str(json.load(open(self.jsonDataFile)))) # Import the data from the original file

        # If the AI made a move not known to the database
        emptyJson = {}
        for outcome1 in self.data["outcomes"]:
            emptyJson[outcome1] = 0
            
        for gameState in self.gameStates: # Save the outcome of the game
            if not gameState in importedJson["moves"]:
                importedJson["moves"][gameState] = dict(emptyJson)
            importedJson["moves"][gameState][outcome] += 1
        json.dump(importedJson, open(self.jsonDataFile, 'w'))
        lock.release()




def createDatabase(filename, name, description, outcomes):
    """Create a new database."""
    
    if os.path.exists(filename): # If the file already exists
        raise FileExistsError(f"The file '{filename}' already exists")

    # Create a new database
    databaseContent = {"name": name, "description": description, "outcomes": outcomes, "moves":{}}
    database = json.dump(databaseContent, open(filename, 'w'))

