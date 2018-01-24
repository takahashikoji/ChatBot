from random import choice
class RandomResponder:
    """AIの応答を制御する思考エンジンクラス。
    登録された文字列からランダムなものを返す。

    クラス変数:
    RESPONSES -- 応答する文字列のリスト

    プロパティ:
    name -- RandomResponderオブジェクトの名前
    """

    RESPONSES = ['今日はさむいね', 'チョコたべたい', 'きのう10円ひろった']

    def __init__(self, name):
        """文字列を受け取り、自身のnameに設定する。"""
        self._name = name

    def response(self, _):
        """ユーザーからの入力は受け取るが、使用せずにランダムな応答を返す。"""
        return choice(RandomResponder.RESPONSES)

    @property
    def name(self):
        """思考エンジンの名前"""
        return self._name


class Responder:
    """AIの応答を制御するクラス。

    プロパティ:
    name -- Responderオブジェクトの名前
    """

    def __init__(self, name):
        """文字列を受け取り、自身のnameに設定する。"""
        self._name = name
        self._test = 'test'

    def response(self, text):
        """ユーザーからの入力(text)を受け取り、AIの応答を生成して返す。"""
        return '{}ってなに？'.format(text)

    @property
    def name(self):
        """応答オブジェクトの名前"""
        return self._name
# uomo.py

class Unmo:
    """人工無脳コアクラス。

    プロパティ:
    name -- 人工無脳コアの名前
    responder_name -- 現在の応答クラスの名前
    """

    def __init__(self, name):
        """文字列を受け取り、コアインスタンスの名前に設定する。
        ’What' Responderインスタンスを作成し、保持する。
        """
        self._name = name
        self._responder = RandomResponder('What')

    def dialogue(self, text):
        """ユーザーからの入力を受け取り、Responderに処理させた結果を返す。"""
        return self._responder.response(text)

    @property
    def name(self):
        """人工無脳インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """保持しているResponderの名前"""
        return self._responder.name

# responder.py


# main.py

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

        response = proto.dialogue(text)
        print('{prompt}{response}'.format(prompt=build_prompt(proto),
                                          response=response))
