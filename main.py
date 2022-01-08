import requests
import json

notionToken = "INSERT INTEGRATION TOKEN HERE"
notionID = "INSERT NOTION ID HERE"

class Notion:
    def __init__(self, notionToken):
        self.headers = {
            'Notion-Version': '2021-05-13',
            'Authorization': 'Bearer ' + notionToken
        }
        self.base_url = "https://api.notion.com/v1"

    def search_page(self, page_title: str = None):
        url = self.base_url + "/search"

        body = {}
        if page_title is not None:
            body["query"] = page_title

        response = requests.request("POST", url, headers=self.headers, params=body)
        return response

    def append_child_blocks(self, parent_id: str, children: []):
        url = self.base_url + f"/blocks/{parent_id}/children"

        response = requests.request(
            "PATCH",
            url,
            headers=self.headers,
            json={"children": children}
        )

        return response

    def text_append(self, parent_id: str, text: str):
        text_block = {
            "type": "paragraph",
            "paragraph": {
                "text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                    }
                }]
            }
        }

        return self.append_child_blocks(parent_id, [text_block])
class Book:
    def __init__(self, iconUrl, title, author, pageCount, averageRating, ratingsCount):
        self.iconUrl = iconUrl
        self.title = title
        self.author = author
        self.pageCount = pageCount
        self.averageRating = averageRating
        self.ratingsCount = ratingsCount

    def makeBook(self):

        createBook(self.iconUrl, self.title, self.author, self.pageCount, self.averageRating, self.ratingsCount)
# converts google books web links into api links
def parser(url):
    apiUrl = "https://www.googleapis.com/books/v1/volumes/"
    oldString = "books.google"
    newString = "google.com/books"

    if oldString in url:
        url = url.rsplit("id=")[1]
        url = url.rsplit("&")[0]
    elif newString in url:
        url = url.rsplit("/", 1)[1]
        url = url.rsplit("=en",1)[0]

    url = apiUrl + url
    return url
# get books from notion table
def getBooks():
    url = f'https://api.notion.com/v1/databases/{notionID}/query'

    r = requests.post(url, headers={
        "Authorization": f"Bearer {notionToken}",
        "Notion-Version": "2021-08-16"
    })

    result_dict = r.json()
    book_list_result = result_dict['results']

    books = []

    for book in book_list_result:
        book_dict = mapNotionResultToBook(book)
        books.append(book_dict)
    return books
#match notion data with book api data
def mapNotionResultToBook(result):

    book_id = result['id']
    icon = result['icon']['external']['url']
    properties = result['properties']
    title = properties['Title']['title'][0]['text']['content']
    author = properties['Author']['rich_text'][0]['text']['content']
    #description = properties['Description']['rich_text'][0]['text']['content']
    pageCount = properties['pageCount']['number']
    averageRating = properties['averageRating']['number']
    ratingsCount = properties['ratingsCount']['number']
    #small = properties['small']['rich_text'][0]['text']['content']

    return {
        'book_id': book_id,
        'icon': icon,
        'title': title,
        'author': author,
        #'description': description,
        'pageCount': pageCount,
        'averageRating': averageRating,
        'ratingsCount': ratingsCount,

    }
#make a new book
def createBook(icon, title, author, pageCount, averageRating, ratingsCount):
    url = 'https://api.notion.com/v1/pages'

    payload = {
        "parent": {
            "database_id": notionID
        },
        "icon": {
            "external": {
                "url": icon
            }
        },
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Author": {
                "rich_text": [
                    {
                        "text": {
                            "content": author
                        }
                    }
                ]
            },
            "pageCount": {
                            "number": pageCount
            },
            "averageRating": {
                            "number": averageRating
            },
            "ratingsCount": {
                            "number": ratingsCount
            }
        }}

    r = requests.post(url, headers={
        "Authorization": f"Bearer {notionToken}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json"
    }, data=json.dumps(payload))

    book = mapNotionResultToBook(r.json())
    return book
def updateBook(bookID, book):
  url = f'https://api.notion.com/v1/pages/{bookID}'

  payload = {
      "parent": {
          "database_id": notionID
      },
      "cover": {
          "external": {
              "url": book['cover']
          }
      },
      "properties": {
          "Title": {
              "title": [
                  {
                      "text": {
                          "content": book['title']
                      }
                  }
              ]
          },
          "Author": {
              "rich_text": [
                  {
                      "text": {
                          "content": book['author']
                      }
                  }
              ]
          },
          # "Description": {
          #     "rich_text": [
          #         {
          #             "text": {
          #                 "content": description
          #             }
          #         }
          #     ]
          # },
          "pageCount": {
              "number": book['pageCount']
          },
          "averageRating": {
              "number": book['averageRating']
          },
          "ratingsCount": {
              "number": book['ratingsCount']
          }
      }}

  r = requests.patch(url, headers={
    "Authorization": f"Bearer {notionToken}",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json"
  }, data=json.dumps(payload))

  movie = mapNotionResultToBook(r.json())
  return movie

url = input("Input your google books link (use the \"about this book\" section link)\n")

# parser turns it into google books API json style, then requests gets the json info
response = requests.get(parser(url)).json()
bookInfo = response

#making all the book elements from the google books API
titley = str(bookInfo["volumeInfo"]["title"])
authory = str(bookInfo["volumeInfo"]["authors"][0])
descriptiony = str(bookInfo["volumeInfo"]["description"])

try:
    pageCounty = int(bookInfo["volumeInfo"]["pageCount"])
except KeyError:
    pageCounty = 0

try:
    averageRatey = int(bookInfo["volumeInfo"]["averageRating"])
except KeyError:
    averageRatey = 0

try:
    ratingsCounty = int(bookInfo["volumeInfo"]["ratingsCount"])
except KeyError:
    ratingsCounty = 0

try:
    covery = str(bookInfo["volumeInfo"]["imageLinks"]["thumbnail"])
except KeyError:
    covery = "https://st4.depositphotos.com/14953852/22772/v/600/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg"

#this is the part that takes all the elements and actually throws them into a book
createdBook = Book(covery, titley, authory, pageCounty, averageRatey, ratingsCounty)
createdBook.makeBook()

#getting the most recent bookID value from page link in the most hacky way possible (lol). lets me add description after book is added
pageID = json.dumps(getBooks())
pageID = pageID.split(',', 1)
pageID = pageID[0].replace("\"", "")
pageID = pageID.rsplit(": ", 1)[1]

#get rid of HTML characters.
formatList = ['<p>', '<b>', '<br>', '</i>', '<i>', '</p>', '</b>']
for format in formatList:
    descriptiony = descriptiony.replace(format, "")

#adding description — again, very hacky and not clean
nuPage = Notion(notionToken)
nuPage.text_append(pageID, descriptiony)

print("Done! Your book, " + titley + ", has been added to your Notion :)")

#TODO: find a way to be cleaner with creation of google api book elements