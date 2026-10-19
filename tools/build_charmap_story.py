#!/usr/bin/env python3
"""Build data/bigfont_charmap.json entries from verified message readings.

Each expected string is the exact on-screen text of a story message with
control codes removed (control codes are skipped by the same parser used
by render_story.split_screens).  Glyph tokens and expected characters are
zipped; any length mismatch is reported so the reading can be fixed.

Usage: python tools/build_charmap_story.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from render_story import split_screens, tokens  # noqa: E402

RAW = os.path.join(ROOT, "build", "story_messages_raw.json")
RAW_LATE = os.path.join(ROOT, "build", "late_story_raw.json")
CHARMAP = os.path.join(ROOT, "data", "bigfont_charmap.json")

# Full on-screen text per message (controls omitted).  Only verified
# readings belong here.  Fullwidth digits are used where the store has
# fullwidth glyphs (0x1E = ２).
READINGS = {
    0: "神のいない世界に、繁栄などは無いだから私が使わされた。",
    1: "暗黒の時代グランデート大陸は常に人類の危機と共に存在していた。永遠の命を持つといわれた、巨大な２匹のハイドラゴンが大陸の権力を、掌握していた",
    2: "空を支配していた、天空のカノン",
    3: "地上を支配していた、大地のイグニス",
    4: "２匹は互いに対峙し、大陸を征服しようと、血塗られた戦争をくり広げていた。",
    5: "長き戦いの末、この大陸全ての生命と、繁栄が消え去ろうとしたとき・・・"
       "見たことも無い二匹の魔獣を引き連れた、一人の魔術使いが現れ、"
       "２匹に戦いを挑んだ！",
    6: "長く壮絶な戦いが繰り広げられ・・・",
    7: "天空のカノンは敗れ、傷を負った大地のイグニスは、"
       "ファムファンタル火山の地下深く、姿を隠したのであった。",
    8: "その勝利は、二匹の魔獣の命と、引き換えに勝ち取った。"
       "そして魔獣使い自身もまた、力尽きようとしていた。"
       "その時、この魔獣使いを救える技術を持つ者は私以外、"
       "この世界には居なかった。",
    9: "その後この魔獣使いと、二匹の魔獣は伝説の魔獣使いとして"
       "人々に伝えられた。そしてグランデート大陸は、"
       "人類が支配者となった。",
    10: "～ファムファンタル火山～その男は、いまだ盛んに"
        "噴煙を上げる、火口にいた。",
    11: "火口にはイグニスを祭ったと思われる、廃墟が残っていた。"
        "男「どうした！大地のイグニスよ！」",
    12: "男「このタクトを見て思い出さないのか？」"
        "男「おまえを世界から追いやった伝説の魔獣使いのタクトだ！」"
        "男「今再びよみがえりヤツに、いやこの世界に共に、"
        "復讐しようではないか！！」",
    13: "男「・・・」男「これだけではまだ弱いか！"
        "やはりヤツを・・・」そのとき男は足元の地中深くから、"
        "何かがうごめくのを感じとっていた。",
    14: "～廃墟～朝もやの中、人里離れた廃墟から、男達の声が"
        "聞こえた！追っ手１「見つけ出すぞ！」追っ手２「逃がすな！！」",
    15: "それは、バルロア王国配下の衛兵達であった。"
        "追っ手３「もう逃がさんぞ！」追っ手２「えーと・・・"
        "こいつの名前は？」",
    16: "追っ手３「あ、そうだ！」追っ手１「だった！」"
        "追っ手２「かくごしろ！！おまえを捕まえてベリンガム様に"
        "渡せば謝礼がたんまりと・・・」そういって追っ手達がに"
        "手をかけようとしたその時！",
    17: "背後から魔獣達が突然、追っ手達におそいかかった！",
    18: "追っ手達「うわぁ！！」は唖然として、事の成り行きを見ていた。",
    19: "追っ手達はあっというまに倒されたすると、となりの部屋から"
        "一人の老人が現れた。",
    20: "老人「やかましいのう！わしゃ寝起きは機嫌がわるいんじゃ！」",
    21: "その老人はクリムトと名乗った。クリムト「いや、"
        "助けたのはベリンガムと言う名を聞いてな。"
        "やつとは少々ワケありでの・・・うーん、そなたはヴァンダム城の"
        "ウィンスローのとみたが・・城でなにかあったかの？」",
    22: "は昨日に起こった事件をクリムトに語り始めた。",
    23: "～バルロア王国、ヴァンダム城～",
    24: "城主は、貴族の一人ウィンスロー二世事件は小雨の降る朝に、"
        "突然起こった。",
    25: "法王直属の魔獣騎士団が城に乱入！城を占拠した。"
        "首謀者は、法王の軍事顧問として仕えてきたベリンガム・ロー公爵。"
        "彼は魔獣騎士団の最高司令官でもある男だ。"
        "彼は城占拠の理由を、王国に対立する組織へ協力した疑い！"
        "と、示したがまったくの濡れ衣であった。",
    26: "捜索の邪魔をするものは、容赦なく捕らえられ、"
        "その混乱の中が見たものは、自分の目前ですでに息絶えている、"
        "父ウィンスローの姿であった。",
    27: "そこには、見覚えの無い魔獣使いのタクトを手にしている"
        "ベリンガムの姿があった。",
    28: "クリムト「・・・」クリムト「伝説の魔獣使いのタクトが目的か？"
        "いや・・・なんでもない。それよりおぬし・・・"
        "父や家族の仇をとるつもりか？"
        "何も言わんでもその目が語っとるわい！」",
    29: "そう言うと、クリムトは自分のタクトをに手渡した。",
    30: "クリムト「わしの魔獣達をおぬしにあずけよう。"
        "しばらくこの廃墟をねぐらにして訓練するがよいぞ！」",
    31: "クリムト「よいか、ベリンガム達と戦うには、"
        "この魔獣達では力不足じゃ！"
        "そこで伝説の魔獣使いがつれていた伝説の魔獣を作るんじゃ！",
    32: "クリムト「ワシはその研究しておった。"
        "まだ一部しか解っておらんがの・・・」"
        "クリムト「ワシの調べでは、最初はとを合成すると、"
        "の幼体が出来るはずじゃ！」",
    33: "クリムト「わしは再びその後の魔獣の作り方を調べる！」"
        "クリムト「後はまかせたぞ！」",
    34: "そう言い残してクリムトは何処かへ旅立って行った。"
        "その後ろ姿を見ては思った。",
    35: "クリムト老人は、こうなる事を知っていたのではないだろうかと・・・",
    36: "ゴゴゴゴゴ！が祭壇のある部屋に入った時、"
        "大きく城がゆれはじめた。「地震？」",
    37: "地震に気をとられていたの目前に、"
        "見たことも無い大男が立っていた。"
        "彼はをにらみつけながら近づいてきた。",
    38: "ベリンガム「わかるかね！この地震はイグニスが君に気づきはじめて、"
        "地下で暴れているのだよ！」"
        "声のする方向にはベリンガムの姿があった。",
    39: "はベリンガムに向けて、タクトを振りかざそうとしたその時"
        "クリムト「気をつけろ！ヤツの作った魔獣ザーゴに狙われておるぞ！」"
        "いつのまにか背後にクリムトの姿があった。"
        "クリムト「よくここまで来れたのう。」",
    40: "ベリンガム「フフフ・・・やはりクリムトが裏に付いていたか！"
        "だがすでに遅いな！」"
        "その時、再び地面が激しくゆれ始めた！",
    41: "ベリンガム「の存在に気が付いたイグニスが、再び復活しようとしておる！"
        "ザーゴ！あとは任せるゾ！わしはファムファンタル火山へ行き、"
        "君の古い友人に会ってくるよ。」そういい残し、"
        "ベリンガムは部屋を出て行った。そして、ザーゴはゆっくりとに"
        "近づいてきた・・・",
    42: "ザーゴ「グゥゥゥゥッ！」ザーゴが唸り声を上げ、"
        "ヒザをついて倒れこんだ！",
    43: "その時、上空からベリンガムのもう一人の魔獣ラミレスが現れた！",
    44: "ラミレスはザーゴの前に立ち、に告げた！"
        "ラミレス「自分・・・事・・・しりたいか・・・？"
        "ならば・・・ファムファンタル火山に行け・・・」"
        "そう言い残してザーゴを抱え込み飛び立っていった",
    45: "クリムト「これも運命かの・・・こうなったら行くしかないぞ。"
        "ファムファンタル火山へ・・・！"
        "そこでおぬしの全てが解るはずじゃ！」",
    46: "クリムト「よいか、それまでに伝説の魔獣の中型体を完成させるのじゃ！"
        "次はとを合成する。さすれば、の中型体が完成するはずじゃ！」",
    47: "クリムト「ワシはまた、伝説の魔獣の事をしらべに旅に出る。"
        "火山までの道のりは至難を極めるぞ！！」"
        "そういい残し、クリムトは去って行った。",
    48: "がファムファンタル火山を登り始めてから"
        "数え切れないほどの地震が起きていた。は感じた。"
        "この揺れはイグニスが地底で暴れている",
    49: "と突然、ベリンガムの魔獣ザーゴとラミレスが現れた。"
        "ザーゴ「もっと・・・戦え！」"
        "ラミレス「たくさん・・・戦えば、イグニス・・・怒る！」"
        "は体の中から狂暴な力がみなぎるのを感じていた・・・",
    50: "ファムファンタル火山の火口に着くと、"
        "そこには朽ち果てた神殿跡があった。"
        "ベリンガム「ここは大地のイグニスを祭った祭壇だよ。"
        "待っていたよ。もっともワシ以上にイグニスは君を待っていたはず・・・"
        "さあ！復活を盛大に祝おうではないか！！」"
        "するとベリンガムの背後から魔獣達が現れた。"
        "クリムト「ムッ！遅かったか。いかんココで戦っては！」"
        "しかし、遅れてきたクリムトの声は届かなかった・・・",
    51: "ベリンガムの魔獣を倒したその時、大きく大地がゆれ"
        "達の足元が崩れ出した。",
    52: "そして地中深くより巨大なドラゴンが現れた。",
    53: "そのドラゴンは、まるでマグマのように赤い体をし、"
        "巨大なクチからは、嵐のような息使いが聞こえていた。",
    54: "ベリンガム「ハハッ！！待っていたぞ、この瞬間を。"
        "大地のイグニスの完全復活だ！」",
    55: "ベリンガム「おまえ達は例の古城跡で合獣機の準備をしろ！"
        "ワシは二人の再会を見てから行く。"
        "イグニスと天空のカノンと伝説の魔獣使いが合成して出来た君とのな・・・」"
        "は息をのんだ。",
    56: "クリムト「今の我々の力ではイグニスを倒す事は不可能じゃ！"
        "ここはひとまず逃げるぞ！！」"
        "しかしその時、の中で何かが目覚めていた・・・",
    57: "クリムト「どうした！？」"
        "「フフフッ！」"
        "「久しぶりだな・・・」"
        "の表情は"
        "明らかにいつもと違う人格へと変貌していた。",
    58: "「数百年にもわたる戦いの決着を今ここでつけてやる！」"
        "クリムトはの背後に写るカノンの姿を見た。",
    59: "大地のイグニスがおたけびを上げ地面に体を横たえた。"
        "ベリンガム「なんと言うことだ！イグニスがやぶれるとは！！」",
    60: "ベリンガム「いかん、このままでは！！」"
        "ベリンガムの手から発せられた不思議な光の帯が、"
        "イグニスの体を包み込むと、"
        "その巨体が宙に浮かんだ。",
    61: "光に包まれたイグニスとベリンガムは、空の彼方へ飛んでいった。",
    62: "ベリンガム「なんということだ！」"
        "カノンと魔獣使いが合成したは、"
        "これほどの強さを・・・",
}


# On-screen text of the 0x33 messages at 0xD1F96..0xD30F4 (inserts and
# controls omitted; see tools/extract_late_bank.py).  Verified against
# rendered messages; the zip check below re-verifies glyph-by-glyph.
READINGS_LATE = {
    0: "「ハアハア！」イグニスが去った後、我に返ったはその場に倒れこんだ。クリムト「おぬし・・・そうか！何かをきっかけとして、カノンの魂が目覚めるのか！」クリムト「もう話さねばなるまい。全ての事を・・・」クリムト「ベリンガムが言っていた事は事実じゃ！ワシがカノンと魔獣使いを合成し、おぬしが生まれた。」",
    1: "クリムト「そもそもワシがこの世界に合獣機というものを作り出したんじゃ。」クリムト「二匹のドラゴンが支配し狂暴な魔獣達が、支配していたこの世界に、人間的な秩序を持った魔獣人間を作ろうとしたんじゃ」",
    2: "クリムト「ワシが初めて作った魔獣人間、それがベリンガムじゃ。」クリムト「合成した魔獣は、強い遺伝に影響される。複数の魔獣達と合成を繰り返したが、ヤツは暗黒系の遺伝子をより強く受け継いでしまった。姿は人間だが心は狂暴な魔獣達と変わらないヤツだ。」",
    3: "クリムト「結局、ワシの理想はムズカシイと感じ始めた時、が現れた。」クリムト「は２匹のドラゴンと壮絶な戦いをし、が勝利したが、もまた全身に瀕死の重傷をおい、もはや命を助けるには合獣機を使う方法しか残されていなかった。」",
    4: "クリムト「わしは生命力の強いカノンと、を合成したんじゃ！」",
    5: "クリムト「そして、の遺伝子を強く受け継いだ、魔獣人間のおぬしが産まれた。」しかし、いっさいの記憶を失ってな。その後、おぬしはバルロア国の貴族、ウィンスロー一世の子供だと判った。つまり死んだおぬしの父、ウィンスロー二世はそなたの弟だ！彼は事実を知り、記憶の無いおぬしを本当の子のように育ててくれたんじゃよ。」父では無く自分の弟だったウィンスロー二世・・・は動揺する自分を抑えることで精一杯であった。",
    6: "クリムト「ベリンガムはこの事実を知ってイグニスをおびき出すために、おぬしを利用したんじゃ」",
    7: "クリムト「ヤツは古城跡に向かっているはずじゃ。あそこには昔、おぬしを合成した合獣機がある。ヤツはおぬしになろうとしておる。」",
    8: "クリムト「おぬしとイグニスの因果関係は永遠。逃れることは出来ん！伝説の魔獣を復活し、ヤツらを倒すのじゃ！」",
    9: "クリムト「いいか！これで伝説の魔獣が完成する。中型体のとを合成するんじゃ！",
    10: "クリムト「さすれば伝説の魔獣の完成じゃ！この魔獣を使えるのは、そなただけだ。古城跡へ向かい、ベリンガムの野望を阻止するんじゃ！」",
    11: "が中庭まで来ると、突然目の前にザーゴとラミレスが現れた。ザーゴ「今度は・・・本気！」ラミレス「もう容赦・・・しない！」",
    12: "ベリンガムの所へザーゴとラミレスが、逃げ帰って来た。ベリンガム「情けないやつらだ。おまえ達、この中へ入れ！」",
    13: "ベリンガム「おのれ、所詮ザコ同士の合成では、この程度の強さかっ！」ベリンガム「ならばさらなる力をあたえるために、ワシ自身と・・・」そう言うと、ベリンガムみずから合獣機の中に入った。",
    14: "ベリンガム「お・・・おのれこれ・・・で、ワシが・・・",
    15: "最強・・・」その先には、すでにイグニスが合獣機の中に入れられていた。ベリンガムは体を引きずりながら、合獣機の中に入った。",
    16: "合獣機が火を噴き、その炎はまたたくまに古城全体を包んだ！",
    17: "部屋中が炎に包まれてもは逃げ出さず、死んだベリンガムの姿をみつめていた。",
    18: "は思い出していた。ベリンガムが城に攻めて来た時の事を。",
    19: "ウィンスロー「これが目的だったのか！」ウィンスロー王が伝説の魔獣使いのタクトをベリンガムの前に差し出した時！タクトを見たの心がカノンの魂に支配され",
    20: "伝説の魔獣使いに恨みを持つカノンが、弟であるウィンスロー王に何をしたのか・・・",
    21: "の手から魔獣使いのタクトが落ちた。",
    22: "「が殺した・・・」炎が部屋中に広がり、の姿も炎に包まれた。",
    23: "古城全体が煙に包まれ、外壁が崩れた。",
    24: "クリムト「古い合獣機をムリに動かした結果じゃ！」クリムト「は・・・？」",
    25: "その時、炎に包まれていた城が崩れ落ちた。",
    26: "クリムトはその崩れた残骸の中、を探し歩いた。そして、火に焼かれ黒くなったタクトを見つけ出した。クリムトはそのタクトを見て確信した。",
    27: "クリムト「そうか・・・全て知った上での、決断か・・・」クリムト「何処かで生き延びているじゃろ！」",
    28: "そう自分に言い聞かせるよう、黒くなったタクトを見つめていた。",
    29: "～スタッフロール～❋The End❋",
    30: "は立ち止まり、考えた。クリムト老人が言った、伝説の魔獣無しで、戦えるだろうかと？そう考え、はその場を立ち去った。",
    31: "は立ち止まり、考えた。この先にはベリンガム達が、待ち構えている。伝説の魔獣の完成無しで、はたして勝てるのだろうか？魔獣を完成させるためはその場を離れた。",
    32: "は立ち止まり、考えた。この先にはベリンガム達が、待ち構えている。伝説の魔獣の完成無しではたして勝てるのだろうか？魔獣を完成させるため、はその場を離れた。",
}


# Hand-verified non-message readings: name-input charset and other
# glyph sheets.  Codes already covered by the message zip are checked
# for conflicts; the rest are added.  See WIKI.md for sources.
EXTRAS = [
    (142, "\u30a7", "name-input katakana; charset order, samples confirmed on screen"),
    (167, "\u30a8", "name-input katakana; charset order, samples confirmed on screen"),
    (169, "\u30a9", "name-input katakana; charset order, samples confirmed on screen"),
    (260, "\u30aa", "name-input katakana; charset order, samples confirmed on screen"),
    (262, "\u30ad", "name-input katakana; charset order, samples confirmed on screen"),
    (263, "\u30ae", "name-input katakana; charset order, samples confirmed on screen"),
    (265, "\u30b2", "name-input katakana; charset order, samples confirmed on screen"),
    (267, "\u30b5", "name-input katakana; charset order, samples confirmed on screen"),
    (268, "\u30b8", "name-input katakana; charset order, samples confirmed on screen"),
    (269, "\u30ba", "name-input katakana; charset order, samples confirmed on screen"),
    (270, "\u30bb", "name-input katakana; charset order, samples confirmed on screen"),
    (271, "\u30bc", "name-input katakana; charset order, samples confirmed on screen"),
    (272, "\u30bd", "name-input katakana; charset order, samples confirmed on screen"),
    (118, "\u30c0", "name-input katakana; charset order, samples confirmed on screen"),
    (274, "\u30c2", "name-input katakana; charset order, samples confirmed on screen"),
    (276, "\u30c5", "name-input katakana; charset order, samples confirmed on screen"),
    (25, "\u30c6", "name-input katakana; charset order, samples confirmed on screen"),
    (121, "\u30ca", "name-input katakana; charset order, samples confirmed on screen"),
    (279, "\u30cc", "name-input katakana; charset order, samples confirmed on screen"),
    (280, "\u30cd", "name-input katakana; charset order, samples confirmed on screen"),
    (161, "\u30ce", "name-input katakana; charset order, samples confirmed on screen"),
    (166, "\u30cf", "name-input katakana; charset order, samples confirmed on screen"),
    (281, "\u30d1", "name-input katakana; charset order, samples confirmed on screen"),
    (163, "\u30d3", "name-input katakana; charset order, samples confirmed on screen"),
    (283, "\u30d4", "name-input katakana; charset order, samples confirmed on screen"),
    (164, "\u30d6", "name-input katakana; charset order, samples confirmed on screen"),
    (284, "\u30d7", "name-input katakana; charset order, samples confirmed on screen"),
    (162, "\u30d8", "name-input katakana; charset order, samples confirmed on screen"),
    (285, "\u30da", "name-input katakana; charset order, samples confirmed on screen"),
    (151, "\u30db", "name-input katakana; charset order, samples confirmed on screen"),
    (146, "\u30dc", "name-input katakana; charset order, samples confirmed on screen"),
    (286, "\u30dd", "name-input katakana; charset order, samples confirmed on screen"),
    (288, "\u30e2", "name-input katakana; charset order, samples confirmed on screen"),
    (289, "\u30e3", "name-input katakana; charset order, samples confirmed on screen"),
    (165, "\u30e5", "name-input katakana; charset order, samples confirmed on screen"),
    (291, "\u30e6", "name-input katakana; charset order, samples confirmed on screen"),
    (292, "\u30e7", "name-input katakana; charset order, samples confirmed on screen"),
    (293, "\u30e8", "name-input katakana; charset order, samples confirmed on screen"),
    (294, "\u30f2", "name-input katakana; charset order, samples confirmed on screen"),
    (259, "\u30a5", "name-input katakana; charset order, samples confirmed on screen"),
    (224, "\u3041", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (225, "\u3043", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (226, "\u3045", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (228, "\u3047", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (229, "\u3049", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (234, "\u305c", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (236, "\u3062", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (239, "\u3071", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (242, "\u3074", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (243, "\u3075", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (245, "\u3077", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (246, "\u307a", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (248, "\u307c", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (249, "\u307d", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (254, "\u3085", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (256, "\u3087", "name-input hiragana (small-variant codes); pair sizes verified by render"),
    (86, "\uff10", "digit block (fullwidth); confirmed on screen"),
    (32, "\uff14", "digit block (fullwidth); confirmed on screen"),
    (33, "\uff15", "digit block (fullwidth); confirmed on screen"),
    (87, "\uff16", "digit block (fullwidth); confirmed on screen"),
    (88, "\uff17", "digit block (fullwidth); confirmed on screen"),
    (89, "\uff18", "digit block (fullwidth); confirmed on screen"),
    (90, "\uff19", "digit block (fullwidth); confirmed on screen"),
    (134, "\u25bc", "digit block (fullwidth); confirmed on screen"),
    (145, "A", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (139, "B", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (177, "C", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (178, "D", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (179, "E", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (180, "F", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (140, "G", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (181, "H", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (182, "I", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (183, "J", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (184, "K", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (157, "L", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (185, "M", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (186, "N", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (187, "O", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (188, "P", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (189, "Q", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (190, "R", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (191, "S", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (192, "T", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (193, "U", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (158, "V", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (194, "W", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (195, "X", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (196, "Y", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (197, "Z", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (198, "a", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (199, "b", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (200, "c", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (201, "d", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (202, "e", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (203, "f", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (204, "g", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (205, "h", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (206, "i", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (207, "j", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (208, "k", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (209, "l", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (210, "m", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (211, "n", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (212, "o", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (213, "p", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (214, "q", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (215, "r", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (216, "s", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (217, "t", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (218, "u", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (219, "v", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (220, "w", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (221, "x", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (222, "y", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (223, "z", "name-input latin; sample confirmed on screen (The End, BG, LV15)"),
    (156, "\u30e1", "name-input katakana; charset order, samples confirmed on screen"),
    (295, "\u3001", "symbol block; shape tentative"),
    (296, "\u3002", "symbol block; shape tentative"),
    (297, "\uff1a", "symbol block; verified by render"),
    (298, "\uff1b", "symbol block; verified by render"),
    (300, "\uff0f", "symbol block; verified by render"),
    (305, "\u00d7", "symbol block; verified by render"),
    (306, "\u00f7", "symbol block; verified by render"),
    (307, "\uff1d", "symbol block; verified by render"),
    (311, "\uffe5", "symbol block; verified by render"),
    (318, "\uff08", "symbol block; verified by render"),
    (319, "\uff09", "symbol block; verified by render"),
    (320, "\u2192", "symbol block; verified by render"),
    (135, "\u300c", "bracket variants: thick marker pair + thin tall pair (render-verified)"),
    (136, "\u300d", "bracket variants: thick marker pair + thin tall pair (render-verified)"),
    (326, "\u300c", "bracket variants: thick marker pair + thin tall pair (render-verified)"),
    (327, "\u300d", "bracket variants: thick marker pair + thin tall pair (render-verified)"),
    (170, "\u50d5", "word-table insert glyphs (male/female variants)"),
    (174, "\u5973", "word-table insert glyphs (male/female variants)"),
    (148, "\u9032", "kanji/UI; read from glyph sheet or render"),
    (356, "\u4ea4", "kanji/UI; read from glyph sheet or render"),
    (357, "\u5316", "kanji/UI; read from glyph sheet or render"),
    (175, "\u25a0", "kanji/UI; read from glyph sheet or render"),
    (673, "\u8010", "monster status word list (0xD30F4..0xD3144); read from render"),
    (674, "\u6483", "monster status word list (0xD30F4..0xD3144); read from render"),
    (675, "\u9632", "monster status word list (0xD30F4..0xD3144); read from render"),
    (676, "\u5fa1", "monster status word list (0xD30F4..0xD3144); read from render"),
    (677, "\u8b58", "monster status word list (0xD30F4..0xD3144); read from render"),
    (678, "\u5fc5", "monster status word list (0xD30F4..0xD3144); read from render"),
    (679, "\u53cd", "monster status word list (0xD30F4..0xD3144); read from render"),
    (680, "\u6575", "monster status word list (0xD30F4..0xD3144); read from render"),
    (681, "\u5f93", "monster status word list (0xD30F4..0xD3144); read from render"),
    (682, "\u9806", "monster status word list (0xD30F4..0xD3144); read from render"),
    (683, "\u56de", "monster status word list (0xD30F4..0xD3144); read from render"),
    (684, "\u907f", "monster status word list (0xD30F4..0xD3144); read from render"),
]
def glyphs_of(msg):
    out = []
    for screen in split_screens(tokens(msg)):
        for item in screen:
            if item[0] == "g":
                out.append(item[1])
    return out


def verify(readings, msgs, label, mapping):
    """Zip glyph tokens against expected text; fill mapping; return problems."""
    problems = 0
    for idx, expected in readings.items():
        glyphs = glyphs_of(msgs[idx])
        if len(glyphs) != len(expected):
            print(f"{label} {idx}: LENGTH MISMATCH tokens={len(glyphs)} "
                  f"expected={len(expected)}")
            problems += 1
            known = "".join(mapping.get(g, "?") for g in glyphs)
            n = 0
            while (n < min(len(known), len(expected))
                   and known[n] == expected[n]):
                n += 1
            lo = max(0, n - 14)
            print(f"  glyphs ...{known[lo:n + 14]}...")
            print(f"  expect ...{expected[lo:n + 14]}...")
            continue
        for g, ch in zip(glyphs, expected):
            old = mapping.get(g)
            if old is not None and old != ch:
                print(f"{label} {idx}: CONFLICT {g:03X} = {old} vs {ch}")
                problems += 1
            mapping[g] = ch
    return problems


def main():
    msgs = json.load(open(RAW))["messages"]
    msgs_late = json.load(open(RAW_LATE))["messages"]
    cm = json.load(open(CHARMAP))
    entries = cm["entries"]
    mapping = {}
    problems = verify(READINGS, msgs, "msg", mapping)
    problems += verify(READINGS_LATE, msgs_late, "late", mapping)
    extras = {}
    for code, ch, note in EXTRAS:
        old = mapping.get(code)
        if old is not None and old != ch:
            print(f"extras: CONFLICT {code:03X} = {old} vs {ch}")
            problems += 1
        mapping[code] = ch
        extras[code] = note
    print(f"mapped glyphs: {len(mapping)}; problems: {problems}")
    if problems:
        print("Fix readings before writing charmap.")
        return 1
    for g, ch in sorted(mapping.items()):
        key = f"{g}"
        if key not in entries:
            entries[key] = {"char": "", "notes": ""}
        entries[key]["char"] = ch
        entries[key]["notes"] = extras.get(
            g, "story bigfont; verified against render")
    cm["verified_through_msg"] = max(READINGS)
    cm["verified_late_through_msg"] = max(READINGS_LATE)
    with open(CHARMAP, "w") as f:
        json.dump(cm, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {CHARMAP} ({len(mapping)} glyphs confirmed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
