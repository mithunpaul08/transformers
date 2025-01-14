#In this code we go through predictions of 3 models and do a voting between 3 best.
'''
If(all 3 models agree) {
	use the predicted label

}

If (2 out of 3 models agree)

{

	use the predicted label

}

else {

	pick the label predicted with the highest confidence (after softmax)

}

'''
#Adapted from https://github.com/FakeNewsChallenge/fnc-1/blob/master/scorer.py
#Original credit - @bgalbraith
import pandas as pd
import numpy as np

LABELS = ['disagree', 'agree', 'discuss', 'unrelated']
LABELS_RELATED = ['unrelated','related']
RELATED = LABELS[0:3]

def score_submission(gold_labels, test_labels):
    score = 0.0
    cm = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

    for i, (g, t) in enumerate(zip(gold_labels, test_labels)):
        g_stance, t_stance = g, t
        if g_stance == t_stance:
            score += 0.25
            if g_stance != 'unrelated':
                score += 0.50
        if g_stance in RELATED and t_stance in RELATED:
            score += 0.25

        cm[LABELS.index(g_stance)][LABELS.index(t_stance)] += 1

    return score, cm


def print_confusion_matrix(cm):
    lines = []
    header = "|{:^11}|{:^11}|{:^11}|{:^11}|{:^11}|".format('', *LABELS)
    line_len = len(header)
    lines.append("-"*line_len)
    lines.append(header)
    lines.append("-"*line_len)

    hit = 0
    total = 0
    for i, row in enumerate(cm):
        hit += row[i]
        total += sum(row)
        lines.append("|{:^11}|{:^11}|{:^11}|{:^11}|{:^11}|".format(LABELS[i],
                                                                   *row))
        lines.append("-"*line_len)
    print('\n'.join(lines))


def report_score(actual,predicted):
    score,cm = score_submission(actual,predicted)
    best_score, _ = score_submission(actual,actual)

    #print_confusion_matrix(cm)
    print("Score: " +str(score) + " out of " + str(best_score) + "\t("+str(score*100/best_score) + "%)")
    return score*100/best_score


#column order in raw data: index	 gold	prediction_logits	 prediction_label	plain_text
#dtypes = [np.int64, 'str', 'object', 'str','str']
dtypes={'a': np.float64, 'b': np.int32, 'c': 'Int64','d': 'Int64','e': 'Int64'}


model1_predictions=pd.read_csv("predictions/predictions_fnc2fever_by_lex_model.txt", sep="\t", dtype=dtypes)
model2_predictions=pd.read_csv("predictions/predictions_on_test_partition_7b2f40_legendary_voice_best_figerspecific_7474acc_6344fncs.txt", sep="\t", dtype=dtypes)
model3_predictions=pd.read_csv("predictions/predictions_on_test_partition_using_lex_cdaccuracy6908_wandbGraphSweetWater1001.txt", sep="\t", dtype=dtypes)
gold=pd.read_csv("predictions/fnc_dev_gold.tsv", sep="\t")


# are the lengths different?
assert len(gold) == len(model1_predictions)
assert len(gold) == len(model2_predictions)
assert len(model1_predictions) == len(model2_predictions)
assert len(model1_predictions) == len(model3_predictions)

model1_predicted_labels_string=[]
model2_predicted_labels_string=[]
model3_predicted_labels_string=[]
gold_labels=[]
model1_sf=[]
model2_sf=[]
model3_sf=[]

#get labels and softmaxes into its own lists
#column order in raw data: index	 gold	prediction_logits	 prediction_label	plain_text
for (mod1, mod2, mod3) in zip(model1_predictions.values, model2_predictions.values, model3_predictions.values):
    model1_predicted_labels_string.append(mod1[3])
    model2_predicted_labels_string.append(mod2[3])
    model3_predicted_labels_string.append(mod3[3])
    gold_labels.append(mod3[1])
    model1_sf.append(mod1[2])
    model2_sf.append(mod2[2])
    model3_sf.append(mod3[2])



assert len(model1_predicted_labels_string) == len(model2_predicted_labels_string) == len(gold_labels)
assert len(model1_sf) == len(model2_sf) == len(gold_labels)
assert not model1_sf[0] ==model2_sf[0]
assert not model1_sf[0] ==model3_sf[0]


#for some reason the softmaxes was read as a string instead of list- strip out []
def convert_sf_string_to_lists(sf):
    list_as_floats=[]
    for x in sf.split(","):
        y=x.strip("[]")
        list_as_floats.append(float(y))
    return list_as_floats



def two_model_voting(model1_predicted_labels, model2_predicted_labels, model1_softmaxes, model2_softmaxes,gold_labels):
    assert len(model1_predicted_labels) == len(model2_predicted_labels)
    assert len(model1_softmaxes) == len(model2_softmaxes)

    differ_counter=0
    both_match_counter=0
    both_match_gold_counter=0
    predictions_post_voting=[]
    for index,(pred_model1, pred_model2,sf1,sf2, gold) in enumerate(zip(model1_predicted_labels, model2_predicted_labels, model1_softmaxes, model2_softmaxes,gold_labels)):
        if (pred_model1==pred_model2):
            both_match_counter+=1
            predictions_post_voting.append(pred_model1)
            if(pred_model1==gold):
                both_match_gold_counter+=1

        else:
            #if the labels dont match, find who has higher confidence scorediffer_counter
            # differ_counter+=1
            # predictions_post_voting.append(pred_model1)
            sf1_list=convert_sf_string_to_lists(sf1)
            sf2_list = convert_sf_string_to_lists(sf2)
            highest_confidence_model1=max(sf1_list)
            highest_confidence_model2 = max(sf2_list)
            if highest_confidence_model1>highest_confidence_model2:
                predictions_post_voting.append(pred_model1)
            else:
                predictions_post_voting.append(pred_model2)

    print(f"differcounter={differ_counter}")
    print(f"both_match_counter={both_match_counter}")
    print(f"both_match_gold_counter={both_match_gold_counter}")

    return predictions_post_voting




def three_model_voting_two_model_agrees_but_one_is_lex(combined_model_predicted_labels, delex_model_predicted_labels, lex_model_predicted_labels, model1_softmaxes, model2_softmaxes, model3_softmaxes):
    assert len(combined_model_predicted_labels) == len(delex_model_predicted_labels)
    assert len(model1_softmaxes) == len(model2_softmaxes)
    assert len(model1_softmaxes) == len(model3_softmaxes)

    differ_counter=0
    both_match_counter=0
    both_match_gold_counter=0
    predictions_post_voting=[]
    for index,(pred_model1, pred_model2, pred_model3,sf1,sf2, sf3) in enumerate(zip(combined_model_predicted_labels, delex_model_predicted_labels, lex_model_predicted_labels, model1_softmaxes, model2_softmaxes, model3_softmaxes)):
        all_preds=[pred_model1,pred_model2,pred_model3]
        if (pred_model1==pred_model2==pred_model3):
            predictions_post_voting.append(pred_model1)
        else:
            if (pred_model1 == pred_model3):
                predictions_post_voting.append(pred_model1)
            else:
                if (pred_model2 == pred_model3):
                    both_match_counter += 1
                    predictions_post_voting.append(pred_model2)
                else:
                    # if all 3 labels dont match, pick lex
                    # predictions_post_voting.append(pred_model3)
                    # continue

                    #if all 3 labels dont match, find who has higher confidence scorediffer_counter
                    sf1_list=convert_sf_string_to_lists(sf1)
                    sf2_list = convert_sf_string_to_lists(sf2)
                    sf3_list = convert_sf_string_to_lists(sf3)
                    highest_confidence_model1=max(sf1_list)
                    highest_confidence_model2 = max(sf2_list)
                    highest_confidence_model3 = max(sf3_list)
                    all_conf=[highest_confidence_model1,highest_confidence_model2,highest_confidence_model3]
                    best=max(all_conf)
                    best_model_index=all_conf.index(best)
                    predictions_post_voting.append(all_preds[best_model_index])

    print(f"differcounter={differ_counter}")
    print(f"both_match_counter={both_match_counter}")
    print(f"both_match_gold_counter={both_match_gold_counter}")

    return predictions_post_voting


def three_model_voting_any_two_models_agree(model1_predicted_labels, model2_predicted_labels, model3_predicted_labels, gold_labels,model1_softmaxes, model2_softmaxes, model3_softmaxes):
    assert len(model1_predicted_labels) == len(model2_predicted_labels)
    assert len(model1_softmaxes) == len(model2_softmaxes)
    assert len(model1_softmaxes) == len(model3_softmaxes)

    how_many_times_do_all_3_models_disagree_with_each_other=0
    when_all_3_models_disagree_with_each_other_how_many_times_was_delex_stand_alone_model_picked_for_its_high_confidence = 0
    of_all_times_delex_stand_alone_was_picked_how_many_times_delex_stand_alone_matched_with_gold =0
    when_all_3_models_disagree_with_each_other_how_many_times_was_combined_model_picked_for_its_high_confidence = 0
    of_all_times_that_it_was_picked_for_high_confidence_how_many_times_did_combined_match_with_gold = 0
    when_all_3_models_disagree_with_each_other_how_many_times_was_lex_stand_alone_model_picked_for_its_high_confidence = 0
    of_all_times_lex_stand_alone_was_picked_how_many_times_lex_stand_alone_matched_with_gold = 0

    predictions_post_voting=[]
    for index,(pred_student_teacher, pred_delex_stand_alone, pred_lex_stand_alone,gold, sf1,sf2, sf3) in enumerate(zip(model1_predicted_labels, model2_predicted_labels, model3_predicted_labels,gold_labels, model1_softmaxes, model2_softmaxes,model3_softmaxes)):
        all_preds=[pred_student_teacher,pred_delex_stand_alone,pred_lex_stand_alone]
        if (pred_student_teacher==pred_delex_stand_alone==pred_lex_stand_alone):
            predictions_post_voting.append(pred_student_teacher)
        else:
            #if any two models match, pick that.., one of them neednt be lex,
            if (pred_student_teacher == pred_lex_stand_alone):
                predictions_post_voting.append(pred_student_teacher)
            else:
                if (pred_delex_stand_alone == pred_lex_stand_alone):
                    predictions_post_voting.append(pred_delex_stand_alone)
                else:
                    if (pred_student_teacher == pred_delex_stand_alone):
                        predictions_post_voting.append(pred_delex_stand_alone)
                    else:
                        # if all 3 labels dont match, pick ______________
                        #predictions_post_voting.append(pred_student_teacher)
                        #predictions_post_voting.append(pred_delex_stand_alone)
                        # predictions_post_voting.append(pred_lex_stand_alone)
                        #continue

                        #if all 3 labels dont match, find who has higher confidence score
                        how_many_times_do_all_3_models_disagree_with_each_other+=1
                        sf1_list=convert_sf_string_to_lists(sf1)
                        sf2_list = convert_sf_string_to_lists(sf2)
                        sf3_list = convert_sf_string_to_lists(sf3)
                        highest_confidence_model1=max(sf1_list)
                        highest_confidence_model2 = max(sf2_list)
                        highest_confidence_model3 = max(sf3_list)
                        all_conf=[highest_confidence_model1,highest_confidence_model2,highest_confidence_model3]
                        best=max(all_conf)
                        best_model_index=all_conf.index(best)
                        if (best_model_index == 0):
                            when_all_3_models_disagree_with_each_other_how_many_times_was_combined_model_picked_for_its_high_confidence += 1
                            if (all_preds[best_model_index]) == gold:
                                of_all_times_that_it_was_picked_for_high_confidence_how_many_times_did_combined_match_with_gold += 1

                        if(best_model_index==1):
                            when_all_3_models_disagree_with_each_other_how_many_times_was_delex_stand_alone_model_picked_for_its_high_confidence+=1
                            if(all_preds[best_model_index])==gold:
                                of_all_times_delex_stand_alone_was_picked_how_many_times_delex_stand_alone_matched_with_gold+=1

                        if (best_model_index == 2):
                            when_all_3_models_disagree_with_each_other_how_many_times_was_lex_stand_alone_model_picked_for_its_high_confidence += 1
                            if (all_preds[best_model_index]) == gold:
                                of_all_times_lex_stand_alone_was_picked_how_many_times_lex_stand_alone_matched_with_gold += 1
                        predictions_post_voting.append(all_preds[best_model_index])

    print(
        f"how_many_times_do_all_3_models_disagree_with_each_other={how_many_times_do_all_3_models_disagree_with_each_other}")

    print(f"when_all_3_models_disagree_with_each_other_how_many_times_was_combined_model_picked_for_its_high_confidence={when_all_3_models_disagree_with_each_other_how_many_times_was_combined_model_picked_for_its_high_confidence}")
    print(
        f"when_all_3_models_disagree_with_each_other_how_many_times_was_delex_stand_alone_model_picked_for_its_high_confidence={when_all_3_models_disagree_with_each_other_how_many_times_was_delex_stand_alone_model_picked_for_its_high_confidence}")
    print(
        f"when_all_3_models_disagree_with_each_other_how_many_times_was_lex_stand_alone_model_picked_for_its_high_confidence={when_all_3_models_disagree_with_each_other_how_many_times_was_lex_stand_alone_model_picked_for_its_high_confidence}")
    # print(
    #     f"of_all_times_that_it_was_picked_for_high_confidence_how_many_times_did_combined_match_with_gold={of_all_times_that_it_was_picked_for_high_confidence_how_many_times_did_combined_match_with_gold}")

    return predictions_post_voting


#here we compare with gold and pick if any of it is gold. this is to find how high can we go
def three_model_voting_cieling(model1_predicted_labels, model2_predicted_labels, model3_predicted_labels, gold_labels,model1_softmaxes, model2_softmaxes, model3_softmaxes):
    assert len(model1_predicted_labels) == len(model2_predicted_labels)
    assert len(model1_softmaxes) == len(model2_softmaxes)
    assert len(model1_softmaxes) == len(model3_softmaxes)

    differ_counter=0
    both_match_counter=0
    both_match_gold_counter=0
    predictions_post_voting=[]
    for index,(pred_student_teacher, pred_delex_stand_alone, pred_lex_stand_alone,gold, sf1,sf2, sf3) in enumerate(zip(model1_predicted_labels, model2_predicted_labels, model3_predicted_labels,gold_labels, model1_softmaxes, model2_softmaxes,model3_softmaxes)):
        if (pred_student_teacher==pred_delex_stand_alone==pred_lex_stand_alone):
            predictions_post_voting.append(pred_student_teacher)
        else:
            #if atleast one model matches with gold pick it.
            if (pred_student_teacher == gold) or (pred_delex_stand_alone == gold) or (pred_lex_stand_alone == gold) :
                predictions_post_voting.append(gold)
            else:
                #if no model matchs with gold, just pick one randoimly
                predictions_post_voting.append(pred_student_teacher)

    print(f"differcounter={differ_counter}")
    print(f"both_match_counter={both_match_counter}")
    print(f"both_match_gold_counter={both_match_gold_counter}")

    return predictions_post_voting


def convert_labels_from_string_to_index(label_list):
    return [LABELS.index(label) for label in label_list]


def simple_accuracy(preds, gold):
    total_right=0
    for p,g in zip(preds,gold):
        if(p == g):
            total_right+=1
    return (total_right*100)/len(preds)


predictions_post_voting=two_model_voting(model1_predicted_labels_string, model2_predicted_labels_string, model1_sf, model2_sf,gold_labels)
#predictions_post_voting=three_model_voting_two_model_agrees_but_one_is_lex(delex_model_predicted_labels_string, model2_predicted_labels_string, model3_predicted_labels_string,model1_sf, model2_sf, model3_sf)
#predictions_post_voting=three_model_voting_any_two_models_agree(delex_model_predicted_labels_string, model2_predicted_labels_string, model3_predicted_labels_string, gold_labels,model1_sf, model2_sf, model3_sf)
#predictions_post_voting=three_model_voting_cieling(delex_model_predicted_labels_string, model2_predicted_labels_string, model3_predicted_labels_string, gold_labels,model1_sf, model2_sf, model3_sf)

assert len(predictions_post_voting)==len(gold_labels)
report_score(gold_labels,predictions_post_voting)
pred_labels_int=convert_labels_from_string_to_index(predictions_post_voting)
gold_labels_int=convert_labels_from_string_to_index(gold_labels)
accuracy=simple_accuracy(pred_labels_int, gold_labels_int)
print(f"accuracy={accuracy}")
