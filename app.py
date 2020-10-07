import requests
import pandas as pd
import numpy as np



URL = "https://api.github.com/repos/walmartlabs/thorax/issues"

#sending get request and saving the response as response object
r = requests.get(url = URL)

#extracting data in json format
data = r.json()


import json

# with open('temp.json') as f:
#     data = json.load(f)
datb = pd.DataFrame(data)



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():

    rows = datb.shape[0]
    page_arr = page_num_array(rows)

    titles_df = datb[['title', 'number', 'state']][0:10]
    start_end = [0, 10];
    repo_data = "walmart/thorax"

    return render_template('index.html', titles = titles_df.values, curr_pg = currpage, page_nums = page_arr, repo = repo_data)


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

    titles_df = datb[['title', 'number', 'state']][start_end[0]:start_end[1]]
    repo_data = "walmart/thorax"
    currpage = page_number


    return render_template('index.html', titles = titles_df.values, curr_pg = currpage, page_nums = page_arr, repo = repo_data)


def get_issue(number, datb):
    result_issue = datb.loc[datb['number'] == number]
    if result_issue is None:
        abort(404)
    print("goat here!")
    return result_issue



@app.route('/issue/<int:iss_id>')
def issue(iss_id):


    result_issue = get_issue(iss_id, datb)
    if result_issue is None:
        abort(404)

    col_list = np.array((datb.columns))
    vals = np.array(result_issue)
    vals = vals.transpose()
    vals2 = vals[:,0]

    user_json = result_issue["user"]
    user_json = user_json.values[0]
    user_json
    user_dict = pd.DataFrame.from_dict(user_json, orient="index")
    user_dict.index.name = 'key'
    user_dict.reset_index(inplace=True)
    user_dict_arr = user_dict.values
    result_df = pd.DataFrame({'keys':col_list, 'values':vals2})
    result_df = result_df[result_df['keys'] != "user"]
    issue_title_val = result_df.loc[result_df['keys'] == 'title'].values[0][1]
    issue_status_val = result_df.loc[result_df['keys'] == 'state'].values[0][1]



    return render_template('issue.html', data = result_df.values, issue_num = iss_id,  issue_title = issue_title_val, user = user_dict_arr, status = issue_status_val)



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
