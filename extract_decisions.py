# for checking the case that the decision is extracted from the "title"

import os
import re
import html
import json
import codecs
import nltk
nltk.download('all')

from collections import Counter
from nltk.tokenize import sent_tokenize

from datetime import datetime

speaker_king_or_not_words_file = 'data/categorized_words_speakers.txt'
way_decision_filename = 'data/categorized_words_decisions.txt'

speakers_set = set()
len_last_words = 10

chi_said_pattern = re.compile(r'(.{1})曰:(.+)', re.DOTALL)
kor_path_to_chi_path_pattern = re.compile(r'^k', re.DOTALL)
kor_quote_pattern = re.compile(r'(.*?)&ldquo;(.+?)&rdquo;', re.DOTALL)
kor_quote_pattern2 = re.compile(r'&ldquo;(.+?)&rdquo;', re.DOTALL)
king_kor_word = "임금이"
king_kor_word2 = "상이"
king_kor_word3 = "왕이"


def load_quote_in_rule():
    word_speaker_rule = dict()

    with codecs.open(speaker_king_or_not_words_file, "r", "utf-8") as f:
        next(f) # skip header
        for line in f:
            line_arr = line.strip().split('\t')
            last_word_pattern = re.compile("{}[?.!]?$".format(line_arr[0]))
            word_speaker_rule[last_word_pattern] = int(line_arr[1])

    return word_speaker_rule # {last_word_pattern: 1(king) or 0(not king)}


def normalize_body_sentences(kor_body):
    kor_body = re.sub("[\r\n\t]", " ", kor_body)
    kor_body = re.sub("&.+?;", " ", kor_body)
    kor_body = re.sub("\\(.+?\\)", "", kor_body)
    kor_body = re.sub("\\[.+?\\]", "", kor_body)
    kor_body = re.sub(",", "", kor_body)
    kor_body = re.sub("【", " ", kor_body)
    kor_body = re.sub("】", " ", kor_body)
    kor_body = re.sub("〉", " ", kor_body)
    kor_body = re.sub("〈", " ", kor_body)
    kor_body = re.sub("《", " ", kor_body)
    kor_body = re.sub("》", " ", kor_body)
    kor_body = re.sub("「", " ", kor_body)
    kor_body = re.sub("」", " ", kor_body)

    kor_body = re.sub("<font[^>]*?>(.*?)</font>", '\g<1>', kor_body)
    kor_body = re.sub("<font[^>]*?>(.*?)</font>", '\g<1>', kor_body)

    kor_body = re.sub("<[^>]+?>(.*?)</[^>]+?>", '\g<1>', kor_body)

    kor_body = html.unescape(kor_body)

    return kor_body


def filter_document(body_str):
    body_str = re.sub("[\r\n\t]", " ", body_str)
    body_str = re.sub("&.+?;", " ", body_str)
    body_str = re.sub("\\(.+?\\)", "", body_str)
    body_str = re.sub("\\[.+?\\]", "", body_str)
    body_str = re.sub(",", "", body_str)
    body_str = re.sub("【", " ", body_str)
    body_str = re.sub("】", " ", body_str)
    body_str = re.sub("〉", " ", body_str)
    body_str = re.sub("〈", " ", body_str)
    body_str = re.sub("《", " ", body_str)
    body_str = re.sub("》", " ", body_str)
    body_str = re.sub("「", " ", body_str)
    body_str = re.sub("」", " ", body_str)

    body_str = re.sub("<font[^>]*?>(.*?)</font>", r"\1", body_str)
    body_str = re.sub("<font[^>]*?>(.*?)</font>", r"\1", body_str)

    body_str = re.sub("<[^>]+?>(.*?)</[^>]+?>", r"\1", body_str)

    return body_str


def read_words_decisions():
    way_word_decision = dict()

    with codecs.open(way_decision_filename, "r", "utf-8") as f:
        f.readline()

        for line in f:
            line_arr = line.strip().split('\t')
            decision = int(line_arr[0])
            way = int(line_arr[1])
            word = line_arr[2]

            try:
                word_decision_dict = way_word_decision[way]
            except KeyError:
                way_word_decision[way] = dict()
                word_decision_dict = way_word_decision[way]
            if way == 10:
                last_word_pattern = re.compile("{}[?.!]?$".format(word))
                word_decision_dict[last_word_pattern] = decision
            else:
                word_decision_dict[word] = decision

    return way_word_decision


def classify_king_or_not_quote_in(word_speaker_rule, last_words):
    candidate_speaker = None
    for word_pattern, speaker_tag in word_speaker_rule.items():
        if word_pattern.search(last_words) is not None:
            candidate_speaker = speaker_tag
    return candidate_speaker


def identify_speaker_each_quote(kor_body, word_speaker_rule):
    quote_results = kor_quote_pattern.findall(kor_body)
    speaker_list = list()

    for quote_pre, quote_in in quote_results:
        quote_pre_sentences = sent_tokenize(quote_pre)
        quote_in_sentences = sent_tokenize(quote_in)

        classified_speaker_list = list()
        for sentence_quote_in in quote_in_sentences:
            sentence_quote_in = sentence_quote_in.strip()
            last_words = sentence_quote_in[-min(len(sentence_quote_in), len_last_words):]
            classified_speaker_list.append(classify_king_or_not_quote_in(word_speaker_rule, last_words))
        classified_speaker_set = set(classified_speaker_list)

        try:
            classified_speaker_set.remove(None)
        except KeyError:
            pass

        if len(classified_speaker_set) == 1:
            classified_speaker_final_v1 = list(classified_speaker_set)[0]
        else:
            count_classified_speaker_list = Counter(classified_speaker_list)
            if count_classified_speaker_list[0] == 0 and count_classified_speaker_list[1] == 0:
                classified_speaker_final_v1 = None
            else:
                if count_classified_speaker_list[0] > count_classified_speaker_list[1]:
                    classified_speaker_final_v1 = 0
                elif count_classified_speaker_list[0] < count_classified_speaker_list[1]:
                    classified_speaker_final_v1 = 1
                else:
                    classified_speaker_final_v1 = None

        classified_speaker_final_v2 = classified_speaker_list[-1] # important - last sentence

        if classified_speaker_final_v2 is not None:
            classified_speaker_final = classified_speaker_final_v2
        else:
            classified_speaker_final = classified_speaker_final_v1

        try:
            quote_pre_last_sentence = quote_pre_sentences[-1]
            if len(quote_pre_sentences) >= 2:
                quote_pre_last_prev_sentence = quote_pre_sentences[-2]
            else:
                quote_pre_last_prev_sentence = None
        except IndexError: # if continue, speaker_list & quote_results length is not same
            quote_pre_last_sentence = None
            quote_pre_last_prev_sentence = None

        if quote_pre_last_sentence is not None:
            quote_pre_last_sent_king_kor = king_kor_word in quote_pre_last_sentence or king_kor_word2 in quote_pre_last_sentence or king_kor_word3 in quote_pre_last_sentence
        else:
            quote_pre_last_sent_king_kor = False

        if quote_pre_last_prev_sentence is not None:
            quote_pre_last_prev_sent_king_kor = king_kor_word in quote_pre_last_prev_sentence or king_kor_word2 in quote_pre_last_prev_sentence or king_kor_word3 in quote_pre_last_prev_sentence
        else:
            quote_pre_last_prev_sent_king_kor = False

        if classified_speaker_final == 1 or quote_pre_last_sent_king_kor or quote_pre_last_prev_sent_king_kor:
            speaker_list.append(True) # king
        else:
            speaker_list.append(False) # not king (officials, ...)

    return speaker_list, quote_results


def identify_decision_by_words_in_quote(kor_body, word_speaker_rule, target_words_rule):
    speaker_list, quote_results = identify_speaker_each_quote(kor_body, word_speaker_rule)
    candidate_category_list = list()

    for speaker, quote_result in zip(speaker_list, quote_results):
        quote_pre, quote_in = quote_result

        if speaker: # if king
            quote_in = quote_in.strip()
            last_words = quote_in[-min(len(quote_in), len_last_words):]

            for word_pattern, category_tag in target_words_rule.items():
                if word_pattern.search(last_words) is not None:
                    candidate_category_list.append(category_tag)

    # quote에 대해서만!
    # 명령이 상당히 많기에 만약 명령이 아닌 것이 하나라도 나오면 명령을 제거하자
    # -> 즉, order only가 아닌 경우를 여기서 거르는 것
    if 1 in candidate_category_list or 2 in candidate_category_list:
        candidate_count = Counter(candidate_category_list)
        candidate_category_list = list()
        for _ in range(candidate_count[1]):
            candidate_category_list.append(1)
        for _ in range(candidate_count[2]):
            candidate_category_list.append(2)

    return candidate_category_list, len(speaker_list)


def identify_decision_by_words_kor_title(kor_title, target_words):
    kor_title = html.unescape(kor_title)
    candidate_list = list()

    for target_word, target_decision in target_words.items():
        if target_word in kor_title:
            candidate_list.append(target_decision)

    return candidate_list


def kor_body_without_quote(kor_body):
    kor_body = re.sub(kor_quote_pattern2, '', kor_body)
    return kor_body


def identify_decision_by_words_kor_body(kor_body, target_words_list):
    candidate_list = list()
    only_kor_body = kor_body_without_quote(kor_body)

    if len(only_kor_body) > 0:
        for target_words in target_words_list:
            for target_word, target_decision in target_words.items():
                if target_word in only_kor_body:
                    candidate_list.append(target_decision)

    return candidate_list


def convert_from_kor_path_to_chi_path(kor_filename):
    return kor_path_to_chi_path_pattern.sub('w', kor_filename)


def identify_decision_by_words_chi_body(chi_body, target_words, target_words_said_list):
    chi_body_sentences = list(filter(lambda x: len(x) > 0, chi_body.split("。")))
    last_sentence = chi_body_sentences[-1]
    # tokens = sft.tokenize(last_sentence)

    candidate_list = list()
    for target_word, target_decision in target_words.items():
        if target_word in last_sentence:
            candidate_list.append(target_decision)

    # Said pattern
    said_results = chi_said_pattern.findall(last_sentence)
    for said_whom, said_what in said_results:
        said_whom = said_whom.strip()
        said_what = said_what.strip()

        for target_word, target_decision in target_words_said_list[0].items():
            if target_word in said_whom: # 傳曰
                candidate_list.append(target_decision)

        for target_word, target_decision in target_words_said_list[1].items():
            if target_word in said_what:
                candidate_list.append(target_decision)

    return candidate_list


def filter_discussion_docs(kor_files_content, chi_files_content, way_word_decision, word_speaker_rule):
    return_list = list()

    for each_kor_doc_name, each_kor_doc_content in sorted(kor_files_content.items(), key=lambda x: x[0]):
        each_chi_doc_name = convert_from_kor_path_to_chi_path(each_kor_doc_name)
        each_chi_doc_content = chi_files_content[each_chi_doc_name]

        kor_title = html.unescape(each_kor_doc_content[0])
        kor_body = " ".join(each_kor_doc_content[1])

        try:
            final_cue = 'title'
            identify_decision_by_words_in_quote(kor_body, word_speaker_rule, way_word_decision[10])
            candidate_list = list()

            temp = identify_decision_by_words_kor_title(kor_title, way_word_decision[0])
            if temp == []:
                final_cue = 'body'
                temp = identify_decision_by_words_kor_body(kor_body, (way_word_decision[1], way_word_decision[2]))
            
            if temp != []:
                candidate_list += temp
            else:
                final_cue = 'vote'

            if final_cue == 'vote' and each_chi_doc_content is not None:
                chi_body = " ".join(each_chi_doc_content[1])
                chi_body_norm = normalize_body_sentences(chi_body)
                temp = identify_decision_by_words_chi_body(chi_body_norm, way_word_decision[3], (way_word_decision[4], way_word_decision[5]))
                candidate_list += temp

            # 추가
            # 본문에 quotation 이 있을 때만 확인
            if '&ldquo;' in kor_body:
                candidate_from_quote, num_quote = identify_decision_by_words_in_quote(kor_body, word_speaker_rule, way_word_decision[10])
                if final_cue == 'vote':
                    candidate_list += candidate_from_quote
            else:
                candidate_from_quote = []
                num_quote = 0

            # title 인 경우, 제목에 명확히 드러난 경우
            if final_cue == 'title':
                max_candidate = candidate_list[0]
                candidate_list = [max_candidate]
            else: # body 나 vote 인 경우, 한문 본문과 한글 인용절에서 vote 가 필요한 경우 
                candidate = set(candidate_list)
                if len(candidate) == 1:
                    max_candidate = candidate_list[0]
                elif len(candidate) > 1:
                    most_common_candidates = Counter(candidate_list).most_common()
                    max_count = most_common_candidates[0][1]
                    most_common_max = [(item, count) for item, count in most_common_candidates if count == max_count]

                    if len(most_common_max) == 1:
                        max_candidate = most_common_max[0][0]
                    elif len(most_common_max) == 2 and most_common_max[1][0] == 1 and num_quote > 1:
                        max_candidate = 1 # 0, 1 이 동점이고 인용절이 2개 이상일 때는 1이 더 우선됨
                    else: # 대략 10만개의 결정 중 단 50개? 정도만이 동점에 해당하므로 그냥 무시
                        max_candidate = '동점'
                        # continue
                else: # 해당 문서에서 왕의 결정을 찾아볼 수 없음
                    continue

            return_list.append((each_kor_doc_name, len(candidate_list), max_candidate, candidate_from_quote, candidate_list, 'title' if final_cue == 'title' else 'vague'))

            # if len(candidate_list) > 0:
            #     candidate_count = Counter(candidate_list)
            #     max_candidate = sorted(candidate_count.items(), key=lambda x: x[1], reverse=True)[0][0]

            #     if max_candidate == 0 and num_quote > 1: # 0 = order only, 1 = agreement, 2 = disagreement, 3 = order + discussion (same with 1)
            #         max_candidate = 3
            # else:
            #     continue
            
        except IndexError:
            print("Index Error in filter_discussion_docs function with {}".format(each_kor_doc_name), file=error_f)
            continue

    return return_list

if __name__ == "__main__":
    way_word_decision = read_words_decisions()
    word_speaker_rule = load_quote_in_rule()

    kor_root_path = "data/pp_kor_docs_json/"
    chi_root_path = "data/pp_chi_docs_json/"

    king_code_name_file = "../data/king_code_name.txt"
    king_code = list()
    with codecs.open(king_code_name_file, "r", "utf-8") as f:
        for line in f:
            line_arr = line.strip().split("\t")
            king_code.append(line_arr[0])
    king_code = set(king_code[:-2])

    error_f = codecs.open("error.txt", "w", "utf-8")

    today_date = datetime.now().strftime("%Y-%m-%d")

    # max_count_candidate means the 'final decision' of the document
    with codecs.open(f"{today_date}_classification_result.csv", "w", "utf-8") as output_f:
        print("document_code,len_candidates,max_count_candidate,candidate_from_quote,candidates,title_or_not", file=output_f)
        
        for root, dirs, files in os.walk(kor_root_path):
            for one_file in sorted(files):
                if ".json" in one_file:
                        print("Do {}".format(one_file))

                        with codecs.open(os.path.join(root, one_file), "r", "utf-8") as kor_json_f:
                            kor_files_content = json.load(kor_json_f)
                            chi_file_path = os.path.join(chi_root_path, convert_from_kor_path_to_chi_path(one_file))

                            with codecs.open(chi_file_path, "r", "utf-8") as chi_json_f:
                                chi_files_content = json.load(chi_json_f)
                                
                                output_list = filter_discussion_docs(kor_files_content, chi_files_content, way_word_decision, word_speaker_rule)

                                for one_doc in output_list:
                                    print(",".join([str(x) for x in one_doc]), file=output_f)
    error_f.close()
