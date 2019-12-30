import numpy as np
import sys

def read_files(train, index_word, index_tag):
    file1 = open(train, "r+")
    train_list = file1.readlines();
    
    file2 = open(index_word, "r+")
    word_index = file2.readlines()
    
    file3 = open(index_tag, "r+")
    tag_index = file3.readlines()
    
    for i in range(len(word_index)):
        word_index[i] = word_index[i].strip()
        
    for i in range(len(tag_index)):
        tag_index[i] = tag_index[i].strip()
    
    indexed_train = []
    for line in train_list:
        words_tags = line.split(" ")
        wt_ind_list = []
        for w in words_tags:
            word_tag = w.strip().split("_")
            w_ind = word_index.index(word_tag[0])
            t_ind = tag_index.index(word_tag[1])
            wt_ind_list.append((w_ind, t_ind))
        indexed_train.append(wt_ind_list)
            
    return indexed_train, word_index, tag_index

def populate_params(indexed_train, word_index, tag_index):
    
    pi = np.zeros(len(tag_index))
    A = np.zeros((len(tag_index), len(tag_index)))
    B = np.zeros((len(tag_index), len(word_index)))
    
    for line in indexed_train:
        pi[line[0][1]] +=1
        
        for i in range(len(line)-1):
            A[line[i][1], line[i+1][1]] += 1
            
        for tup in line:
            B[tup[1], tup[0]] +=1
            
    pi_mat = (pi+1)/np.sum(pi+1)
    A_mat = (A + 1)/np.sum(A + 1, axis=1)[:,None]
    B_mat = (B+1)/np.sum(B+1, axis=1)[:,None]
    
    return pi_mat, A_mat, B_mat
    
indexed_train, word_index, tag_index = read_files(sys.argv[1], sys.argv[2], sys.argv[3])
pi_mat, A_mat, B_mat = populate_params(indexed_train, word_index, tag_index)


file6 = open(sys.argv[4], "w")
for i in range(len(pi_mat)):
    file6.writelines(str(pi_mat[i]) + "\n")
file6.close()

file7 = open(sys.argv[6], "w")
for i in range(A_mat.shape[0]):
    for j in range(A_mat.shape[1]):
        if j < A_mat.shape[1] - 1:
            file7.writelines(str(A_mat[i][j]) + " ")
        else:
            file7.writelines(str(A_mat[i][j]))
    file7.writelines("\n")
file7.close()

file8 = open(sys.argv[5], "w")
for i in range(B_mat.shape[0]):
    for j in range(B_mat.shape[1]):
        if j < B_mat.shape[1] - 1:
            file8.writelines(str(B_mat[i][j]) + " ")
        else:
            file8.writelines(str(B_mat[i][j]))
    file8.writelines("\n")
file8.close()

    
            
        
