import xlwings as xw
import requests

def book_trade_from_excel():
    wb = xw.Book.caller()  # Connect to the Excel workbook that called this function
    sheet = wb.sheets['Dashboard']  # the sheet which we're reading from

    trade_data = {
        "isin": sheet.range("B2").value,
        "ticker": sheet.range("B3").value,
        "face_value": sheet.range("B4").value,
        "clean_price": sheet.range("B5").value
    }

    # Send the trade data to our API
    api_url = "http://localhost:8000/portfolio/trade"
    response = requests.post(api_url, json=trade_data)
    if response.status_code == 200:
        sheet.range("B7").value = "Trade booked successfully!"
        wb.api.RefreshAll()
    else:
        sheet.range("B7").value = f"❌ Failed to book trade: {response.text}"
