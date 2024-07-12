from db_connection_mongo import *

if __name__ == '__main__':

    # Connecting to the database
    db = connectDataBase()

    # Creating a collection
    users = db.users

    #print a menu
    print("")
    print("######### Menu ##############")
    print("#a - Create users and message")
    print("#b - Update a user")
    print("#c - Update a comment")
    print("#d - Delete a user and his/her comments")
    print("#e - Delete a comment")
    print("#f - Return a user")
    print("#g - Return the chat")
    print("#q - Quit")

    option = ""
    while option != "q":

          print("")
          option = input("Enter a menu choice: ")

          if (option == "a"):

              nUsers = input("Enter the number os users: ")

              commentId = 0
              for u in range(int(nUsers)):
                  userId = input("Enter the ID of user " + str(u + 1) + ": ")
                  userName = input("Enter the name of user " + str(u + 1) + ": ")
                  userEmail = input("Enter the email of user " + str(u + 1) + ": ")
                  createUser(users, userId, userName, userEmail)

                  comments = input("Enter the number of comments of user " + userName + ": ")
                  for c in range(int(comments)):
                      commentId += 1
                      commentText = input("Enter the text of " + userName + "'s " + str(c + 1) + " comment: ")
                      commentDate = input("Enter the date of " + userName + "'s " + str(c + 1) + " comment: ")
                      createComment(users, str(commentId), userId, commentText, commentDate)

          elif (option == "b"):

              userId = input("Enter the user id to be updated: ")
              userName = input("Enter the new name of user " + userId + ": ")
              userEmail = input("Enter the new email of user " + userId + ": ")

              updateUser(users, userId, userName, userEmail)

          elif (option == "c"):

              userId = input("Enter the user id: ")
              commentId = input("Enter the comment id to be updated: ")
              commentText = input("Enter the new text of comment " + commentId + ": ")
              commentDate = input("Enter the new date of comment " + commentId + ": ")

              updateComment(users, userId, commentId, commentText, commentDate)

          elif (option == "d"):

              userId = input("Enter the user id to be deleted: ")

              deleteUser(users, userId)

          elif (option == "e"):

              userId = input("Enter the user id: ")
              commentId = input("Enter the comment id to be deleted: ")

              deleteComment(users, userId, commentId)

          elif (option == "f"):

              nameUser = input("Enter the name of the user to be returned:  ")

              print(getUser(users, nameUser))

          elif (option == "g"):

              print(getChat(users))

          elif (option == "q"):

               print("Leaving the application ... ")

          else:

               print("Invalid Choice.")




