import xlwings as xw
import requests

def book_trade_from_excel():
    wb = xw.Book.caller()  # Connect to the Excel workbook that called this function
    sheet = wb.sheets['Dashboard']  # the sheet which we're reading from

    

