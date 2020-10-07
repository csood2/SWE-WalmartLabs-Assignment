import requests
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template



URL = "https://api.github.com/repos/walmartlabs/thorax/issues"

#sending get request and saving the response as response object and extracting data
r = requests.get(url = URL)
data = r.json()

#main store of the data from GET request
datb = pd.DataFrame(data)

app = Flask(__name__)


#landing page
@app.route('/')
def index():
    #calculating array of pages to be displayed as pagination
    rows = datb.shape[0]
    page_arr = page_num_array(rows)

    #extracting first 10
    titles_df = datb[['title', 'number', 'state']][0:10]
    repo_data = "walmart/thorax"

    #start at page 1
    currpage = 1

    return render_template('index.html', titles = titles_df.values, curr_pg = currpage, page_nums = page_arr, repo = repo_data)

#once user selects a page, we display those values which correspond to that page
@app.route('/<int:page_number>')
def index_numbered(page_number):

    #calculating array of pages to be displayed as pagination
    rows = datb.shape[0]
    page_arr = page_num_array(rows)

    #using method paginator to get the start and end indices of access to database (datb)
    start_end = paginator(page_number, datb);
    titles_df = datb[['title', 'number', 'state']][start_end[0]:start_end[1]]
    repo_data = "walmart/thorax"
    #pages change as we switch from front end
    currpage = page_number


    return render_template('index.html', titles = titles_df.values, curr_pg = currpage, page_nums = page_arr, repo = repo_data)


#returns a dataframe containing all the information about the issue# specified in number (from datb)
def get_issue(number, datb):
    result_issue = datb.loc[datb['number'] == number]
    if result_issue is None:
        abort(404)
    return result_issue



@app.route('/issue/<int:iss_id>')
def issue(iss_id):


    result_issue = get_issue(iss_id, datb)
    if result_issue is None:
        abort(404)

    #creating dataframe which contains the label and description of
    #information about the issues as 2 separate columns
    col_list = np.array((datb.columns))
    vals = np.array(result_issue)
    vals = vals.transpose()
    vals2 = vals[:,0]
    result_df = pd.DataFrame({'keys':col_list, 'values':vals2})
    result_df = result_df[result_df['keys'] != "user"]
    result_df_arr = result_df.values

    #creating dataframe which contains the label and description of
    #information about the user as 2 separate columns
    user_json = result_issue["user"]
    user_json = user_json.values[0]
    user_dict = pd.DataFrame.from_dict(user_json, orient="index")
    user_dict.index.name = 'key'
    user_dict.reset_index(inplace=True)
    user_dict_arr = user_dict.values

    #accessing values of issue required for heading
    issue_title_val = result_df.loc[result_df['keys'] == 'title'].values[0][1]
    issue_status_val = result_df.loc[result_df['keys'] == 'state'].values[0][1]



    return render_template('issue.html', data = result_df_arr, issue_num = iss_id,  issue_title = issue_title_val, user = user_dict_arr, status = issue_status_val)


#returns array of page numbers based on 10 issues per page.
def page_num_array(count_rows):
    num_pages = (count_rows//10)
    num_left = count_rows%10
    if (num_left > 0):
        num_pages+=1

    if (num_pages == 0):
        num_pages = 1
    arr = list(range(1,num_pages+1))
    return arr

#returns array of start and end indices for the index functions.
#Uses the page number to calculate appropriate indices to slice the database
def paginator(page_num, db):
    rows = db.shape[0]
    num_pages = rows//10
    num_lastpg = rows%10

    start_index = (page_num-1)*10;
    end_index = start_index + 10
    arr_result = [start_index, end_index]

    return arr_result
