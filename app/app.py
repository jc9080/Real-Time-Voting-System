from flask import Flask, render_template, request, session, url_for, redirect
from kafka import KafkaConsumer

import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

PRES_A_CNT = 0
PRES_B_CNT = 0
PRES_C_CNT = 0
PRES_D_CNT = 0

VP_A_CNT = 0
VP_B_CNT = 0
VP_C_CNT = 0
VP_D_CNT = 0

@app.route('/view')
def draw_vote():
    topic_name = 'aggregate-votes'
    consumer = KafkaConsumer(topic_name, bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='latest', group_id='group1',
                            enable_auto_commit=True, consumer_timeout_ms=500)
    for msg in consumer:
        global PRES_A_CNT
        global PRES_B_CNT
        global PRES_C_CNT
        global PRES_D_CNT

        global VP_A_CNT
        global VP_B_CNT
        global VP_C_CNT
        global VP_D_CNT

        dmsg = json.loads(msg.value)
        print('draw_vote(): New aggregated votes read: %s' % dmsg)
        if 'pa' in dmsg:
            PRES_A_CNT += dmsg['pa']
        elif 'pb' in dmsg:
            PRES_B_CNT += dmsg['pb']
        elif 'pc' in dmsg:
            PRES_C_CNT += dmsg['pc']
        elif 'pd' in dmsg:
            PRES_D_CNT += dmsg['pd']

        if 'vpa' in dmsg:
            VP_A_CNT += dmsg['vpa']
        elif 'vpb' in dmsg:
            VP_B_CNT += dmsg['vpb']
        elif 'vpc' in dmsg:
            VP_C_CNT += dmsg['vpc']
        elif 'vpd' in dmsg:
            VP_D_CNT += dmsg['vpd']

    consumer.close()

    return render_template('vote-result.html', pa=PRES_A_CNT, pb=PRES_B_CNT, pc=PRES_C_CNT, pd=PRES_D_CNT,\
                                                vpa=VP_A_CNT, vpb=VP_B_CNT, vpc=VP_C_CNT, vpd=VP_D_CNT)

if __name__ == "__main__":
    app.run('127.0.0.1', 8888, debug = True)