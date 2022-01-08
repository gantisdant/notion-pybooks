# notion-pybooks
This is a pretty simple python script that allows you to add a book to a notion database simply by entering the Google Books link.

Using the official Notion API and the official Google Books API, this script will prompt you to enter a Google Books URL (something like **this** for the new version of Google Books: https://www.google.com/books/edition/Learn_Python_Visually/eggOEAAAQBAJ?hl=en&gbpv=0 or like **this** for the old Google Books: https://books.google.com/books?id=eggOEAAAQBAJ&newbks=1&newbks_redir=0&dq=learn+python&source=gbs_navlinks_s). 

The program is in very early stages, but I'm hoping to continue adding to it. 

## Getting Started
1. Download the project. 
2. Open up the **main.py** script in your text editor/Python IDE. You'll see at the top that there are two blank variables, one called **notionID** and one called **notionToken**. In order for this script to access your Notion, you'll need to create an _Integration Token_ on Notion's website, which can be done here: https://www.notion.so/help/create-integrations-with-the-notion-api. Once you've got that token, put that inside the quotation marks for the **notionToken** value. 
3. For the **notionID** value, go to the database page in Notion that you want to use with this program, and choose "copy link" from the top right menu in Notion. From there, you'll get a link that looks like this: https://www.notion.so/fakeUser/**fe82bcab32494Wfcba497aa5fe3a79c898**?v=db0418861829464eewf6f3d2f7ef08f199. The bolded section is what you'll use for the **notionID** value (the part after your Notion username and before the question mark). Copy that and set it as the notionID variable. 
4. Lastly, make sure the page that you plan to use with the script is formatted as a **database**. In order for it to work (as-is, hoping to add more flexibility later), **you need to have the 5 following columns in your database:** **Title, Author (as text property), pageCount, averageRating, and ratingsCount (all formatted as number property).** Make sure you have these exact names—if you don't care about one or the other values, you can hide the column. You can also add as many additional columns as you want—formulas to show how long it might take you to read based on page-length, etc. Additional columns won't mess up the program. 
5. From there, the script should run! I then proceeded to make a .zsh script so that I can run this program simply by calling "pybook" in terminal, which makes it a lot more handy. 
