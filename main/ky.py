# coding: utf-8
from urllib import request
from bs4 import BeautifulSoup
import bs4
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# spacyのロード
nlp = spacy.load('ja_ginza_nopn')

# urlに要約対象とする書籍のURLを指定します。以下は「だしの取り方 by 北大路魯山人」のURLです。
url = 'https://www.aozora.gr.jp/cards/001403/files/49986_37674.html'
html = request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
body = soup.select('.main_text')

text = ''
for b in body[0]:
    if type(b) == bs4.element.NavigableString:
        text += b
        continue
    # ルビの場合、フリガナは対象にせずに、漢字のみ使用します。
    text += ''.join([e.text for e in b.find_all('rb')])

# 分析用コーパスではレンマ化
corpus = []
originals = []
doc = nlp(text)
for s in doc.sents:
    originals.append(s)
    tokens = []
    for t in s:
        tokens.append(t.lemma_)
    corpus.append(' '.join(tokens))

print(len(corpus))
print(len(originals))

# 連結したcorpusを再度tinysegmenterでトークナイズさせる
parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

summarizer = LexRankSummarizer()
summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する

# sentencres_countに要約後の文の数を指定します。
summary = summarizer(document=parser.document, sentences_count=3)

# 元の文を表示
for sentence in summary:
    print(originals[corpus.index(sentence.__str__())])