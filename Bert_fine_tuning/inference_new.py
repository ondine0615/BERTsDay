# -*- coding: utf-8 -*-

# 필요한 모듈 불러오기

import argparse
import os
import pickle
import tensorflow as tf
import numpy as np

from to_array.bert_to_array import BERTToArray
from models.bert_slot_model import BertSlotModel
from to_array.tokenizationK import FullTokenizer
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")


# read command-line parameters
parser = argparse.ArgumentParser('Evaluating the BERT / ALBERT NLU model')
parser.add_argument('--model', '-m', help = 'Path to BERT / ALBERT NLU model', type = str, required = True)
parser.add_argument('--type', '-tp', help = 'bert or albert', type = str, default = 'bert', required = False)
parser.add_argument('--bertpath', '-bp', help = '프리트레인된 BERT 모듈 경로', type = str, default = "/content/drive/MyDrive/bert-module")



VALID_TYPES = ['bert', 'albert']

args = parser.parse_args()
load_folder_path = args.model
type_ = args.type

# this line is to enable gpu
os.environ["CUDA_VISIBLE_DEVICES"]="0"

config = tf.ConfigProto(intra_op_parallelism_threads=0,
                        inter_op_parallelism_threads=0,
                        allow_soft_placement=True,
                        device_count = {'GPU': 1})
sess = tf.compat.v1.Session(config=config)

if type_ == 'bert':
    bert_model_hub_path = args.bertpath
    is_bert = True
elif type_ == 'albert':
    bert_model_hub_path = 'https://tfhub.dev/google/albert_base/1'
    is_bert = False
else:
    raise ValueError('type must be one of these values: %s' % str(VALID_TYPES))


# 모델과 벡터라이저 불러오기
vocab_file = os.path.join(bert_model_hub_path, "assets/vocab.korean.rawtext.list")
bert_to_array = BERTToArray(is_bert, vocab_file)

#모델
print('Loading models ...')
if not os.path.exists(load_folder_path):
    raise FileNotFoundError('Folder `%s` not exist' % load_folder_path)

with open(os.path.join(load_folder_path, 'tags_to_array.pkl'), 'rb') as handle:
    tags_to_array = pickle.load(handle)
    slots_num = len(tags_to_array.label_encoder.classes_)

model = BertSlotModel.load(load_folder_path, sess)
tokenizer = FullTokenizer(vocab_file=vocab_file)

answer_name_arr = ['성함이 어떻게 되시나요?', '이름을 말해주세요.']
answer_phone_arr = ['연락 가능한 번호를 써주세요.(예시 : 010-1234-1234)', '전화번호를 알려주세요.(예시 : 010-1234-1234)', '예약자 분의 번호를 입력해주세요.(예시 : 010-1234-1234)']
answer_date_arr = ['몇 월 며칠에 예약하고 싶으신가요?', '예약하고 싶은 월일을 입력해주세요. (예시: 1월 3일)', '예약하시려는 날짜를 알려주세요.']
answer_start_arr = ['몇 시로 예약하실 건가요?', '몇 시부터 사용하실 건가요?', '사용 시작 시간을 알려주세요.']
answer_end_arr = ['몇 시까지 이용하실 건가요?', '언제까지 사용하실 건가요?', '종료 시간을 알려주세요.']
answer_person_arr = ['총 몇 명이신가요?', '몇 명이서 쓰실 건가요?', '이용 인원을 말씀해주세요?']

r_name = ''
r_phone_no = ''
r_date = ''
r_start_time = ''
r_end_time = ''
r_person = ''
r_num = 0

while True:
    print('\nEnter your sentence: ')
    try:
        input_text = input().strip()

    except:
        continue

    if input_text == 'quit':
        break

    input_text = ' '.join(tokenizer.tokenize(input_text))

    #벡터화
    data_text_arr = [input_text]
    print(data_text_arr)
    data_input_ids, data_input_mask, data_segment_ids = bert_to_array.transform(data_text_arr)

    #예측 결과 출력
    inferred_tags, slots_score = model.predict_slots([data_input_ids, data_input_mask, data_segment_ids], tags_to_array)
    print("Inferred tags")
    print(inferred_tags)
    print("Slots score")
    print(slots_score)    
    
    for i in range(0,len(inferred_tags[0])):
        if inferred_tags[0][i]=='이름':
            if r_name == '': r_num += 1
            r_name = inferred_tags[0][i]
        elif inferred_tags[0][i]=='번호':
            if r_phone_no == '': r_num += 1
            r_phone_no = inferred_tags[0][i]     
        elif inferred_tags[0][i]=='날짜':
            if r_date == '': r_num += 1
            r_date = inferred_tags[0][i]     
        elif inferred_tags[0][i]=='시작시간':
            if r_start_time == '': r_num += 1
            r_start_time = inferred_tags[0][i]     
        elif inferred_tags[0][i]=='종료시간':
            if r_end_time == '': r_num += 1
            r_end_time = inferred_tags[0][i]     
        elif inferred_tags[0][i]=='인원':
            if r_person == '': r_num += 1
            r_person = inferred_tags[0][i] 

    if r_num >= 6:
        print('예약이 완료되었습니다. 예약을 종료합니다.')
        break
    elif  r_num == 0:   
        print('죄송합니다 제가 이해를 잘 못해서 다시 한번 입력해주세요.')
    else:        
        if r_name == '':
            print(np.random.choice(answer_name_arr, 1))
        elif r_phone_no == '':
            print(np.random.choice(answer_phone_arr, 1))
        elif r_date == '':
            print(np.random.choice(answer_date_arr, 1))
        elif r_start_time == '':
            print(np.random.choice(answer_start_arr, 1))
        elif r_end_time == '':
            print(np.random.choice(answer_end_arr, 1))
        elif r_person == '':
            print(np.random.choice(answer_person_arr, 1))

            
tf.compat.v1.reset_default_graph()