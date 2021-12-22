findAllUnlabeled = "SELECT photo_idx, work_idx, stored_file_path, label FROM photo WHERE label is NULL"
findAllLabeled = "SELECT photo_idx, work_idx, stored_file_path, label FROM photo WHERE label is not NULL"
updateLabelQuery = "UPDATE photo SET label=%s WHERE photo_idx=%s"

findPhotographerIdx = "SELECT photographer_idx FROM work WHERE work_idx=%s"