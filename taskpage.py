import mysql
from flask import render_template, request, redirect
import siteInfo

dbconfig = {"host": siteInfo.databasehost(),
            "user": siteInfo.databaseuser(),
            "password": siteInfo.databasepassword(),
            "database": siteInfo.database(), }

def getData(table):
    database = mysql.connector.connect(**dbconfig)
    cursor = database.cursor(dictionary=True)
    cursor.execute("select * from " + table)
    req = cursor.fetchall()
    cursor.close()
    database.close()
    return req

def updateData(table, status, id):
    database = mysql.connector.connect(**dbconfig)
    sql = "UPDATE " + table + " SET status = " + str(status) + " WHERE id = " + str(id)

    cursor = database.cursor()
    cursor.execute(sql)

    database.commit()
    cursor.close()
    database.close()


def task_page(webpage):
    teamClaim = request.args.get("claim", '')
    taskID = request.args.get("id", '')

    codeTasks = []
    codeDB = getData("codeTasks")

    mechanicalTasks = []
    mechanicalDB = getData("mechanicalTasks")

    electricalTasks = []
    electricalDB = getData("electricalTasks")

    businessTasks = []
    businessDB = getData("businessTasks")

    for task in codeDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            codeTasks.append({"id": task["id"], "task": task["task"], "color": color, "claimText": claimText,
                              "status": task["status"]})

    for task in mechanicalDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            mechanicalTasks.append({"id": task["id"], "task": task["task"], "color": color, "claimText": claimText,
                                    "status": task["status"]})

    for task in electricalDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            electricalTasks.append({"id": task["id"], "task": task["task"], "color": color, "claimText": claimText,
                                    "status": task["status"]})

    for task in businessDB:
        if not task["status"] == 3:
            switcher = {
                1: "Tomato",
                0: "Orange",
                2: "MediumSeaGreen",
            }
            switcher2 = {
                1: "Claim Task",
                0: "Finish Task",
                2: "Remove Task",
            }

            color = switcher.get(task["status"], "")
            claimText = switcher2.get(task["status"], "")
            businessTasks.append({"id": task["id"], "task": task["task"], "color": color, "claimText": claimText,
                                  "status": task["status"]})

    if teamClaim == "code":
        for task in codeTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("codeTasks", newStatus, task["id"])
        return redirect('/Tasks#code')
    elif teamClaim == "mechanical":
        for task in mechanicalTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("mechanicalTasks", newStatus, task["id"])
        return redirect('/Tasks#mechanical')
    elif teamClaim == "electrical":
        for task in electricalTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("electricalTasks", newStatus, task["id"])
        return redirect('/Tasks#electrical')
    elif teamClaim == "business":
        for task in businessTasks:
            if task["id"] == int(taskID):
                switcher = {
                    1: 0,
                    0: 2,
                    2: 3,
                }
                newStatus = switcher.get(task["status"], "")
                updateData("businessTasks", newStatus, task["id"])
        return redirect('/Tasks#business')
    else:
        return render_template(webpage,
                               codeTasks=sorted(codeTasks, key=lambda x: x["status"]),
                               mechanicalTasks=sorted(mechanicalTasks, key=lambda x: x["status"]),
                               electricalTasks=sorted(electricalTasks, key=lambda x: x["status"]),
                               businessTasks=sorted(businessTasks, key=lambda x: x["status"]),
                               the_title="PV Robotics Tasks")  # Hello