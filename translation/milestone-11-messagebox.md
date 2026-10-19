# Milestone 11 — field message box (3rd text system), 169 strings

Status: first full pass, all 169 strings translated. Layout assumes the
planned message-box change (13 glyphs/line, 3 lines, word wrap); see
WIKI.md for the renderer patch. `translation/msgfont_en.tsv` is the
machine-readable version of this table.

Terminology: 命令 = Order, クリア条件 = Clear Condition (compressed to
"Goal:" in battle objectives for width), 戦闘終了 = Battle Over,
プレイヤーポイント = Player Points, 通信 = link, 出撃 = deploy, 修行中 =
in training, 排除 = eliminate, ボコれ = Pummel, アイテム = Item,
魔獣 = beast, モンスター = monster. Names: Zargo, Ramires, Beringham,
Ignis (msg 61: glyph 186 is ニ, so the string is イグニス).

| # | JP | EN | len |
|---|----|----|-----|
| 0 | 命令を決めてください | Choose an order. | 16 |
| 1 | 指示の対象を決めてください | Choose the target. | 18 |
| 2 | 全部のモンスターに指示を出します | Order all monsters. | 19 |
| 3 | モンスター個別に指示を出します | Order each monster. | 19 |
| 4 | どのモンスターを狙うか決めてください | Choose a target monster. | 24 |
| 5 | コマンド対象モンスターを決めてください | Choose the target monster. | 26 |
| 6 | 戦闘終了 | Battle Over | 11 |
| 7 | クリア条件 | Clear Condition | 15 |
| 8 | ー クリア条件 ー   全ての敵を倒す | [Clear Condition] Defeat all enemies. | 37 |
| 9 | ー 命令：戦え ー   敵をみつけて攻撃する | [Order: Attack] Find and attack foes. | 37 |
| 10 | ー 命令：待機 ー   その場で立ち止まる | [Order: Wait] Hold your position. | 33 |
| 11 | ー 命令：排除 ー   敵を指定して排まえる | [Order: Eliminate] Hunt down the target. | 40 |
| 12 | ー 命令：アイテム ー アイテムを拾いにいく | [Order: Item] Go and pick up items. | 35 |
| 13 | ー 命令：逃げる ー  敵から逃げる | [Order: Flee] Run from the enemy. | 33 |
| 14 | ー 命令：守れ ー   ガードして攻撃をかわす | [Order: Defend] Guard and dodge attacks. | 40 |
| 15 | ー 命令：ボコれ ー  集中攻撃 | [Order: Pummel] Focus your attacks. | 35 |
| 16 | プレイヤーポイントが足りません | Not enough Player Points. | 25 |
| 17 | 対象となるモンスターがいません | No target monster. | 18 |
| 18 | 通信準備ができたらボタンを押してください | Press a button when ready to link. | 34 |
| 19 | 通信できませんでした | Link failed. | 12 |
| 20 | 通信中 | Linking... | 10 |
| 21 | 無制限クラス      料金０Ｇ | Unlimited Class    Fee 0G | 25 |
| 22 | ＬＶ５１以上クラス   料金３００Ｇ | Lv 51+ Class       Fee 300G | 27 |
| 23 | ＬＶ３１～ＬＶ５０クラス料金６０Ｇ | Lv 31-50 Class     Fee 60G | 26 |
| 24 | ＬＶ１１～ＬＶ３０クラス料金２０Ｇ | Lv 11-30 Class     Fee 20G | 26 |
| 25 | ＬＶ１～ＬＶ１０クラス 料金１０Ｇ | Lv 1-10 Class      Fee 10G | 26 |
| 26 | あ加できないモンスターがパーティーに入っています | Your party has a monster you can't use. | 39 |
| 27 | 対戦成績 勝   負   引き分け | Battle Record  Win Loss Draw | 28 |
| 28 | ０１２３４５６７８９ | 0123456789 | 10 |
| 29 | プレイヤーポイントが足りません | Not enough Player Points. | 25 |
| 30 | モンスターを選んでください | Choose a monster. | 17 |
| 31 | 指示対象を決めてください | Choose the target. | 18 |
| 32 | 命令を決めてください | Choose an order. | 16 |
| 33 | 全部のモンスターに指示を出します | Order all monsters. | 19 |
| 34 | モンスター個別に指示を出します | Order each monster. | 19 |
| 35 | 対象となるモンスターがいません | No target monster. | 18 |
| 36 |  クリア条件      戦闘終了 | Clear Condition  Battle Over | 28 |
| 37 | 通信中です。Ｂボタンでキャンセルできます | Linking. Press B to cancel. | 27 |
| 38 | 通信エラーです。ケーブルを確認してください | Link error. Check the cable. | 28 |
| 39 | 通信準備ができたらＡボタンを押してください | Press A when ready to link. | 27 |
| 40 |   相手の作戦中！ |   Opponent is planning! | 23 |
| 41 | 【クリア条件】    行く手を阻む魔獣を殲滅 | Goal: Beat the beasts in your way. | 34 |
| 42 | 【クリア条件】    襲いくる魔獣達を倒せ！ | Goal: Defeat the attacking beasts! | 34 |
| 43 | 【クリア条件】    追手の魔獣を全滅せよ！ | Goal: Wipe out the pursuing beasts! | 35 |
| 44 | 【クリア条件】    追手の魔獣を全滅せよ！ | Goal: Wipe out the pursuing beasts! | 35 |
| 45 | 【クリア条件】    敵の魔獣の全滅！ | Goal: Annihilate the enemy beasts! | 34 |
| 46 | 【クリア条件】    敵の魔獣達を全滅せよ！ | Goal: Wipe out all enemy beasts! | 32 |
| 47 | 【クリア条件】    砦備の魔獣を倒せ！ | Goal: Defeat the fort's beasts! | 31 |
| 48 | 【クリア条件】    城塞の魔獣を倒せ！ | Goal: Defeat the citadel beasts! | 32 |
| 49 | 【クリア条件】    城塞の魔獣の殲滅！ | Goal: Wipe out the citadel beasts! | 34 |
| 50 | 【クリア条件】    敵の魔獣達を全滅せよ！ | Goal: Wipe out all enemy beasts! | 32 |
| 51 | 【クリア条件】    サーゴを倒せ！ | Goal: Defeat Zargo! | 19 |
| 52 | 【クリア条件】    岩の番人達の殲滅！ | Goal: Annihilate the rock guardians! | 36 |
| 53 | 【クリア条件】    森の先住者を倒せ！ | Goal: Defeat the forest dwellers! | 33 |
| 54 | 【クリア条件】    魔獣たちを倒せ！ | Goal: Defeat the beasts! | 24 |
| 55 | 【クリア条件】    癒った兵士の殲滅！ | Goal: Annihilate the healed soldiers! | 37 |
| 56 | 【クリア条件】    待ち伏せた魔獣を倒せ！ | Goal: Defeat the ambushing beasts! | 34 |
| 57 | 【クリア条件】    敵の放った魔獣を倒せ！ | Goal: Defeat the enemy's beasts! | 32 |
| 58 | 【クリア条件】    サーゴを倒せ！ | Goal: Defeat Zargo! | 19 |
| 59 | 【クリア条件】    ラミレスを倒せ！ | Goal: Defeat Ramires! | 21 |
| 60 | 【クリア条件】    魔獣を倒せ！ | Goal: Defeat the beast! | 23 |
| 61 | 【クリア条件】    イグニスを倒せ！ | Goal: Defeat Ignis! | 19 |
| 62 | 【クリア条件】    追手の魔獣を殲滅せよ！ | Goal: Annihilate the pursuers! | 30 |
| 63 | 【クリア条件】    砂漠の魔獣達を倒せ！ | Goal: Defeat the desert beasts! | 31 |
| 64 | 【クリア条件】    廃墟の魔獣達を倒せ！ | Goal: Defeat the ruin beasts! | 29 |
| 65 | 【クリア条件】    敵の追跡者を倒せ！ | Goal: Defeat the enemy trackers! | 32 |
| 66 | 【クリア条件】    敵の見張りを倒せ！ | Goal: Defeat the enemy lookouts! | 32 |
| 67 | 【クリア条件】    サーゴを倒せ！ | Goal: Defeat Zargo! | 19 |
| 68 | 【クリア条件】    ラミレスを倒せ！ | Goal: Defeat Ramires! | 21 |
| 69 | 【クリア条件】    敵の合成魔獣を倒せ！ | Goal: Defeat the combined beast! | 32 |
| 70 | 【クリア条件】    ベリンガムを倒せ！ | Goal: Defeat Beringham! | 23 |
| 71 | 【クリア条件】    敵最終形態の魔獣を倒せ | Goal: Defeat the final-form beast! | 34 |
| 72 | 【クリア条件】    現れた魔獣達の殲滅！ | Goal: Annihilate the beasts! | 28 |
| 73 |  【命令：戦え】   敵をみつけて攻撃する | [Order: Attack] Find and attack foes. | 37 |
| 74 |  【命令：待機】   その場で立ち止まる | [Order: Wait] Hold your position. | 33 |
| 75 |  【命令：排除】   敵を指定して排まえる | [Order: Eliminate] Hunt down the target. | 40 |
| 76 |  【命令：アイテム】 アイテムを拾いにいく | [Order: Item] Go and pick up items. | 35 |
| 77 |  【命令：逃げる】  敵から逃げる | [Order: Flee] Run from the enemy. | 33 |
| 78 |  【命令：守れ】   ガードして攻撃をかわす | [Order: Defend] Guard and dodge attacks. | 40 |
| 79 |  【命令：ポコれ】  集中攻撃 | [Order: Pummel] Focus your attacks. | 35 |
| 80 | 無制限級         料金０Ｇ | Unlimited Class     Fee 0G | 26 |
| 81 | レベル５１以上級     料金３００Ｇ | Level 51+ Class     Fee 300G | 28 |
| 82 | レベル３１～レベル５０級 料金６０Ｇ | Level 31-50 Class   Fee 60G | 27 |
| 83 | レベル１１～レベル３０級 料金２０Ｇ | Level 11-30 Class   Fee 20G | 27 |
| 84 | レベル１～レベル１０級  料金１０Ｇ | Level 1-10 Class    Fee 10G | 27 |
| 85 | あ加できないモンスターがパーティーに入っています | Your party has a monster you can't use. | 39 |
| 86 | 対戦成績  勝  負  引き分け | Battle Record  Win Loss Draw | 28 |
| 87 | ０１２３４５６７８９ | 0123456789 | 10 |
| 88 | 記録が破壊されています 削除完了しました | Data is corrupted. Deletion complete. | 37 |
| 89 | データをセーブしますか はい  いいえ | Save data?  Yes  No | 19 |
| 90 | データをセーブしました | Data saved. | 11 |
| 91 | 残念ですがデータはセーブできないようです | Sorry, can't save the data. | 27 |
| 92 | ワールドマップへ切替えます | Switching to World Map. | 23 |
| 93 | ブリーフィングへ切替えます | Switching to Briefing. | 22 |
| 94 | モンスター管理へ切替えます | Switching to Monsters. | 22 |
| 95 | パーティ編成へ切替えます | Switching to Party. | 19 |
| 96 | アイテム管理へ切替えます | Switching to Items. | 19 |
| 97 | システム処理へ切替えます | Switching to System. | 20 |
| 98 | プレイヤーの名前を変更します | Change the player's name. | 25 |
| 99 | メッセージ表示を行います | Show messages. | 14 |
| 100 | 通信イベント中のパーティ状態を表示します | Show party status during links. | 31 |
| 101 | 攻略に必要なモンスターの情報を表示します | Show info on monsters you need. | 31 |
| 102 | モンスターパラメータを確認します | Check monster stats. | 20 |
| 103 | モンスターの名前変更が行えます | Rename a monster. | 17 |
| 104 | モンスターの名前変更は、只今行えません | Can't rename monsters now. | 26 |
| 105 | 出撃設定にできます | Can be deployed. | 16 |
| 106 | このパーティが戦闘を行います | This party will fight. | 22 |
| 107 | 修行中の為、出撃設定にはできません | In training: can't deploy. | 26 |
| 108 | 編成されていないので出撃設定にはできません | Not in a party: can't deploy. | 29 |
| 109 | パーティ名未設定の為、出撃設定できません | No party name: can't deploy. | 28 |
| 110 | パーティ名を設定します | Set the party name. | 19 |
| 111 | パーティ名を変更します | Change the party name. | 22 |
| 112 | 修行中の為、名前の変更は行えません | In training: can't rename. | 26 |
| 113 | パーティ編成を行います | Set up the party. | 17 |
| 114 | 修行中の為、編成は行えません | In training: can't edit party. | 30 |
| 115 | パーティに加えることができます | Can be added to the party. | 26 |
| 116 | 位置変更／パーティから外せます | Reorder / remove from party. | 28 |
| 117 | 修行中の為、操作は行えません | In training: can't change. | 26 |
| 118 | アイテムの装備を行います | Equip items. | 12 |
| 119 | アイテムの装備／解除を行います | Equip / remove items. | 21 |
| 120 | このアイテムの装備変更は行えません | This item can't be changed. | 27 |
| 121 | モンスターにアイテムを装備します | Equip an item on a monster. | 27 |
| 122 | 装備中のアイテムを外します | Remove the equipped item. | 25 |
| 123 | このモンスターには装備できません | This monster can't equip it. | 28 |
| 124 | このパラメータを強化します | Boost this stat. | 16 |
| 125 | これがなくなるとダウンします | Knocked out when it hits zero. | 30 |
| 126 | ダメージ時のスキが小さくなります | Smaller openings when hit. | 26 |
| 127 | 与えるダメージが大きくなります | Increases damage dealt. | 23 |
| 128 | 受けたダメージを軽減します | Reduces damage taken. | 21 |
| 129 | 移動するスピードが速くなります | Increases movement speed. | 25 |
| 130 | 行動のムダな動作が減ります | Fewer wasted movements. | 23 |
| 131 | 必殺技を行いやすくなります | Improves special moves. | 23 |
| 132 | 反撃を行いやすくなります | Improves counterattacks. | 24 |
| 133 | 相性の良い敵を選ぶようになります | Picks foes it is strong against. | 32 |
| 134 | 命令に服従しやすくなります | Obeys orders more often. | 24 |
| 135 | 攻撃が命中しやすくなります | Improves attack accuracy. | 25 |
| 136 | 攻撃を回避しやすくなります | Improves evasion. | 17 |
| 137 | 排除の成功する確率がアップします | Boosts eliminate success. | 25 |
| 138 | データを保存します | Save data. | 10 |
| 139 | いままでのイベントを見ます | View events so far. | 19 |
| 140 | 仲間にした事のあるモンスターなどを表示します | Show monsters you recruited. | 28 |
| 141 | サウンド関連の調整を行います | Adjust sound settings. | 22 |
| 142 | メッセージの表示スピードを変更します | Change message speed. | 21 |
| 143 | 自分のモンスターにマークをつけます | Mark your own monsters. | 23 |
| 144 | ヘルプの自動表示を行うか設定します | Set auto-help on or off. | 24 |
| 145 | 出撃タイプを選択します | Choose the deploy type. | 23 |
| 146 | 音楽のＯＮ／ＯＦＦを設定します | Set music ON / OFF. | 19 |
| 147 | 効果音のＯＮ／ＯＦＦを設定します | Set sound ON / OFF. | 19 |
| 148 | データを保存するファイルを選択してください | Choose a file to save. | 22 |
| 149 | 見たいイベントを選択してください | Choose an event to view. | 24 |
| 150 | 魔獣モンスターを選択してください | Choose a beast monster. | 23 |
| 151 | 全ての保存データのクリアを行います | Erase all saved data. | 21 |
| 152 | パスワードの削除を行います | Delete the password. | 20 |
| 153 | 前回の続きからはじめます | Continue from last save. | 24 |
| 154 | セーブデータが存在しません | There is no save data. | 22 |
| 155 | ０１２３４５６７８９ | 0123456789 | 10 |
| 156 | 生命 | Life | 4 |
| 157 | 耐久 | Durability | 10 |
| 158 | 攻撃 | Attack | 6 |
| 159 | 防御 | Defense | 7 |
| 160 | 行動 | Agility | 7 |
| 161 | 知識 | Knowledge | 9 |
| 162 | 必殺技 | Special | 7 |
| 163 | 反撃 | Counter | 7 |
| 164 | 索敵 | Recon | 5 |
| 165 | 従順 | Obedience | 9 |
| 166 | 命中 | Accuracy | 8 |
| 167 | 回避 | Evasion | 7 |
| 168 | 技能 | Skill | 5 |
