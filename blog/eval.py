#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import os
import data_helpers
from multi_class_data_loader import MultiClassDataLoader
from word_data_processor import WordDataProcessor


# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

data_loader = MultiClassDataLoader(tf.flags, WordDataProcessor())
data_loader.define_flags()
"""
data_loader.define_flags() 메소드 실행할시 코드
self.__flags.DEFINE_string("train_data_file", "./data/kkk.train", "Data source for the training data.")
self.__flags.DEFINE_string("dev_data_file", "./data/kkk.dev", "Data source for the cross validation data.")
self.__flags.DEFINE_string("class_data_file", "./data/kkk.cls", "Data source for the class list.")
"""


def eval(input_data):

    FLAGS = tf.flags.FLAGS
    FLAGS._parse_flags()

    print ("\nParameters:")
    for attr, value in sorted(FLAGS.__flags.items()): # flags.items()알파벳순 정렬
        print("{}={}".format(attr.upper(), value))


    # Parameters
    # ==================================================


    #여기 부분바꾸면 개인 데이터셋으로 사용가능한듯.
    if FLAGS.eval_train:
        x_raw=[input_data]
        y_test=[1]
        #x_raw, y_test = data_loader.load_data_and_labels()
        #y_test = np.argmax(y_test, axis=1)
    else:
        #x_raw, y_test = data_loader.load_dev_data_and_labels()
        """개인 데이터 입력할것"""
        x_raw=[input_data]
        y_test = [1]
        #y_test 는 원래 dev 파일에 있던 , 다음의 항목을 나타낸다.
        #y_test= np.argmax(y_test, 0)




    # checkpoint_dir이 없다면 가장 최근 dir 추출하여 셋팅
    if FLAGS.checkpoint_dir == "":
        all_subdirs = ["./runs/" + d for d in os.listdir('./runs/.') if os.path.isdir("./runs/" + d)]
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        FLAGS.checkpoint_dir = latest_subdir + "/checkpoints/"
        print(FLAGS.checkpoint_dir)


    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
    vocab_processor = data_loader.restore_vocab_processor(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    print ("vocab_processor:", vocab_processor)
    print ("x_raw:", x_raw)
    print ("x_test:", x_test)
    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variable
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            print ("input_x:",input_x)
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            #score =graph.get_operation_by_name("output/scores/(scores)").output[0]
            score =graph.get_tensor_by_name('output/scores:0')

            # Tensors we want to evaluate
            #predictions = graph.get_operation_by_name("output/predictions").outputs[0]



            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)
            #print "batches:" ,batches

            for x_test_batch in batches:
                batch_predictions1 = sess.run(score, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                #batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                #print(batch_predictions1)# predictions은 결정된 상태이다.
                print ("batch_predictions[0]:", batch_predictions1[0])

                #softmax를 이용해서 확률 계산
                e_x = np.exp(batch_predictions1[0]-np.max(batch_predictions1[0]))
                prob_predictions= (e_x/e_x.sum(axis=0))

                print ("sum prob:",sum(prob_predictions,0.0))
                print ("all prob:",prob_predictions)
                arg_predictions=prob_predictions.argsort()
                #print(arg_predictions)


                prob_predictions.sort()
                print("first prob:",prob_predictions[-1])
                print("second prob:",prob_predictions[-2])

                arg_predictions = [arg_predictions[-1]]
                #all_predictions =np.concatenate([all_predictions,batch_predictions])

                #print(all_predictions)
                #print(batch_predictions.astype(int))

    # 데이터 로더를 통해 클래스 라벨을 부착한다.

    """class_predictions = data_loader.class_labels(batch_predictions) #class predictions에 예측값이 들어간다.
    print(class_predictions)"""

    class_predictions = data_loader.class_labels(arg_predictions)

    print ("class predictions :" ,class_predictions[0])
    return(class_predictions[0],prob_predictions[-1])

#eval("기록물 이관")
