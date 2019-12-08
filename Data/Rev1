import tensorflow as tf
from tensorflow.contrib.layers import fully_connected
from tensorflow.examples.tutorials.mnist import input_data
import os
import numpy as np
import matplotlib.pyplot as plt
#from skimage.transform import resize
import scipy as sc
import ConvHelper
import pickle
import csv as csv
import datetime
import os as os
import random
import Placeholders
import KaggleRNNDataManager
import word2Vec as w2v


model_folder_name = "models/adience"
model_filename = os.path.join(model_folder_name,"main_model.ckpt")
STEPS = 50
MINIBATCH_SIZE = 100


#Kaggle data
current_working_folder = os.path.dirname(os.getcwd())
kaggle_files_path = os.path.join(current_working_folder, 'Project/Datasets/Kaggle/')
kaggle_images_path = os.path.join(current_working_folder, 'Project/Datasets/Kaggle/Images')
train_metadata_filename = 'Kaggle-str-process.csv'
test_metadata_filename = 'Kaggle-str-process.csv'
today = datetime.datetime.now()
format = "%d_%m_%Y_%H_%M_%S"
run_folder = today.strftime(format)


x_main = tf.placeholder(tf.float32, shape=[None, Placeholders.feature_width])
keep_prob = tf.placeholder(tf.float32)





x = Placeholders.x
y_ = Placeholders.y_

def test(sess, accuracy, test,fc7, word_vec, y_conv, correct_prediction,loss, kdm, epoch, datasetType = "Test"):
    print ("Starting Test")
    number_of_test_batches = 5
    number_of_samples_per_batch = 10
    total_samples = number_of_test_batches * number_of_samples_per_batch
    random_index = random.randint(0,len(test.features) - total_samples)

    #print len(adience.test.images)
    data = test
    batch_features = data.features[random_index:random_index+total_samples]
    batch_labels = data.labels[random_index:random_index+total_samples]
    batch_x = batch_features.reshape(-1, Placeholders.feature_width)

    acc = sess.run(accuracy, feed_dict={x_main: batch_x, y_: batch_labels,
                                     keep_prob: 1.0})
    print (datasetType + " Accuracy: {:.4}%".format(acc * 100))
    mse = loss.eval(feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0})
    predictions = np.array(sess.run(tf.argmax(y_conv, 1), feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0}))
    correct_predictions = np.array(sess.run(correct_prediction, feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0}))
    raw_data = kdm.test_raw if datasetType == "Test" else (kdm.train_raw if datasetType == "Train" else kdm.validation_raw)
    write_results_to_file(mse, acc * 100, raw_data, predictions, correct_predictions, epoch, datasetType)
    return acc * 100


def test_all(sess, accuracy, test,fc7, word_vec, y_conv, correct_prediction,loss, kdm, epoch = 0, datasetType = "Test"):
    print ("Starting test on all data:" + datasetType)

    #print len(adience.test.images)
    data = test
    #batch_features =  data.features
    #batch_labels = data.labels
    batch_features = data.features[:, :Placeholders.feature_width]
    batch_labels = one_hot(data.features[:, Placeholders.feature_width])
    batch_x = batch_features#batch_features.reshape(-1, Placeholders.feature_width)

    acc = sess.run(accuracy, feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0})
    print (datasetType + " Accuracy: {:.4}%".format(acc * 100))
    mse = loss.eval(feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0})
    print(datasetType + " Loss: {:.4}".format(mse))
    predictions = np.array(sess.run(tf.argmax(y_conv, 1), feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0}))
    correct_predictions = np.array(sess.run(correct_prediction, feed_dict={x_main: batch_x, y_: batch_labels, keep_prob: 1.0}))
    raw_data = kdm.test_raw if datasetType == "Test" else (kdm.train_raw if datasetType == "Train" else kdm.validation_raw)
    write_results_to_file(mse, acc * 100, raw_data, predictions, correct_predictions, epoch, datasetType)
    return acc*100


# def test1(sess, accuracy, test,fc7, word_vec):
#     print ("Starting Test")
#     batch = get_features_and_labels(test, sess, fc7, word_vec)
#     batch_x = batch[0].reshape(-1, Placeholders.feature_width)
#
#     acc = sess.run(accuracy, feed_dict={x_main: batch_x, y_: batch[1],
#                                      keep_prob: 1.0})
#     print ("Accuracy: {:.4}%".format(acc * 100))

def train(sess, train, retrain, fc7):
    output_folder = os.path.join(current_working_folder,"Project/output")
    output_folder = os.path.join(output_folder, run_folder)
    if not os.path.exists(output_folder):
        print("Creating folder: " + output_folder)
        os.makedirs(output_folder)
    else:
        print("Folder exists: " + output_folder)

    word_vec = w2v.word2vec()
    kdm = KaggleRNNDataManager.KaggleRNNDataManager(kaggle_files_path + train_metadata_filename, sess, fc7, word_vec)


    basic_cell = tf.contrib.rnn.BasicRNNCell(num_units = Placeholders.n_neurons, activation = tf.tanh)
    outputs , states = tf.nn.dynamic_rnn(basic_cell, Placeholders.rnn_X, dtype= tf.float32)
    other_features = Placeholders.rnn_other_features
    rnn_features = np.hstack((states, other_features))
    y_conv = tf.layers.dense(rnn_features, Placeholders.n_classes)
    #xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels= Placeholders.y_ , logits= logits)
    #loss = tf.reduce_mean(xentropy)
    #optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    #optimizer = tf.train.RMSPropOptimizer(0.1, 0.9, 0.01)
    #training_op = optimizer.minimize(loss)
    #correct = tf.nn.in_top_k(logits, Placeholders.y_, 1)


    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits= y_conv,
                                                                   labels=y_))
    loss = tf.reduce_mean(cross_entropy)
    train_step = tf.train.AdamOptimizer(1e-5).minimize(loss)

    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    STEPS = 500
    MINIBATCH_SIZE = 50

    #Retrieve training data

    #training_data = get_fc7_representation(train, sess, fc7)

    if os.path.exists(model_folder_name) & (not retrain):
        print("Model found in file: %s" % model_filename)
        saver.restore(sess, model_filename)
    else:
        if (retrain) & os.path.exists(model_folder_name):
            print ("Retraining the model.")
        print ("Starting at:" , datetime.datetime.now())
        sess.run(tf.global_variables_initializer())
        print ("Initialization done at:" , datetime.datetime.now())
        for epoch in range(STEPS):
            print ("Starting epoch", epoch, " at:", datetime.datetime.now())
            for batch_count in range(int(len(kdm.train.features)/MINIBATCH_SIZE)):
                batch = kdm.next_batch(MINIBATCH_SIZE)
                features = batch[0][:,:Placeholders.feature_width]
                #print(batch[0][:,Placeholders.feature_width])
                labels = one_hot(batch[0][:,Placeholders.feature_width])
                #print(features.shape)
                #print(labels.shape)
                batch_x = features
                sess.run(train_step, feed_dict={x_main: batch_x, y_: labels,keep_prob: 0.5})
            if(epoch%10 == 0):
                mse = loss.eval(feed_dict={x_main: batch_x, y_: labels, keep_prob: 0.5})
                print("Iter " + str(epoch) + ", Minibatch Loss= " + \
                      "{:.6f}".format(mse))
                train_accuracy = test_all(sess, accuracy, kdm.train, fc7, word_vec, y_conv, correct_prediction, loss, kdm, epoch, datasetType="Train")
                validation_accuracy = test_all(sess, accuracy, kdm.validation, fc7, word_vec, y_conv, correct_prediction, loss, kdm, epoch, datasetType="Validation")
                #test_accuracy = test(sess, accuracy, kdm.test, fc7, word_vec, y_conv, correct_prediction, loss, epoch, datasetType="Test")
                if (validation_accuracy > Placeholders.best_accuracy_so_far):
                    Placeholders.best_accuracy_so_far = validation_accuracy
                    test_all(sess, accuracy, kdm.test, fc7, word_vec, y_conv, correct_prediction, loss, kdm, epoch)
                elif (train_accuracy > 60):
                    test_all(sess, accuracy, kdm.test, fc7, word_vec, y_conv, correct_prediction, loss, kdm, epoch)
        test_all(sess, accuracy, kdm.test, fc7, word_vec, y_conv, correct_prediction, loss, kdm)
        save_path = saver.save(sess, model_filename)
        print("Model saved in file: %s" % save_path)
    return accuracy

def one_hot(vec, vals = Placeholders.n_classes):
    n = len(vec)
    vec = [int(val) for val in vec]
    out = np.zeros((n, vals))
    out[range(n), vec] = 1
    return out

def write_results_to_file(loss, accuracy, test_data_raw, predictions, correct_predictions, epoch, datasetType):
    today = datetime.datetime.now()
    format = "_%d_%m_%Y_%H_%M_%S"
    filename = "output/" + run_folder + "/" + datasetType + today.strftime(format) + "_Iteration_" + str(epoch)  + "_Accuracy_" + str(round(accuracy, 2)) + ".csv"
    with open(filename, 'wt') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([datasetType + " Accuracy = " + str(accuracy)])
        wr.writerow(["Loss = " + str(loss)])
        wr.writerow(get_header())
        for i in range(len(test_data_raw)):
            local_result = []
            local_result.append(test_data_raw[i].name)
            local_result.append(test_data_raw[i].description)
            local_result.append(test_data_raw[i].tweet_text)
            local_result.append(test_data_raw[i].link_color)
            local_result.append(test_data_raw[i].sidebar_color)
            local_result.append(test_data_raw[i].label)
            local_result.append(predictions[i])
            local_result.append(correct_predictions[i])
            wr.writerow(local_result)

def get_header():
    header = []
    header.append('name')
    header.append('description')
    header.append('tweet_text')
    header.append('link_color')
    header.append('sidebar_color')
    header.append('true label')
    header.append('predicted label')
    header.append('correct_prediction')
    return header

