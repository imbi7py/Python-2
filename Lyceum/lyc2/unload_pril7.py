import pypyodbc
import pandas as pd
import datetime
import glob, os
import schedule, time

WORK_DIR = 'D:\Lvov\Python'
PRIL7_SQL = """select q_select FROM SQL_QUERIES where q_name = 'FLK_Pril7'"""
CONN_STR = """Driver={SQL Server Native Client 11.0};
                                Server=dpx\mssqlserver2012;
                                Database=my_base;
                                uid=srz_admin;
                                pwd=srz_admin"""


# Модуль выравнивания столбцов в Excel
def Excel_Column_Autofit(df, worksheet, max_length=None):
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 2  # adding a little extra space
        if max_length:
            max_len = min(max_length, max_len)
        worksheet.set_column(idx, idx, max_len)


#  Проверка необходимости выгрузки Приложения 7
def Check_Flag():
    try:
        conn = pypyodbc.connect(CONN_STR)
        df = pd.read_sql_query("""select Modified_flag 
                                   from ModifiedTables 
                                   where Table_name = '[IESDB].[IES].[R_NSI_USL_V001]'""", conn)
    except Exception as pe:
        print('Ошибка подключения к DBX\MSSQLSERVER2012', pe)
        raise
    flag = df.iloc[0]['modified_flag']
    return flag

def Write_Log(text):
    print(f'{datetime.datetime.now().strftime("%d-%m-%Y %H-%M")} -> {text}')

def Make_Pril7():
    if Check_Flag():  # Есть изменения - нужно обновлять
        Write_Log('Есть признак изменений. Начинаем выгрузку')
        try:  # Берём селект для выгрузки из таблицы
            conn = pypyodbc.connect(CONN_STR)
            sql_text = pd.read_sql_query(PRIL7_SQL, conn).iloc[0]['q_select']
            df = pd.read_sql(sql_text, conn)
            df.columns = map(lambda x: str(x).upper(), df.columns)
        except Exception as pe:
            print("Ошибка выгрузки select q_select FROM SQL_QUERIES where q_name = 'FLK_Pril7'", pe)
            raise

        try:
            # Удаляем предыдущие выгрузки
            for f in glob.glob(f'{WORK_DIR}\Приложение 7*.xlsx'):
                os.remove(f)

            #  Пишем в Excel
            Write_Log('Пишем в Excel')
            Write_Log(f'{WORK_DIR}\Приложение 7 от {datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}.xlsx')
            with pd.ExcelWriter(
                    f'{WORK_DIR}\Приложение 7 от {datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}.xlsx') as writer:
                df.to_excel(writer, sheet_name='Приложение 7', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Приложение 7']
                Excel_Column_Autofit(df, worksheet, 16)
                worksheet.set_column('B:B', 115, None)

                writer.save()
            # Меняем признак необходимсоти выгрузки Flag = 0
            sql_text = "update ModifiedTables set Modified_flag = 0 where Table_name = '[IESDB].[IES].[R_NSI_USL_V001]'"
            cur = conn.cursor()
            cur.execute(sql_text)
            conn.commit()
        except Exception as pe:
            print(pe)


Make_Pril7()
schedule.every().hour.do(Make_Pril7)
while True:
    schedule.run_pending()
    time.sleep(1)

# pyinstaller -F --exclude-module PyQt5 unload_pril7.py
