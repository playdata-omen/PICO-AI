findAllUnlabeled = "select photo_idx, work_idx, stored_file_path, label from photo where label is null"
findAllLabeled = "select photo_idx, work_idx, stored_file_path, label from photo where label is not null"
updateLabelQuery = "UPDATE photo SET label=%s WHERE photo_idx=%s"

findByWorkIdx = "select photographer_idx from work where work_idx=%s"