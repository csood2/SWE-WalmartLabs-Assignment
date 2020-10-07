import requests
import pandas as pd



# URL = "https://api.github.com/repos/walmartlabs/thorax/issues"
#
# #sending get request and saving the response as response object
# r = requests.get(url = URL)
#
# #extracting data in json format
# data = r.json()


import json

with open('temp.json') as f:
    data = json.load(f)
datb = pd.DataFrame(data)



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    page = 1
    # URL = "https://api.github.com/repos/walmartlabs/thorax/issues"
    #
    # # sending get request and saving the response as response object
    # r = requests.get(url = URL)
    #
    # # extracting data in json format
    # data = r.json()

    #db = pd.DataFrame(data)

    #mainpage = df[['title', 'number', 'state']]

#conn = get_db_connection()
#    //posts = conn.execute('SELECT * FROM posts').fetchall()
#    //conn.close()


    rows = datb.shape[0]
    page_arr = page_num_array(rows)

    titles_df = datb[['title', 'number', 'state']][0:10]
    start_end = [0, 10];

    return render_template('index.html', titles = titles_df.values, page_nums = page_arr)


@app.route('/<int:page_number>')
def index_numbered(page_number):
    # URL = "https://api.github.com/repos/walmartlabs/thorax/issues"
    #
    # # sending get request and saving the response as response object
    # r = requests.get(url = URL)
    #
    # # extracting data in json format
    # data = r.json()

    #db = pd.DataFrame(data)

    rows = datb.shape[0]
    page_arr = page_num_array(rows)

    start_end = paginator(page_number, datb);

    titles_df = datb[['title', 'number', 'state']]
    titles_df = datb[['title', 'number', 'state']][start_end[0]:start_end[1]]

    return render_template('index.html', titles = titles_df.values, page_nums = page_arr)


#, numbers = db["number"]


def get_issue(number, datb):
    result_issue = datb.loc[datb['number'] == number]
    if result_issue is None:
        abort(404)
    print("goat here!")
    return result_issue



@app.route('/issue/<int:iss_id>')
def issue(iss_id):

    print("got here!")

    result_issue = get_issue(iss_id, datb)
    if result_issue is None:
        abort(404)

    print("values:")
    print(result_issue.values)
    return render_template('issue.html', issue=result_issue.values)



def page_num_array(count_rows):
    num_pages = (count_rows//10)
    num_left = count_rows%10
    if (num_left > 0):
        num_pages+=1

    if (num_pages == 0):
        num_pages = 1
    arr = list(range(1,num_pages+1))
    return arr


def paginator(page_num, db):
    rows = db.shape[0]
    num_pages = rows//10
    num_lastpg = rows%10

    start_index = (page_num-1)*10;
    end_index = start_index + 10
    arr_result = [start_index, end_index]

    return arr_result
