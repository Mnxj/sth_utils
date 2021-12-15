import psycopg2

conn = psycopg2.connect(database="sonar", user="postgres",
                        password="123", host="127.0.0.1", port="5432")

cursor = conn.cursor()
sqlMetrics = "select uuid from metrics limit 1 offset "

sqlTemplate = "select projdesc.component_uuid,\np.name,"
sumTemplate1 = "sum(case when projdesc.metric_uuid = {UUID} then projdesc.value else 0 end)"
sumTemplate2 = "sum(case when projdesc.metric_uuid = {UUID} then projdesc.variation_value_1 else 0 end)"
name = ["bugs", "漏洞", "异味", "测试覆盖率", "重复率", "新bugs", "新漏洞", "新异味"]

for index, num in enumerate([74, 76, 72, 33, 52, 75, 77, 73]):
    cursor.execute(sqlMetrics + str(num - 1))
    rows = cursor.fetchall()
    if index > 3:
        sqlTemplate += sumTemplate2.replace("{UUID}", "'" + str(rows[0][0]) + "'")
    else:
        sqlTemplate += sumTemplate1.replace("{UUID}", "'" + str(rows[0][0]) + "'")
    sqlTemplate += "  " + name[index] + ",\n"

sqlTemplate += """
p.kee
from
project_measures projdesc, projects p
where
projdesc.component_uuid=p.uuid
group by projdesc.component_uuid, p.name, p.kee ;"""
print(sqlTemplate)
cursor.close()
conn.close()
