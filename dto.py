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