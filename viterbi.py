
import numpy as np
import sys

pi_mat1 = np.genfromtxt(sys.argv[4], delimiter=' ', dtype=float)
A_mat1 = np.genfromtxt(sys.argv[6], delimiter=' ', dtype=float)
B_mat1 = np.genfromtxt(sys.argv[5], delimiter=' ', dtype=float)


def read_test_files(test, index_word, index_tag):
    file1 = open(test, "r+")
    test_list = file1.readlines();
    
    file2 = open(index_word, "r+")
    word_index = file2.readlines()
    
    file3 = open(index_tag, "r+")
    tag_index = file3.readlines()
    
    for i in range(len(word_index)):
        word_index[i] = word_index[i].strip()
        
    for i in range(len(tag_index)):
        tag_index[i] = tag_index[i].strip()
    
    indexed_word = []
    indexed_tag = []
    for line in test_list:
        words_tags = line.split(" ")
        w_ind_list = []
        t_ind_list = []
        for w in words_tags:
            word_tag = w.strip().split("_")
            w_ind = word_index.index(word_tag[0])
            t_ind = tag_index.index(word_tag[1])
            w_ind_list.append(w_ind)
            t_ind_list.append(t_ind)
        indexed_word.append(w_ind_list)
        indexed_tag.append(t_ind_list)
    return indexed_word, indexed_tag, word_index, tag_index

indexed_word, indexed_tag, word_index, tag_index = read_test_files(sys.argv[1],sys.argv[2], sys.argv[3])

def viterbi(indexed_word, indexed_tag, pi_mat1, A_mat1, B_mat1, tag_index):
    st_cnt = len(tag_index)
    error = 0
    total_words = 0
    pred_states = []
    for i in range(len(indexed_word)):
        total_words += len(indexed_word[i])
        vit_val = np.zeros((st_cnt, len(indexed_word[i])))
        vit_pos = np.zeros((st_cnt, len(indexed_word[i])))
        
        for j in range(st_cnt):
            vit_val[j][0] = np.log(pi_mat1[j]) + np.log(B_mat1[j][indexed_word[i][0]])
            vit_pos[j][0] = int(j)
            
        for q in range(1, len(indexed_word[i])):
            for j in range(st_cnt):
                temp_list = [vit_val[h][q-1] + np.log(A_mat1[h][j]) for h in range(st_cnt)]
                vit_val[j][q] = np.log(B_mat1[j][indexed_word[i][q]]) + max(temp_list)
                vit_pos[j][q] = int(np.argmax(temp_list))
                
        state_seq = []
        last_state = np.argmax(vit_val[:,-1])
        state_seq.append(last_state)
        for u in range(len(indexed_word[i])-1, 0, -1):
            next_state = int(vit_pos[last_state][u])
            state_seq = [next_state , *state_seq]
            last_state = next_state
        
        for l in range(len(state_seq)):
            if (state_seq[l] != indexed_tag[i][l]):
                error += 1
                
        pred_states.append(state_seq)
        
    accuracy = 1.0 - error/float(total_words)
    
    return pred_states, accuracy, vit_val, vit_pos

pred_states, accuracy, vit_val, vit_pos = viterbi(indexed_word, indexed_tag, pi_mat1, A_mat1, B_mat1, tag_index)

file4 = open(sys.argv[8], "w")
file4.writelines("Accuracy: " + str(accuracy) + "\n")
file4.close()

file5 = open(sys.argv[7], "w")
for i in range(len(pred_states)):
    for j in range(len(pred_states[i])):
        if j < len(pred_states[i])-1:
            file5.writelines(word_index[indexed_word[i][j]] + "_" + tag_index[pred_states[i][j]] + " ")
        else:
            file5.writelines(word_index[indexed_word[i][j]] + "_" + tag_index[pred_states[i][j]])
    file5.writelines("\n")
file5.close()
                
        