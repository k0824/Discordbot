from collections import OrderedDict

'''
    if name == '' or name == '':
        __info = ['', '', '歳', '', 'cm', 'kg', '', '月日', '座', '型', '',
                  '', '', '']
'''

def info(name):
    item = ['名前', 'タイプ', '年齢', '学年', '身長', '体重', 'B-W-H', '誕生日', '星座', '血液型', '利き手', '出身地', '趣味', 'CV']
    ret = OrderedDict()
    if name == '相川千夏' or name == 'あいかわちなつ':
        __info = ['相川千夏', 'Cool', '23歳', None, '161cm', '43kg', '82-56-85', '11月11日', '蠍座', 'B型', '右',
                  '北海道', 'カフェで読書', None]
    elif name == '橘ありす' or name == 'たちばなありす':
        __info = ['橘ありす', 'Cool', '12歳', '小学6年生', '141cm', '34kg', '68-52-67', '7月31日', '獅子座', 'A型', '右',
                  '兵庫県', 'ゲーム・読書', '佐藤亜美菜']
    else:
        ret['入力した名前は名簿に登録されていません'] = 'フルネームを正確に、漢字またはひらがなで入力してください。'
        return ret
    for a in item:
        ret[a] = __info[item.index(a)]
    return ret
