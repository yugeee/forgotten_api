import pdfkit
from jinja2 import Template, Environment, FileSystemLoader

#  勤怠をPDFに
def write_attendance_pdf(user, year, month, attendances, work_time_total):
    env = Environment(loader=FileSystemLoader('./'))
    tpl = env.get_template('pdf/attendance.html')

    
    html = tpl.render({'user':user, 'year':year, 'month':month, 'attendances':attendances, 'work_time_total':work_time_total})
    
    out_path = ('./out/%s_attendance_report.pdf' % user['id'])

    pdfkit.from_string(str(html), out_path)

    return out_path


#  運賃をPDFに
def write_fare_pdf(user, year, month, fares, fare_total):
    env = Environment(loader=FileSystemLoader('./'))
    tpl = env.get_template('pdf/fare.html')

    
    html = tpl.render({'user':user, 'year':year, 'month':month, 'fares':fares, 'fare_total':fare_total})
    
    out_path = ('./out/%s_fare_report.pdf' % user['id'])

    pdfkit.from_string(str(html), out_path)

    return out_path