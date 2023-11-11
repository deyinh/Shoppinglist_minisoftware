# --------------------------------------------------------------------------- #
#                                                                             #
# Sail() Submitter                                                            #
#                                                                             #
# Please, set the following variables as needed.                              #
#                                                                             #
# TASK_NUMBER:         An integer which specifies the number of a task for    #
#                      which the submission is being made. For example, set   #
#                      this value to 1 to submit to Task 1 of the project.    #
#                                                                             #
# REFRESH_CREDENTIALS: A boolean which specifies if the stored credentials    #
#                      should be used (when set to `False`), or if the user   #
#                      should be prompted to enter the credentials (when set  #
#                      to `True`).                                            #
#                      If no credetnials have been stored yet the user will   #
#                      be prompted to enter the credentials regardless of the #
#                      value provided to this parameter.                      #
#                                                                             #
# --------------------------------------------------------------------------- #
TASK_NUMBER = 6
REFRESH_CREDENTIALS = True

# --------------------------------------------------------------------------- #
#                                                                             #
# No changes to the code below                                                #
#                                                                             #
# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    from submitter_utils import submit
    submit(TASK_NUMBER, REFRESH_CREDENTIALS)
