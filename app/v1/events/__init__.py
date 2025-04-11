
import atexit
import pymysql
import asyncio
from google.protobuf.message import Message
from fastapi import APIRouter, Response
from app.pbf import Event_pb2
from app.config import MYSQL_HOST, MYSQL_AUTH, MYSQL_PORT

mysql_user, mysql_pass = MYSQL_AUTH.split(':')

db = pymysql.connect(
    host=MYSQL_HOST, user=mysql_user, password=mysql_pass,
    port=MYSQL_PORT, database="kxpage"
)

event_router = APIRouter(
    prefix="/api/events",
    tags=["events"]
)

@event_router.get("/")
async def get_events():

    def execute():
        cursor = db.cursor()
        cursor.execute(
"""SELECT a.uuid, a.ev_time, a.ev_title, a.ev_href, a.ev_desc, a.image_hash
FROM events a ORDER BY ev_time DESC;
""")    
        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    result = await asyncio.to_thread(execute)

    ev_list: Message = Event_pb2.EventList()
    for record in result:
        uuid, dtime, title, href, desc, img_hash = record
        event = ev_list.events.add()
        event.eventUUID = uuid
        event.eventTitle = title
        event.eventDescription = desc
        event.eventHref = href
        event.eventTime = dtime.strftime("%Y/%m/%d")
        if img_hash: event.imageHash = img_hash

    data = ev_list.SerializeToString()

    return Response(
        content=data,
        status_code=200,
        headers={
            'X-Requested-With': 'XMLHttpRequest'
        },
        media_type="application/octet-stream"
    )

def _end_of_life() -> None:
    db.close()

atexit.register(_end_of_life)
