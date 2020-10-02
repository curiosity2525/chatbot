import sys
import re
import libmstdn
import os
import MeCab
import io
from sys import argv
from math import log
from glob import glob
from time import sleep

#Mastdonホスト
MASTODON_HOST = "Mastdonホスト名"
#MastodonAPIアクセストークン
ACCESS_TOKEN = "アクセストークン"

documents_path = ["パス"]
doc = "パス"

mecab = MeCab.Tagger("-Ochasen")


#ドキュメントの総数をカウント
def count_docs():
    cnt = 0
    for i in documents_path:
        cnt += len(glob("" + i + "*")) #ファイル一覧を取得
    return cnt

#wordが含まれるドキュメント数をカウント
def count_pop_docs(word):
    cnt = 0
    for path in documents_path:
        for i in glob(path + "*"):
            #print(i)
            text = open(i, encoding="shift-jis").read()
            if count_nown(text, word)[0] > 0:
                cnt += 1
    return cnt

#text内でwordが出現する回数をカウント
def count_nown(text, word):
    nown_cnt = 0
    word_cnt = 0
    node = mecab.parseToNode(text)
    while node.next:
        node = node.next
        if node.feature.split(",")[0] == "名詞":
            nown_cnt += 1
            if node.surface == word:
                word_cnt += 1
    return word_cnt, nown_cnt

#tfスコアを計算
def get_tf(doc, word):
    text = open(doc, encoding = "shift-jis").read()
    word_cnt, nown_cnt = count_nown(text, word)
    return 1.0*word_cnt / nown_cnt

#idfスコアを計算
def get_idf(word):
    word_pop_count = count_pop_docs(word)
    number = count_docs()
    return log(1.0 * number / word_pop_count)

#tf-idfスコアを計算
def get_tfidf(doc, word):
    tf = get_tf(doc, word)
    idf = get_idf(word)
    return 1.0*tf*idf

#文字列内のHTMLタグを削除
def remove_html_tags(content):

    return re.sub("<[^>]*>", "", content).strip()

def is_to_me(status, my_id):

    for mention in status["mentions"]:
        if mention["id" ] == my_id:
            return True
    return False

def is_to_some(status, some_id):
    for mention in status["mentions"]:
        if mention["id" ] == some_id:
            return True
    return False


def generate_reply(status, my_name):
    print("status =" + str(status))
    #print("status[content] = " + str(status["content"]))

    received_text = remove_html_tags(status["content"])
    toot_from = status["account"]["username"]


    if "こんにちは" in received_text:
        return toot_from + "さん、こんにちは! \n 単語をつぶやいたら該当する江戸川乱歩の少年探偵団シリーズの作品名と要約を返します"

    elif "江戸川乱歩" in received_text:
        makeText_path = "パス"
        with io.open(makeText_path, encoding='utf-8-sig') as mt_f:
            return mt_f.read(200) + "・・・"
                 


    else:
        received_context = received_text.replace("@ボットのアカウント名 ","")
        #word_list = received_context.split(" ")
        print(received_context)
        word = received_context
        result2 = {}
        print("全" + str(count_docs()) + "ドキュメントの中，「" + word + "」は" + str(count_pop_docs(word)) + "個数存在")
        for path in documents_path:
            for doc in glob(path + "*"):
                score = get_tfidf(doc, word)
                print("" + doc + "の" + word + "のTF-IDFスコアは" + str(score) + "です")
                if score > 0:
                    result2[doc] = score
        print("\n")
        print("検索結果")
        count = 0
        summary_text = ""
        for k, v in sorted(result2.items(), key = lambda x:x[1], reverse = True):
            if(count == 0):
                if(k == "/Users/user名/Desktop/江戸川乱歩/seidono_majin.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data001_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「青銅の魔神」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/denjin_emu.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data002_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「電人M」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/haiirono_kyojin.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data003_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「灰色の巨人」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/kaiki_yonju_menso.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data004_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「怪奇四十面相」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/kaijin_nijumenso.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data005_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「怪人二十面相」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/kaiteino_majutsushi.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data006_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「海底の魔術師」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/kimenjono_himitsu.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data007_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「奇面城の秘密」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/maho_hakase.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data008_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「魔法博士」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/ogon_hyo.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data009_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「黄金豹」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/shonen_tanteidan.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data010_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「少年探偵団」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/tetsujin_kyu.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data011_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「鉄人Q」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/tettono_kaijin.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data012_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「鉄塔の怪人」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/tomei_kaijin.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data013_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「透明怪人」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/uchu_kaijin.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data014_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「宇宙怪人」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/yako_ningen.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data015_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「夜光人間」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/yojin_gongu.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data016_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「魔人ゴング」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/dai_kinkai.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data017_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「大金塊」ではありませんか？" + summary_text

                elif(k == "/Users/user名/Desktop/江戸川乱歩/kamenno_kyouhu.txt"):
                    summary_path = '/Users/user名/Desktop/edogawa/5回目/data002_out.txt'
                    with io.open(summary_path, encoding='utf-8-sig') as s_f:
                        summary_text = s_f.read()
                    return "それは「仮面の恐怖」ではありませんか？" + summary_text
                
                else:
                    return "すみません，そのキーワードでは見つかりません"

            count += 1
            print(k + " : " + str(v))

        return received_context

def main():
    api = libmstdn.MastodonAPI(
        mastodon_host = MASTODON_HOST,
        access_token = ACCESS_TOKEN)

    account_info = api.verify_account()
    my_id = account_info["id"]
    my_name = account_info["username"]
    print("Started bot, name: {}, id: {}".format(my_name, my_id))

    stream = api.get_user_stream()

    for status in stream:
        print("hello")
        if is_to_me(status, my_id):
            print("is_to_me")
            
            received_text = remove_html_tags(status["content"])
            toot_id = status["id"]
            toot_from = status["account"]["username"]
            print("received from {}:{}".format(toot_from, received_text))
            reply_text = "@{} {}".format(
                                         toot_from, generate_reply(status, my_name))
            api.toot(reply_text, toot_id)
            sleep(10)
            print("post to {}:{}".format(toot_from, reply_text))
            
    return 0

if __name__ == "__main__":
    sys.exit(main())

