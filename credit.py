#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
from lxml import etree

filename = '浙江大学现代教务管理系统.html'
tree = etree.parse(filename, parser=etree.HTMLParser(encoding='gbk'))

table = tree.xpath('//*[@id="DataGrid1"]//tr')

titles = []
tds = table[0].xpath('./td')
for i in range(len(tds)):
    titles.append(tds[i].text)

other_score_format = {
    '优秀':(100+85)/2, '良好':(84+75)/2, '中等':(74+65)/2, '及格':(64+60)/2,
    'A+':(100+95)/2, 'A':94*2/3+85/3, 'A-':94/3+85*2/3,
    'B+':84*0.75+75*0.25, 'B':84*0.5+75*0.5, 'B-':84*0.25+75*0.75,
    'C+':74*0.75+65*0.25, 'C':74*0.5+65*0.5, 'C-':74*0.25+65*0.75,
    'D':(64+60)/2,
    '合格': (100+60)/2
    }

allCourses = []
for i in range(1,len(table)):
    text_elements = table[i].xpath('./td')
    data = {}
    for it, title in enumerate(titles):
        try:
            data[title] = float(text_elements[it].text)
        except ValueError:
            if text_elements[it].text == '\xa0':
                data[title] = None
            elif text_elements[it].text in other_score_format:
                data[title] = other_score_format[text_elements[it].text]
            else:
                data[title] = text_elements[it].text
        allCourses.append(data)

None_Major_id = [
    '(2017-2018-1)-061K0150-0004166-1',
    '(2017-2018-1)-181H0010-0084361-1',
    '(2017-2018-2)-041S0300-0009067-1',
    '(2018-2019-2)-061K0030-0095446-1',
    '(2018-2019-2)-7216N001-0095479-1',
    '(2019-2020-1)-041J0060-0099092-1',
    '(2020-2021-1)-011A0011-0087018-1',
    '(2020-2021-1)-011A0041-0094351-1',
    '(2020-2021-1)-2114N002-0088262-1'
    ]

def calc_score(courses):
    score_4 = []
    score_5 = []
    score_100 = []
    credit = []
    
    for course in courses:
        if course['绩点'] > 4:
            score_4.append(4)
        else:
            score_4.append(course['绩点'])
        score_5.append(course['绩点'])
        score_100.append(course['成绩'])
        credit.append(course['学分'])

    sum_score_4 = [ score*credit[i] for i, score in enumerate(score_4) ]
    sum_score_5 = [ score*credit[i] for i, score in enumerate(score_5) ]
    sum_score_100 = [ score*credit[i] for i, score in enumerate(score_100) ]
    sum_credit = credit
    return sum_score_4, sum_score_5, sum_score_100, sum_credit

score_4, score_5, score_100, credit = calc_score(allCourses)
major_courses = [course for course in allCourses if not course['选课课号'] in None_Major_id]
major_score_4, major_score_5, major_score_100, major_credit = calc_score(major_courses)

print('四分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(major_score_4), sum(major_credit), sum(major_score_4)/sum(major_credit)))
print('五分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(major_score_5), sum(major_credit), sum(major_score_5)/sum(major_credit)))
print('百分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(major_score_100), sum(major_credit), sum(major_score_100)/sum(major_credit)))

print('总-四分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(score_4), sum(credit), sum(score_4)/sum(credit)))
print('总-五分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(score_5), sum(credit), sum(score_5)/sum(credit)))
print('总-百分制\t= {:.2f}/{:.2f} = {:.2f}'
      .format(sum(score_100), sum(credit), sum(score_100)/sum(credit)))

with open('成绩.txt', 'w', encoding='utf-8') as file:
    file.write('四分制\t= {:.2f}/{:.2f} = {:.2f}\n'
      .format(sum(major_score_4), sum(major_credit), sum(major_score_4)/sum(major_credit)))
    file.write('五分制\t= {:.2f}/{:.2f} = {:.2f}\n'
          .format(sum(major_score_5), sum(major_credit), sum(major_score_5)/sum(major_credit)))
    file.write('百分制\t= {:.2f}/{:.2f} = {:.2f}\n'
          .format(sum(major_score_100), sum(major_credit), sum(major_score_100)/sum(major_credit)))
    file.write('\n')
    file.write('总-四分制\t= {:.2f}/{:.2f} = {:.2f}\n'
          .format(sum(score_4), sum(credit), sum(score_4)/sum(credit)))
    file.write('总-五分制\t= {:.2f}/{:.2f} = {:.2f}\n'
          .format(sum(score_5), sum(credit), sum(score_5)/sum(credit)))
    file.write('总-百分制\t= {:.2f}/{:.2f} = {:.2f}\n'
          .format(sum(score_100), sum(credit), sum(score_100)/sum(credit)))
