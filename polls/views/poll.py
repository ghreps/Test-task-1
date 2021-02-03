from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Polls
from ..serializers import PollsSerializer
import json

import sqlite3
import time

class PollResults(APIView):
    def get(self, request):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = 'select * from "polls_usersanswers" where user_id = {0}'.format(
            request.query_params['user_id']
        )
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        results = []
        for i, row in enumerate(rows):
            print(row)
            stri = row[1]
            results.append({
                'id': row[0],
                'poll_id': row[3],
                'timestamp': row[4],
                'answers': json.loads(stri.replace('\'','"'))
            })
        answer = {
            'user_id': request.query_params['user_id'],
            'answers': results
        }
        return Response(answer)

class PollCommit(APIView):
    def post(self, request):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            insert into polls_usersanswers
            (user_answer, user_id, poll_id, timestamp) 
            values 
            ("{0}", {1}, {2}, {3})
        """.format(
            request.data.get("answers"),
            request.data.get("user_id"),
            request.data.get("poll_id"),
            int(time.time())
        )
        cursor.execute(sql)
        conn.commit()
        return Response({
            "status": True,
            "desc": 'Poll {0} filled successfully'.format(
                request.data.get("poll_id")
                )
        })

class PollsList(APIView):
    def get(self, request):
        # timestamp = int(time.time())
        # polls = Polls.objects.filter(poll_start = timestamp, poll_end = timestamp)
        # serializer = PollsSerializer(polls, many=True)
        # return Response({"polls": polls})
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        if request.query_params['user_id']:
            sql = 'insert or replace into polls_users(user_id) values ({0})'.format(
                request.query_params['user_id']
            )
            cursor.execute(sql)
            conn.commit()
        sql = """
            select poll_id, poll_title, poll_description, poll_start, poll_end 
            from 'polls_polls' where strftime('%s','now') between poll_start and poll_end;
        """
        rows = cursor.execute(sql)
        answer = []
        for i, row in enumerate(rows):
            answer.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'start': row[3],
                'end': row[4]
            })
        return Response({"polls": answer})

class Poll(APIView):
    def get(self, request):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            select a.poll_title, a.poll_description, 
            b.question_id, b.question_type, b.question_title, b.question_choices
            from polls_polls a
            left join polls_questions b on a.poll_id = b.poll_id
            where a.poll_id = {0}
        """.format(request.query_params['id'])
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) != 0:
            title, desc, answer = '', '', []
            for i, row in enumerate(rows):
                title = row[0]
                desc = row[1]
                stri = row[5]
                answer.append({
                    'id': row[2],
                    'type': row[3],
                    'title': row[4],
                    'choices': json.loads(stri.replace('\'','"'))
                })
            return Response({
                'id': request.query_params['id'],
                'title': title,
                'description': desc,
                'questions': answer
            })
        else:
            return Response({
                "status": False,
                "desc": 'Poll id {0} doesnt exists'.format(
                    request.query_params['id']
                )
            })

    def post(self, request):
        poll = request.data.get("poll")
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            insert into "polls_polls"
            ("poll_title", "poll_start", "poll_end", "poll_description", "user_id")
            values ('{0}', {1}, {2}, '{3}', {4})
        """.format(
            poll['title'],
            poll['start'],
            poll['end'],
            poll['description'],
            poll['user_id']
        )
        cursor.execute(sql)
        conn.commit()
        return Response({
            "status": True,
            "desc": 'Poll {0} created successfully'.format(poll['title'])
        })

    def put(self, request):
        poll = request.data.get("poll")
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            select poll_id, poll_title, poll_description, poll_start, poll_end, user_id
            from 'polls_polls' where poll_id = {0}
        """.format(poll['id'])
        cursor.execute(sql)
        rows = cursor.fetchone()
        if rows is not None:
            if poll['user_id'] != rows[5]:
                return Response({
                    "status": False,
                    "desc": 'Poll edit failed - you can edit only your own polls'
                })
            sql = """
                update polls_polls 
                set poll_title = '{0}', poll_end = {1}, poll_description = '{2}'
                WHERE rowid = {3}
            """.format(
                poll['title'],
                poll['end'],
                poll['description'],
                poll['id']
            )
            cursor.execute(sql)
            conn.commit()
            return Response({
                "status": True,
                "desc": 'Poll {0} edited successfully'.format(poll['title'])
            })
        else:
            return Response({
                "status": False,
                "desc": 'Poll edit failed - this poll doesnt exist'
            })
    
    def delete(self, request):
        poll = request.data.get("poll")
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = """
            select poll_id, poll_title, poll_description, poll_start, poll_end, user_id
            from 'polls_polls' where poll_id = {0}
        """.format(poll['id'])
        cursor.execute(sql)
        rows = cursor.fetchone()
        if rows is not None:
            if poll['user_id'] != rows[5]:
                return Response({
                    "status": False,
                    "desc": 'Poll delete failed - you can delete only your own polls'
                })
            sql = 'delete from polls_usersanswers where poll_id = {0}'.format(poll['id'])
            cursor.execute(sql)
            conn.commit()
            sql = 'delete from polls_questions where poll_id = {0}'.format(poll['id'])
            cursor.execute(sql)
            conn.commit()
            sql = 'delete from polls_polls where poll_id = {0}'.format(poll['id'])
            cursor.execute(sql)
            conn.commit()
            return Response({
                "status": True,
                "desc": 'Poll id {0} deleted successfully'.format(poll['id'])
            })
        else:
            return Response({
                "status": False,
                "desc": 'Poll delete failed - this poll doesnt exist'
            })