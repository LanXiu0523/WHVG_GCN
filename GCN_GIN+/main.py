import easydict
import numpy as np
from tqdm import tqdm
import tensorflow as tf

from util import load_data, separate_data
from models.graphcnn import GraphCNN


args = easydict.EasyDict({
    "dataset": 'HVG',
    "device": 0,
    "batch_size": 16,
    "iters_per_epoch": 50,
    "epochs":50,
    "lr": 0.005,  
    "seed": 0,
    "fold_idx": 0,
    "num_layers": 5,
    "num_mlp_layers": 2,
    "hidden_dim": 32,
    "final_dropout": 0.5,
    "graph_pooling_type": 'sum',
    "neighbor_pooling_type": 'sum',
    "learn_eps": 'store_true',
    'degree_as_tag': 'store_true',
    'filename': 'output.txt'
    
})


loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

graphs, num_classes = load_data(args.dataset, args.degree_as_tag)
train_graphs, test_graphs = separate_data(graphs, args.seed, args.fold_idx)
labels = tf.constant([graph.label for graph in train_graphs])

model = GraphCNN(args.num_layers, args.num_mlp_layers, args.hidden_dim, num_classes, args.final_dropout, args.learn_eps, args.graph_pooling_type, args.neighbor_pooling_type)

optimizer = tf.keras.optimizers.Adam(lr = args.lr)


#def train(loss,model,opt,original):    
def train(args,model,train_graphs,opt,epoch):
  total_iters = args.iters_per_epoch
  pbar = tqdm(range(total_iters),unit = 'batch')
  
  loss_accum = 0
  for pos in pbar:
    selected_idx = np.random.permutation(len(train_graphs))[:args.batch_size]
    batch_graph = [train_graphs[idx] for idx in selected_idx]
    labels = tf.constant([graph.label for graph in batch_graph])
    loss_accum = 0
    with tf.GradientTape() as tape:
      output = model(batch_graph)
      loss = loss_object(labels,output)
      
    gradients = tape.gradient(loss,model.trainable_variables)
    gradient_variables = zip(gradients, model.trainable_variables)
    opt.apply_gradients(gradient_variables)
    loss_accum += loss
    
    #report
    pbar.set_description(f'epoch: {epoch}')
    
  average_loss = loss_accum/total_iters
  print(f'loss training: {average_loss}')
  return average_loss


#pass data to model with minibatch during testing to avoid memory overflow (does not perform backpropagation)
def pass_data_iteratively(model, graphs, minibatch_size = 64):
    output = []
    idx = np.arange(len(graphs))
    for i in range(0, len(graphs), minibatch_size):
        sampled_idx = idx[i:i+minibatch_size]
        if len(sampled_idx) == 0:
            continue    
        output.append(model([graphs[j] for j in sampled_idx]))
    return tf.concat(output,0)

  
def tf_check_acc(pred,labels):
    pred = tf.cast(pred,tf.int32)
    correct = tf.equal(pred,labels)
    answer = 0
    for element in correct:
      if element:
        answer +=1
    return answer
  

def test(args, model, train_graphs, test_graphs, epoch):
    output = pass_data_iteratively(model, train_graphs)
    pred = tf.argmax(output,1)
    labels = tf.constant([graph.label for graph in train_graphs])

    correct = tf_check_acc(pred,labels)
    acc_train = correct / float(len(train_graphs))

    output = pass_data_iteratively(model, test_graphs)
    pred = tf.argmax(output,1)
    labels = tf.constant([graph.label for graph in test_graphs])
    correct = tf_check_acc(pred,labels)
    acc_test = correct / float(len(test_graphs))

    print("accuracy train: %f test: %f" % (acc_train, acc_test))

    return acc_train, acc_test



f = open(args.filename, 'a')
if args.filename == "":
  print("OutputFileNameError")
f.truncate(0)

for epoch in range(1, args.epochs + 1):
    if epoch % 5 == 0:
      optimizer.lr = optimizer.lr * 0.5    
    print (optimizer.lr)
    avg_loss = train(args, model, train_graphs, optimizer, epoch)
    acc_train, acc_test = test(args, model, train_graphs, test_graphs, epoch)
    #'1.01e-16'==0,has no practical significance. It is only for standardized output and convenient data processing        
    f.write("Epoch:%03d  Avg_loss:%.8s  Acc_train:%8f  Acc_test:%8f\n" % (epoch, str(float(avg_loss)+1.01e-16), acc_train, acc_test))
    print("")

    print(model.eps)

f.close()


