import os.path
from collections import defaultdict

# Dictionary
class Dictionary:
    """思考エンジンの辞書クラス。
    クラス変数:
    DICT_RANDOM -- ランダム辞書のファイル名
    DICT_PATTERN -- パターン辞書のファイル名
    スタティックメソッド:
    touch_dics() -- 辞書ファイルにtouch処理を行う
    make_pattern(str) -- パターン辞書読み込み用のヘルパー
    pattern_to_line(pattern) -- パターンハッシュをパターン辞書形式に変換する
    プロパティ:
    random -- ランダム辞書
    pattern -- パターン辞書
    template -- テンプレート辞書
    """

    DICT = {'random': 'dics_random.txt',
            'pattern': 'dics_pattern.txt',
            'template': 'dics_template.txt',
            }

    def __init__(self):
        """ファイルから辞書の読み込みを行う。"""
        Dictionary.touch_dics()
        with open(Dictionary.DICT['random'], encoding='utf-8') as f:
            self._random = [l for l in f.read().splitlines() if l]

        with open(Dictionary.DICT['pattern'], encoding='utf-8') as f:
            self._pattern = [Dictionary.make_pattern(l) for l in f.read().splitlines() if l]

        with open(Dictionary.DICT['template'], encoding='utf-8') as f:
            self._template = defaultdict(lambda: [], {})  # set dict default value to []
            for line in f:
                count, template = line.strip().split()
                if count and template:
                    count = int(count)
                    self._template[count].append(template)

    def study(self, text, parts):
        """ランダム辞書、パターン辞書、テンプレート辞書をメモリに保存する。"""
        self.study_random(text)
        self.study_pattern(text, parts)
        self.study_template(parts)

    def study_template(self, parts):
        """形態素のリストpartsを受け取り、
        名詞のみ'%noun%'に変更した文字列templateをself._templateに追加する。
        名詞が存在しなかった場合、または同じtemplateが存在する場合は何もしない。
        """
        template = ''
        count = 0
        for word, part in parts:
            if morph.is_keyword(part):
                word = '%noun%'
                count += 1
            template += word

        if count > 0 and template not in self._template[count]:
            self._template[count].append(template)

    def study_random(self, text):
        """ユーザーの発言textをランダム辞書に保存する。
        すでに同じ発言があった場合は何もしない。"""
        if not text in self._random:
            self._random.append(text)

    def study_pattern(self, text, parts):
        """ユーザーの発言textを、形態素partsに基づいてパターン辞書に保存する。"""
        for word, part in parts:
            if morph.is_keyword(part):  # 品詞が名詞であれば学習
                # 単語の重複チェック
                # 同じ単語で登録されていれば、パターンを追加する
                # 無ければ新しいパターンを作成する
                duplicated = next((p for p in self._pattern if p['pattern'] == word), None)
                if duplicated:
                    if not text in duplicated['phrases']:
                        duplicated['phrases'].append(text)
                else:
                    self._pattern.append({'pattern': word, 'phrases': [text]})

    def save(self):
        """メモリ上の辞書をファイルに保存する。"""
        with open(Dictionary.DICT['random'], mode='w', encoding='utf-8') as f:
            f.write('\n'.join(self.random))

        with open(Dictionary.DICT['pattern'], mode='w', encoding='utf-8') as f:
            f.write('\n'.join([Dictionary.pattern_to_line(p) for p in self._pattern]))

        with open(Dictionary.DICT['template'], mode='w', encoding='utf-8') as f:
            for count, templates in self._template.items():
                for template in templates:
                    f.write('{}\t{}\n'.format(count, template))

    @staticmethod
    def pattern_to_line(pattern):
        """パターンのハッシュを文字列に変換する。"""
        return '{}/t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))

    @staticmethod
    def make_pattern(line):
        """文字列lineを\tで分割し、{'pattern': [0], 'phrases': [1]}の形式で返す。
        [1]はさらに`|`で分割し、文字列のリストとする。"""
        pattern, phrases = line.split()
        if pattern and phrases:
            return {'pattern': pattern, 'phrases': phrases.split('|')}

    @staticmethod
    def touch_dics():
        """辞書ファイルがなければ空のファイルを作成し、あれば何もしない。"""
        for dic in Dictionary.DICT.values():
            if not os.path.exists(dic):
                open(dic, 'w').close()

    @property
    def random(self):
        """ランダム辞書"""
        return self._random

    @property
    def pattern(self):
        """パターン辞書"""
        return self._pattern

    @property
    def template(self):
        """テンプレート辞書"""
        return self._template

# responder
import re
from random import choice

class Responder:
    """AIの応答を制御する思考エンジンの基底クラス。
    メソッド:
    response(str) -- ユーザーの入力strを受け取り、思考結果を返す
    プロパティ:
    name -- Responderオブジェクトの名前
    """

    def __init__(self, name, dictionary):
        """文字列nameを受け取り、自身のnameに設定する。
        辞書dictionaryを受け取り、自身のdictionaryに保持する。"""
        self._name = name
        self._dictionary = dictionary

    def response(self, *args):
        """文字列を受け取り、思考した結果を返す"""
        pass

    @property
    def name(self):
        """思考エンジンの名前"""
        return self._name


class WhatResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    入力に対して疑問形で聞き返す。"""

    def response(self, text, _):
        """文字列textを受け取り、'{text}ってなに？'という形式で返す。"""
        return '{}ってなに？'.format(text)


class RandomResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録された文字列からランダムなものを返す。
    """

    def response(self, *args):
        """ユーザーからの入力は受け取るが、使用せずにランダムな応答を返す。"""
        return choice(self._dictionary.random)


class PatternResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録されたパターンに反応し、関連する応答を返す。
    """

    def response(self, text, _):
        """ユーザーの入力に合致するパターンがあれば、関連するフレーズを返す。"""
        for ptn in self._dictionary.pattern:
            matcher = re.search(ptn['pattern'], text)
            if matcher:
                chosen_response = choice(ptn['phrases'])
                return chosen_response.replace('%match%', matcher[0])
        return choice(self._dictionary.random)


class TemplateResponder(Responder):
    def response(self, _, parts):
        """形態素解析結果partsに基づいてテンプレートを選択・生成して返す。"""
        keywords = [word for word, part in parts if morph.is_keyword(part)]
        count = len(keywords)
        if count > 0:
            if count in self._dictionary.template:
                template = choice(self._dictionary.template[count])
                for keyword in keywords:
                    template = template.replace('%noun%', keyword, 1)
                return template
        return choice(self._dictionary.random)

# unmo
from random import choice, randrange
from janome.tokenizer import Tokenizer
import morph

class Unmo:
    """人工無脳コアクラス。
    プロパティ:
    name -- 人工無脳コアの名前
    responder_name -- 現在の応答クラスの名前
    """

    def __init__(self, name):
        """文字列を受け取り、コアインスタンスの名前に設定する。
        Responder(What, Random, Pattern)インスタンスを作成し、保持する。
        Dictionaryインスタンスを作成し、保持する。
        Tokenizerインスタンスを作成し、保持する。
        """
        self._tokenizer = Tokenizer()
        self._dictionary = Dictionary()

        self._responders = {
            'what':   WhatResponder('What', self._dictionary),
            'random': RandomResponder('Random', self._dictionary),
            'pattern': PatternResponder('Pattern', self._dictionary),
            'template': TemplateResponder('Template', self._dictionary)
        }
        self._name = name
        self._responder = self._responders['pattern']

    def dialogue(self, text):
        """ユーザーからの入力を受け取り、Responderに処理させた結果を返す。
        呼び出されるたびにランダムでResponderを切り替える。
        入力をDictionaryに学習させる。"""
        chance = randrange(0, 100)
        if chance in range(0, 39):
            self._responder = self._responders['pattern']
        elif chance in range(40, 69):
            self._responder = self._responders['template']
        elif chance in range(70, 89):
            self._responder = self._responders['random']
        else:
            self._responder = self._responders['what']

        parts = morph.analyze(text)
        response = self._responder.response(text, parts)
        self._dictionary.study(text, parts)
        return response

    def save(self):
        """Dictionaryへの保存を行う。"""
        self._dictionary.save()

    @property
    def name(self):
        """人工無脳インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """保持しているResponderの名前"""
        return self._responder.name

# morph
TOKENIZER = Tokenizer()


def analyze(text):
    """文字列textを形態素解析し、[(surface, parts)]の形にして返す。"""
    return [(t.surface, t.part_of_speech) for t in TOKENIZER.tokenize(text)]


def is_keyword(part):
    """品詞partが学習すべきキーワードであるかどうかを真偽値で返す。"""
    return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))

# main

def build_prompt(unmo):
    """AIインスタンスを取り、AIとResponderの名前を整形して返す"""
    return '{name}:{responder}> '.format(name=unmo.name,
                                         responder=unmo.responder_name)


if __name__ == '__main__':
    print('Unmo System prototype : proto')
    proto = Unmo('proto')
    while True:
        text = input('> ')
        if not text:
            break

        try:
            response = proto.dialogue(text)
        except IndexError as error:
            print('{}: {}'.format(type(error).__name__, str(error)))
            print('警告: 辞書が空です。(Responder: {})'.format(proto.responder_name))
        else:
            print('{prompt}{response}'.format(prompt=build_prompt(proto),
                                              response=response))
    proto.save()
