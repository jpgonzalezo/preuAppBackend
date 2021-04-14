import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.writer.excel import save_virtual_workbook
from flask import send_file, Response


def sheet_Tupla(path):
    wb_obj = openpyxl.load_workbook(path)
    sheet = wb_obj.active
    result_list = []
    for value in sheet.iter_rows(values_only=True):
        result_list.append(value)
    result_list.pop(0)
    return result_list

def create_workbook(path,validate_dict, max_rows):
    keys = validate_dict.keys()
    wb = Workbook()
    ws = wb.active
    for element in keys:
        data_val = DataValidation(type="list",formula1=validate_dict[element]) #You can change =$A:$A with a smaller range like =A1:A9
        ws.add_data_validation(data_val)
        for num in range(1, max_rows +1):
            data_val.add(ws[element + str(num)]) #If you go to the cell B1 you will find a drop down list with all the values from the column A
    return Response(
        save_virtual_workbook(wb),
        headers={
            'Content-Disposition': 'attachment; filename=sheet.xlsx',
            'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    )

#print (create_workbook({'A': '"Dog,Cat,Bat"', 'C': '"wea1, wea2, wea3"'}))


