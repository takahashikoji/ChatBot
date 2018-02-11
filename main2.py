from unmo import Unmo
from rulebased import Rulebase


def build_prompt(unmo):
    """AIインスタンスを取り、AIとResponderの名前を整形して返す"""
    return '{name}:{responder}> '.format(name=unmo.name,
                                         responder=unmo.responder_name)


if __name__ == '__main__':
    print('Unmo System prototype : proto')
    proto = Unmo('manachan')


    markov_training = 0
    while True:
        if markov_training==1:
            markov_tr_list = markov_tr_list[1:]
            if len(markov_tr_list)==0:
                markov_training = 0
                print('markov training is done!')
            else:
                text = markov_tr_list[0]
                print('traiing :',text)

        if markov_training!=1:
            text = input('> ')

        if text=='tm':
            markov_tr_list = []
            print('ファイル名を教えて下さい')
            path = open(input('file_name='),'r')
            strings = path.read()
            markov_training = 1
            dst = strings.replace('/n', ',')
            markov_tr_list += dst.split(',')
            print('markov_tr_list',markov_tr_list)
            text = markov_tr_list[0]
            print('traiing :',text)

        if text=='勉強する':
            rulebase = Rulebase()
            rulebase.rule_response()

        if not text:
            break

        try:
            response = proto.dialogue(text, markov_training)
        except IndexError as error:
            print('{}: {}'.format(type(error).__name__, str(error)))
            print('警告: 辞書が空です。(Responder: {})'.format(proto.responder_name))
        else:
            print('{prompt}{response}'.format(prompt=build_prompt(proto),
                                              response=response))
    proto.save()
