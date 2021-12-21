class PhotoDTO:
  def __init__(self, newPhotoIdx, newWorkIdx, newStoredFilePath, newLabel):
    self.photoIdx = newPhotoIdx
    self.workIdx = newWorkIdx
    self.storedFilePath = newStoredFilePath
    self.label = newLabel

  def getPhotoIdx(self):
    return self.photoIdx
  def setPhotoIdx(self, newPhotoIdx):
    self.photoIdx = newPhotoIdx

  def getWorkIdx(self):
    return self.workIdx
  def setWorkIdx(self, newWorkIdx):
    self.workIdx = newWorkIdx

  def getStoredFilePath(self):
    return self.storedFilePath
  def setStoredFilePath(self, newStoredFilePath):
    self.storedFilePath = newStoredFilePath

  def getLabel(self):
    return self.label
  def setLabel(self, newLabel):
    self.label = newLabel

  def __str__(self):
    return 'DTO : ' + '( ' + str(self.photoIdx) + ' / ' + str(self.workIdx) + ' / ' + self.storedFilePath + ' / '+ str(self.label) + ' ) '


class WorkDTO:
  def __init__(self, newWorkIdx, newPhotographerIdx):
    self.workIdx = newWorkIdx
    self.photographerIdx = newPhotographerIdx
  
  def getWorkIdx(self):
    return self.workIdx
  def setWorkIdx(self, newWorkIdx):
    self.workIdx = newWorkIdx

  def getPhotographerIdx(self):
    return self.photographerIdx
  def setPhotographerIdx(self, newPhotographerIdx):
    self.photographerIdx = newPhotographerIdx