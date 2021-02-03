from rest_framework.response import Response
from rest_framework.views import APIView

import sqlite3
import json

class Question(APIView):
    def post(self, request):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = (
            "select poll_id from 'polls_polls' where poll_id = {0}"
        ).format(request.data.get("poll_id"))
        cursor.execute(sql)
        rows = cursor.fetchone()
        if rows is not None:
            questions = request.data.get("questions")
            if len(questions) != 0:
                for i, row in enumerate(questions):
                    sql = (
                        'insert into polls_questions'
                        '(question_title, question_choices, poll_id, question_type)'
                        'values("{0}", "{1}", {2}, {3})'
                    ).format(
                        row['title'],
                        row['choices'],
                        request.data.get("poll_id"),
                        row['type'],
                    )
                    cursor.execute(sql)
                    conn.commit()
            else:
                return Response({
                    "status": False,
                    "desc": 'Questions adding failed - no Questions'
                })
            return Response(
                {"success": 'Questions to poll #{0} created successfully'.format(
                    request.data.get("poll_id")
                )}
            )
        else:
            return Response({
                "status": False,
                "desc": 'Questions adding failed - this poll doesnt exist'
            })

    def put(self, request):
        question = request.data.get("question")
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            update polls_questions 
            set question_title = '{0}', question_choices = '{1}', 
            poll_id = {2}, question_type = {3}
            WHERE question_id = {4}
        """.format(
            question['title'],
            question['choices'],
            question['poll_id'],
            question['type'],
            question['id'],
        )
        cursor.execute(sql)
        conn.commit()
        return Response(
            {"success": 'Question {0} edited successfully'.format(question['title'])}
        )

    def delete(self, request):
        question = request.data.get("question")
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            delete from polls_questions 
            where question_id = {0} and
            poll_id = {1}
        """.format(
            question['id'],
            question['poll_id']
        )
        cursor.execute(sql)
        conn.commit()
        return Response({
                "status": True,
                "desc": 'Question {0} deleted successfully'.format(
                    question['id']
                )
            })