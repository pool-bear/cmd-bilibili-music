import sys
import search as s
import play as p

try:
    keyword = sys.argv[1]
except:
    print("Usage: python search.py <keyword>")
    sys.exit(1)
order = "x"
video_matrix, page, numPages = s.search(keyword, page = 1)
while order != "q":
    order = input("Enter page number or direction: ")
    if(order == "-" or order == "="):
        page = s.turnPage(order, page, numPages)
        video_matrix, page, numPages = s.search(keyword, page)
    elif order=="r":
        keyword = input("Enter new keyword: ")
        video_matrix, page, numPages = s.search(keyword, page = 1)
    else:
        try:
            no = int(order)
            if no > 0 and no <= len(video_matrix):
                p.play(video_matrix[no - 1]["bvid"])
        except:
            if order != "q":
                print("Invalid input")