from bs4 import BeautifulSoup
import requests
import xlsxwriter
import lxml.html.clean
import re
import matplotlib.pyplot as plt


def codeconv(string_ip):
    updated_string_list = []
    decipher = lxml.html.clean.clean_html(string_ip)
    clean_code = re.compile('<.*?>')
    final_result = re.sub(clean_code, '', decipher)
    updated_string_list.append(final_result)
    return final_result


def typeconv(no_input):
    change = int(no_input)
    return change


# Create empty lists for storing News titles, Views and upload date
all_titles = []
upload_time_list = []
no_of_views_list = []

# Collect data from autocar website
for pg_no in range(1, 92):
    pg_url = "https://www.autocarindia.com/car-news/" + str(pg_no)
    response = requests.get(pg_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Collect titles
    if pg_no == 1:
        data_array = soup.find_all(class_="img")
    else:
        data_array = soup.find_all(class_="img col-sm-4 no-padding")
    for title_list in range(0, len(data_array)):
        title_path_1 = data_array[title_list].a.find("img", alt=True)
        all_titles.append(title_path_1['alt'])

    # Collect upload dates
    tym_upload = soup.find_all(class_="body")
    for time_list in range(0, len(data_array)):
        upload_time_list.append(tym_upload[time_list].time.text)

    # Collect number of views
    no_of_views = soup.find_all(class_="footer row")
    for views in range(0, len(no_of_views)):
        no_of_views_list.append(no_of_views[views].ul.li.text)


print(all_titles)
print(upload_time_list)
print(no_of_views_list)

new_titles = []
for x in all_titles:
    if '&#' in x:
        rem_chars = codeconv(x)
        print(rem_chars)
        new_titles.append(rem_chars)
    else:
        new_titles.append(x)

print('/' * 100)
print(new_titles)

new_views = []
for lml in no_of_views_list:
    divide = lml.split()
    if ',' in lml:
        remove_comma = divide[0].replace(',', '')
        change_type = typeconv(remove_comma)
        new_views.append(change_type)

    else:
        change_type = typeconv(lml)
        new_views.append(change_type)

print(new_views)


# Create an excel file
excel_sheet = xlsxwriter.Workbook('D:/Autocar Internship/Crash_test_10.xlsx')

# Create a sheet within the excel
worksheet_1 = excel_sheet.add_worksheet("All_news_data")
worksheet_2 = excel_sheet.add_worksheet("Car_launch_news")

# write data in the excel sheet
col_name_1 = 'A'
col_name_2 = 'B'
col_name_3 = 'C'
count_1 = 1
count_2 = 1
count_3 = 1
count_4 = 1
count_5 = 1
count_6 = 1

# write column names in all news section
worksheet_1.write("A1", "Car News")
worksheet_1.write("B1", "Views")
worksheet_1.write("C1", "Date Upload")

# Write column names in launch news section
worksheet_2.write("A1", "Crash Test News")
worksheet_2.write("B1", "views")
worksheet_2.write("C1", "Date upload")

# Write title names
for title_write in new_titles:
    count_1 = count_1 + 1
    worksheet_1.write(col_name_1 + str(count_1), title_write)

# Write number of views
for views_write in new_views:
    count_2 = count_2 + 1
    worksheet_1.write(col_name_2 + str(count_2), views_write)

# write date of upload
for dates_write in upload_time_list:
    count_3 = count_3 + 1
    worksheet_1.write(col_name_3 + str(count_3), dates_write)

excel_sheet.close()

# plt.scatter(list(range(0, len(new_views))), new_views)
# plt.grid(linestyle='--')
# plt.rcParams['axes.axisbelow'] = True
# plt.show()

