import apiclient
import gspread
import vertica_python
import pymysql
import schedule
import pandas
import time
import httplib2
from threading import Thread
import os
from oauth2client.service_account import ServiceAccountCredentials
from database import db_session
from models import User, Job
from sqlalchemy import create_engine

SERVICE_CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),'config/')
GOOGLE_CREDENTIALS = os.path.join(SERVICE_CONFIG_PATH, "automate-9c1bd94a604e.json")


'''
QUERY FUNCTIONS

'''

def query_mysql(query, host, username, password, port=3306, db="testdb"):
    engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{db}".format(user=username, 
        password=password, host=host, db=db))
    results = pandas.read_sql_query(query, engine)
    print results
    return results

#def query_vertica(query, host, port, username, password, db):

#def query_presto(query, host, port, username, password, db):

'''
GOOGLE SPREADSHEET WRITE FUNCTIONS
db-writer@automate-160703.iam.gserviceaccount.com
'''


def write_gspread(df, workbook_name, worksheet_name, replace_sheet=True, resize_sheet=True, convert_unicode=True, ignore_worksheet_case=True):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS, scope)

    print df

    gd_connection = gspread.authorize(credentials)
    gd_workbook = gd_connection.open(workbook_name)

    row_count = df.shape[0] + 1
    col_count = df.shape[1]

    #if convert_unicode:
    #    df = decode_string_columns(df)

    gd_worksheet = None

    for worksheet in gd_workbook.worksheets():
        is_same_sheet = False
        if ignore_worksheet_case:
            is_same_sheet = (worksheet.title.lower() == worksheet_name.lower())
        else:
            is_same_sheet = (worksheet.title == worksheet_name)

        if is_same_sheet:
            if replace_sheet:
                gd_worksheet = worksheet
                if resize_sheet:
                    gd_worksheet.resize(rows=row_count, cols=col_count)
            else:
                gd_workbook.del_worksheet(worksheet)

    if gd_worksheet is None:
        gd_worksheet = gd_workbook.add_worksheet(title=worksheet_name, rows=row_count, cols=col_count)

    cell_list = gd_worksheet.range('A1:{}'.format(gd_worksheet.get_addr_int(1, col_count)))
    for cell in cell_list:
        cell.value = df.iloc[cell.row -2, cell.col -1]

    gd_worksheet.update_cells(cell_list)

    cell_list = gd_worksheet.range('A2:{}'.format(gd_worksheet.get_addr_int(row_count, col_count)))
    for cell in cell_list:
        cell.value = df.iloc[cell.row -2, cell.col -1]

    gd_worksheet.update_cells(cell_list)


'''
SCHEDULING FUNCTIONS

'''

def run(job_id, db_session):
    print "Running", str(job_id)
    job = db_session.query(Job).filter_by(id=job_id).first()
    query_results = query_mysql(job.query, job.host, job.db_user, job.db_pass)#, job.port)
    push_results = write_gspread(query_results, job.spreadsheet, job.sheet)

def load_jobs(db_session, Job):
    jobs = db_session.query(Job).all()
    for job in jobs:
        print "Adding to scheduler: ", job.title
        schedule.every(int(job.schedule)).minutes.do(run, job.id, db_session)

def scheduler():  
    print "initiated" 
    load_jobs(db_session, Job)
    t = Thread(target=runner)
    t.start()


def runner():
    while True:
        schedule.run_pending()
        time.sleep(1)
