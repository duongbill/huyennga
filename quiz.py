import streamlit as st
import re
import pandas as pd
from math import ceil
import time
import random
import os

# --- THIẾT LẬP THỜI GIAN ---
DEFAULT_TIME_LIMIT = 12
MATCH_TIME_LIMIT = 30

# --- DỮ LIỆU CÂU HỎI ---
quiz_data_string = """
--- PHẦN A (ĐIỀN TỪ & ĐÚNG/SAI)/ ---
[1.]
Câu hỏi: “数”在汉语中是个多音字，在“请 你数一下，看看总数是多少”这句话中分别 读作______和 。
Đáp án: shǔ、shù
[2.]
Câu hỏi: “大”是多音字，在“这是王大夫的大儿 子”这句话中分别读作_____和 。
Đáp án: dài、dà
[3.]
Câu hỏi: “长”在汉语中是个多音字,在“头发越长越 长了”中分别读作______和 。
Đáp án: zhǎng、cháng
[4.]
Câu hỏi: “答”是多音字，在“你的回答正确”和 “ 我没有答应他的请求 ” 中分别读 作_______和 。
Đáp án: dá、dā
[5.]
Câu hỏi: “难”在汉语中是个多音字，在“灾难来 临的时候，我们应该临危不惧，千万不要被难 倒！”这句话中分别读作_____和_____。
Đáp án: nàn、nán
[6.]
Câu hỏi: 根据整个句子的意思，填写关联词语， 完成句子。 “_______更早一点出门，我们_______能避开 上班堵车的早高峰。”
Đáp án: 只有……才/如果……就/要是……就
[7.]
Câu hỏi: 填写关联词语，根据句意完成句子. “_______我们早一点出门，_______不会赶上 这堵车的早高峰了！唉！”
Đáp án: 如果/假如/要是、就
[8.]
Câu hỏi: “大家都说你有两把刷子”，这里“有两 把刷子”的意思是 _____。
Đáp án: 有本领、有能力、有本事。
[9.]
Câu hỏi: 在汉语口语中，说一个人“没喝过什么墨 水”，意思是这个人“_____很少”。
Đáp án: 文化/知识/学问
[10.]
Câu hỏi: “他在音乐方面完全是个门外汉”的意思 是 “_____”。
Đáp án: 他在音乐方面是个外行人。
[11.]
Câu hỏi: “大家都说你做菜有两下子！今天的饭你 来做吧！” 这个句子里“有两下子”的意思是 _____。
Đáp án: 具有某些方面的技术或才能/技术好/有水 平/水平高）
[12.]
Câu hỏi: 汉语中有这样的句子：“听说你乒乓球打 得很不错，给我们露两手吧！”这里“露两手” 的意思是_____。
Đáp án: 展示在某些方面的技术或才能
[13.]
Câu hỏi: 汉语中有些词“儿化”以后，词义 会产生 变化，往往能表示“少、小、 轻”等状态和性 质。如“瓶盖儿”、 “雨点儿”、“针眼儿” 等。
Đáp án: 正确。
[14.]
Câu hỏi: 汉语中有些词“儿化”以后，词义会产生变 化，往往能表示“少、小、轻”等状态或性质。 如“果汁儿”“针尖儿”“指甲刀儿”等。
Đáp án: 正确。
[15.]
Câu hỏi: 汉语中加在名词后面的“儿”大多可以表 示小，如“玻璃球儿”“土豆丝儿”“号码牌 儿”中的“儿”。
Đáp án: 正确。
[16.]
Câu hỏi: 汉语中有些词“儿化”以后，词义会产生 变化，往往能表示“少、小、轻”等状态或性 质，如“雨点儿”“土豆丝儿”“米粒儿”等。
Đáp án: 正确。
[17.]
Câu hỏi: “月”在“明”、“朋”、“胃” 中都是 表示“肉”的意思。
Đáp án: 错误。“月”在“明”中不是。
[18.]
Câu hỏi: “月”在“朝”“阴”“胖”中原来都是表 示 “月亮”的意思。
Đáp án: 错误。“胖”中的“月”不是。
[19.]
Câu hỏi: “桌子”“椅子”“孩子”“孔子”“面 子”等词里的“子”都读轻声，是词缀。
Đáp án: 错误。“孔子”的“子”不读轻声，不 是词缀。
[20.]
Câu hỏi: “石头”“馒头”“木头”“枕头”“针 头”等词里的“头”都读轻声。
Đáp án: 错误。“针头”的“头”不读轻声。
[21.]
Câu hỏi: “想头、听头、看头、山头、吃头”都读轻 声。
Đáp án: 错误。“山头”的“头”不读轻声。
[22.]
Câu hỏi: “他每天从家七点钟去学校”这句话是正确的。
Đáp án: 错误。应为“他每天七点钟从家去学校”。
[23.]
Câu hỏi: “昨天大伙儿都来参加晚会了，你为什么没 来吗？”这句话说得不对，应该说成“昨天大伙 儿都来参加晚会了，你为什么没来呢？”
Đáp án: 正确。
[24.]
Câu hỏi: “昨天我们都去参加小王的婚礼了，你为什 么没来吗？”这句话说得不对，应该说成“昨天 我们都去参加小王的婚礼了，你为什么没来 呢？”
Đáp án: 正确。
[25.]
Câu hỏi: “同学们都去看电影了，你为什么不去 吗？”的说法不对，应该说成“同学们都去看 电影了，你为什么不去呢？”
Đáp án: 正确。
[26.]
Câu hỏi: “他明天不来学书法”和“他明天没来学书 法”都是正确的句子。
Đáp án: 错误。第二句错误。
[27.]
Câu hỏi: “这个月我付给你五百十五块”这句话是错 误的。
Đáp án: 正确。应该说“这个月我付给你五百一 十五块”。
[28.]
Câu hỏi: “我比我哥哥不高”这句话是正确的。
Đáp án: 错误。应该说“我没有我哥哥高”。
[29.]
Câu hỏi: “饭吃不完”和“饭没吃完”的意思一样。
Đáp án: 错误。
[30.]
Câu hỏi: “钱花不完。”和“钱不花完。” 的意思一 样。
Đáp án: 错误。
[31.]
Câu hỏi: “这事儿刚说完，怎么还提起来了？ ”这句 话“还”使用正确。
Đáp án: 错误。“还”应改为“又”。
[32.]
Câu hỏi: “请你把外套脱。”这句话不符合汉语 “把”字句的要求，可以改成“请你把外套脱 下。”
Đáp án: 正确。
[33.]
Câu hỏi: A:你真漂亮！ B:哪里哪里！ 上面的对话中，B 想问 A 自己哪个部位很漂亮。
Đáp án: 错误。“哪里哪里”是一种谦虚的说法。
[34.]
Câu hỏi: “这么多年没联系，她的模样我真的不记起 来了。”这句话没有语法错误。
Đáp án: 错误。应为“记不起来了”。
[35.]
Câu hỏi: “上周末你去了哪些地方，真的不想起来了 吗？”这句话没有语法错误。
Đáp án: 错误。应为“想不起来”。
[36.]
Câu hỏi: “上海是中国大城市中的之一”这句话表达 正确。
Đáp án: 错误。应该说“上海是中国的大城市之 一”或“上海是中国大城市中的一个”。
[37.]
Câu hỏi: “她虽然花了不少时间和精力，所以还是没 能完成手头的工作。”这句话的关联词语用得准 确。
Đáp án: 错误。“所以”改成“但/可”。
[38.]
Câu hỏi: “虽然我不可能了解每个人的内心，但我却 愿意相信人大都是善良的。”这句话的词序是对 的。
Đáp án: 正确。
[39.]
Câu hỏi: “她不但自己学习勤奋努力，所以还抽出时 间帮助同学，一起进步。”这句话的关联词语用得准确。
Đáp án: 错误。“所以”改成“而且”。
[40.]
Câu hỏi: 普通话是以北京语音为标准音,以北方话为基础方言，以典范的现代白话文著作为语法规范的全民通用语。 
Đáp án: 北方话 
[41.]
Câu hỏi: 按照中国婚姻法的规定，中国公民的结婚年龄,男性不得早于______ 周岁，女性不得早于______周岁。 
Đáp án: 22 20 
[42.]
Câu hỏi: 北京传统民居的格局是，一个院子四面建有房 屋， 将 庭 院 合 围 在 中 间 ， 这 种 民 居 叫___________。 
Đáp án: 四合院
[43.]
Câu hỏi: 中国人逢有新婚吉庆时，都爱在门窗上贴大红的_________字，寓意好事成双、大吉大利。 
Đáp án: 囍 
[44.]
Câu hỏi: 中国是世界文明古国之一。中国古代四大发明是指南针、造纸术、___________和火药。 
Đáp án: 印刷术
[45.]
Câu hỏi: 你知道中国的“三大国粹”是指什么吗？请列举出来。 
Đáp án: 国画、京剧、中医。
[46.]
Câu hỏi: 中国画按内容分，主要有人物画、山水画和______ 三大类。 
Đáp án: 花鸟画
[47.]
Câu hỏi: “文房四宝” 是中国独具特色的文书工具。请一一列举。 
Đáp án: 笔、墨、纸、砚。 
[48.]
Câu hỏi: 中国古诗文中常提到的“花中四君子”指的是哪四种植物？ 
Đáp án: 梅、兰、竹、菊
--- PHẦN B (TRẮC NGHIỆM)/ ---
[49.]
Câu hỏi: 中国人口在地域上的分布特点是_______。 
Các lựa chọn:
A.  东多西少 B. 东少西多 C. 南多北少 D. 南少北多 
Đáp án: A 
[50.]
Câu hỏi: 中国是一个多民族的国家，共有_____个民族。 
Các lựa chọn: 
A.  50 B. 55 C. 32 D. 56 
Đáp án: D 
[51.]
Câu hỏi: 中国气候的特点是________，属于大陆性季风气候。 
Các lựa chọn: A. 北暖南寒 B. 南暖北寒 C. 东暖西寒 D. 西暖冬寒 
Đáp án: B 
[52.]
Câu hỏi: 北京的传统民居叫_______，它是中国古老传统的文化象征。 Các lựa chọn: A. 大杂院 B. 四合院 C. 别墅 D. 围屋 
Đáp án: B 
[53.]
Câu hỏi: 中国人结婚的时候喜欢在门上、窗户上贴一个大红色的字，这个字是_______字。 
Các lựa chọn: A. 春 B.喜 C. 庆 D. 福 
Đáp án: B 
[54.]
Câu hỏi: 中国古代伟大的思想家和教育家_______被联合国教科文组织列为世界十大文化名人之一。 
Các lựa chọn: A．庄子 B．老子 C．韩非子 D．孔子 
Đáp án: D 
[55.]
Câu hỏi: 中国传统文化中，______色常常用来代表喜庆。
Các lựa chọn: A. 蓝 B. 白 C. 红 D. 黑 
Đáp án: C 
[56.]
Câu hỏi: 下列四组词语中，加点汉字读音相同的一组是：
Các lựa chọn:
A. 为难． 难．得 B. 校长． 长．发 C. 快 乐． 乐 ．器 D.出行． 行．业
Đáp án: A
[57.]
Câu hỏi: 下列四组词语中，加点汉字读音相同的一组是：
Các lựa chọn:
A. 单数． 数．学 B. 家长． 长．远 C. 声乐． 乐．观 D. 银行． 自行．车
Đáp án: A
[58.]
Câu hỏi: 下列四组词语中，加点汉字读音 相同的一组是：
Các lựa chọn:
A. 汉朝． 朝．前走 B. 请假． 假．话 C. 音乐． 快乐． D. 外行． 人行．道
Đáp án: A
[59.]
Câu hỏi: 下列汉字中，不是形声字的是：
Các lựa chọn:
A. 枝 B. 期 C. 休 D. 房
Đáp án: C
[60.]
Câu hỏi: 下列汉字中，不是形声字的是：
Các lựa chọn:
A. 蜘 B. 简 C. 林 D. 唱
Đáp án: C
[61.]
Câu hỏi: 下列汉字中，不是形声字的是：
Các lựa chọn:
A. 功 B. 露 C. 甜 D. 梅
Đáp án: C
[62.]
Câu hỏi: 最近太忙了，那本书我还______。
Các lựa chọn:
A. 看没完 B. 看完没 C. 没看完 D. 不看完
Đáp án: C
[63.]
Câu hỏi: 快______玩手机了，老师开始讲课了。
Các lựa chọn:
A. 非 B. 没 C. 未 D. 别
Đáp án: D
[64.]
Câu hỏi: ______五点半，他______起床了。
Các lựa chọn:
A. 就、又 B. 刚、才 C. 才、就 D. 一、就
Đáp án: C
[65.]
Câu hỏi: ______八点了，他______没起床。
Các lựa chọn:
A. 都 、就 B. 刚 、才 C. 快 、还 D. 一 、就
Đáp án: C
[66.]
Câu hỏi: “作业做完了，不知道对不对，你帮忙 ______吧。”
Các lựa chọn:
A. 看有点儿 B.有点儿看 C. 一下儿看 D. 看一下
Đáp án: D
[67.]
Câu hỏi: 下了一夜的雨，我早上出门上学，觉 得______。
Các lựa chọn:
A. 有点儿冷 B. 一点儿冷 C. 冷一点儿 D. 冷有点儿
Đáp án: A
[68.]
Câu hỏi: “我现在不想吃饭，我先睡会儿吧，今天写 报告写了两个小时，的确是______。”
Các lựa chọn:
A. 有点儿累 B. 一点儿累 C. 累一点儿 D. 累有点儿
Đáp án: A
[69.]
Câu hỏi: 快到年末了，工作的确比平常______。
Các lựa chọn:
A. 有点儿忙 B. 一点儿忙 C. 忙一点儿 D. 忙有点儿
Đáp án: C
[70.]
Câu hỏi: 这首歌真好听，我还想听，你再唱一____吧。
Các lựa chọn:
A. 个 B. 趟 C. 首 D. 遍
Đáp án: D
[71.]
Câu hỏi: 我的作业做完了，不知道做得对不对，你 帮我检查一______吧。
Các lựa chọn:
A. 个 B. 趟 C. 本 D. 遍
Đáp án: D
[72.]
Câu hỏi: 看你，都跑出一______汗了，赶紧擦擦吧！
Các lựa chọn:
A. 次 B. 趟 C. 滴 D. 头
Đáp án: D
[73.]
Câu hỏi: 你说了这么多，可我真的一点儿都_____！
Các lựa chọn:
A. 听没懂 B. 听懂没 C. 没听懂 D. 不听懂
Đáp án: C
[74.]
Câu hỏi: 您千万______客气，这都是我应该做的。
Các lựa chọn:
A. 非 B. 没 C. 不 D. 别
Đáp án: D
[75.]
Câu hỏi: “您千万______这么夸我，我只做了我应 该做的事情啊！”
Các lựa chọn:
A. 要 B. 没 C. 不 D. 别
Đáp án: D
[76.]
Câu hỏi: 有些人早上赶时间，经常来不及吃早饭，长 期这样，______身体健康很不利。
Các lựa chọn:
A. 把 B. 给 C. 对 D. 为了
Đáp án: C
[77.]
Câu hỏi: ______四点半，我们就看见他急急忙忙 ______跑出办公室下班了。
Các lựa chọn:
A. 就、地 B. 刚、得 C. 才、地 D. 一、就
Đáp án: C
[78.]
Câu hỏi: “都过______九点，我们才看见他不急不 忙______走进办公室。”
Các lựa chọn:
A. 了、的 B. 了、地 C. 的、了 D. 得、了
Đáp án: B
[79.]
Câu hỏi: “天气实在太热了，冰箱里的冷饮都_____ 喝光了。”
Các lựa chọn:
A. 从 B. 由 C. 为 D. 被
Đáp án: D
[80.]
Câu hỏi: 马克特别喜欢中国菜，一到了中国, _____ 菜都想尝一尝。
Các lựa chọn:
A. 哪 B. 什么 C. 怎么 D. 谁
Đáp án: B
[81.]
Câu hỏi: 我刚到中国的时候，汉语一点儿也不会 说，和_____都没办法交流。
Các lựa chọn:
A. 哪儿 B. 什么 C. 怎么 D. 谁
Đáp án: D
[82.]
Câu hỏi: “我的书包不见了，我找遍教学楼，问了 每个人，_____都说没看见！”
Các lựa chọn:
A. 哪儿 B. 那儿 C. 这儿 D. 谁
Đáp án: D
[83.]
Câu hỏi: “汉语高手，_____你莫属！”
Các lựa chọn:
A. 不 B. 没 C. 非 D. 别
Đáp án: C
[84.]
Câu hỏi: 大家一致认为只有你去才能解决那个难 题，所以你_____去_____可！
Các lựa chọn:
A. 没 、不 B. 不 、没 C. 非 、不 D. 别 、不
Đáp án: C
[85.]
Câu hỏi: 这工作不能再拖下去了，大家一起努力， 今天_____完成_____可！
Các lựa chọn:
A. 没 、不 B. 不 、没 C. 非 、不 D. 别 、不
Đáp án: C
[86.]
Câu hỏi: 这本书对音乐专业的学生来说太重要了， 我今天______买______可！
Các lựa chọn:
A. 没 、不 B. 不 、没 C. 非 、不 D. 不 、不
Đáp án: C
[87.]
Câu hỏi: 我读不________了，这故事太长了！我要 歇一会儿。
Các lựa chọn:
A. 进去 B. 出去 C. 过去 D. 下去
Đáp án: D
[88.]
Câu hỏi: 我终于想______了，她是我小学同班同学。
Các lựa chọn:
A. 起来 B. 出去 C. 过去 D. 上来
Đáp án: A
[89.]
Câu hỏi: “这问题太难解决了！都两个小时了，我 一点法子也想______。”
Các lựa chọn:
A. 不出 B. 不能 C. 不动 D. 不够
Đáp án: A
[90.]
Câu hỏi: 我看不 了，这个人太蛮横了！我要去与他 评评理。
Các lựa chọn:
A. 进去 B. 下去 C. 过来 D. 出来
Đáp án: B
[91.]
Câu hỏi: “今年来我们学校留学的学生，据我所知， 欧美学生有上．百．个．”其中“上百个”的意思是:
Các lựa chọn:
A. 上学的有一百个 B. 接近一百个人 C. 上面的一百个人 D. 一百个上来了
Đáp án: B
[92.]
Câu hỏi: 他来中国留学，带来上百斤行李。“上百 斤”的意思是:
Các lựa chọn:
A. 一百斤以上 B．接近一百斤 C．上面的一百斤 D. 超过一百斤
Đáp án: B
[93.]
Câu hỏi: 早饭吃三个馒头不算多， 对我来说真是 _______一碟！
Các lựa chọn:
A. 小问题 B. 小麻烦 C. 小菜 D. 凉菜
Đáp án: C
[94.]
Câu hỏi: 这么简单的对话，对于我这个学了四年中 文的人来说，真是_______一碟！
Các lựa chọn:
A. 小意思 B. 小麻烦 C. 小菜 D. 凉菜
Đáp án: C

--- PHẦN C (NỐI CẶP)/ ---
[95.]
Câu hỏi: 请为下面的名词选择合适的量词，并用线段连接起来。
Đáp án:
一列 火车
一扇 木门
一台 电脑
一场 大雨
一道 彩虹
[96.]
Câu hỏi: 请为下面的名词选择合适的量词，并用线段连接起来。
Đáp án:
一辆 汽车
一口 水井
一部 小说
一场 电影
一道 彩虹
[97.]
Câu hỏi: 请为下面的名词选择合适的量词，并用线条连接起来。
Đáp án:
一枚 邮票
一艘 邮轮
一部 电影
一管 牙膏
一扇 窗

--- PHẦN D (HÌNH ẢNH)/ ---
[98.]
Câu hỏi: 看图完成汉语的一个成语。 anh1.jpg
Đáp án: 三心二意
[99.]
Câu hỏi: 用一个成语表示下面这幅图的意思： anh2.jpg
Đáp án: 对牛弹琴
[100.]
Câu hỏi: 用一个成语表示下面这幅图的意思： anh3.jpg
Đáp án: 画蛇添足
[101.]
Câu hỏi: 汉语成语“_______”，原指“住在井底的青蛙永远只能看到井口那么大的一块 天”。常用来比喻见识狭窄的人。 anh4.jpg
Đáp án: 井底之蛙/坐井观天 
[102.]
Câu hỏi: 有一个成语描述的是这样的景象：车多得像流水，马像游龙，形容来往车马很多，热闹繁忙的景象。这个成语是_______。 anh5.jpg
Đáp án: 车水马龙
"""

# --- LOGIC VÀ STATE MANAGEMENT ---

@st.cache_data
def parse_quiz_data(data_string):
    quiz_list = []
    data_string_fixed = data_string.replace("Câu-hỏi:", "Câu hỏi:")
    blocks = re.split(r'\n\[\d+\.\]', data_string_fixed)

    for block in blocks:
        block = block.strip()
        if not block: continue

        question_match = re.search(r'Câu hỏi:\s*(.*?)(?=\nĐáp án:)', block, re.DOTALL)
        answer_match = re.search(r'Đáp án:\s*(.*)', block, re.DOTALL)

        if not question_match or not answer_match: continue

        question_text = question_match.group(1).strip()
        answer_block = answer_match.group(1).strip()
        question_data = {"question": question_text}

        image_match = re.search(r'([\w-]+\.(?:jpg|jpeg|png))', question_text, re.IGNORECASE)

        if image_match:
            question_data["type"] = "image"
            image_filename = image_match.group(1)
            question_data["image_path"] = os.path.join("images", image_filename)
            question_data["question"] = question_text.replace(image_filename, "").strip()
            answers_set = {ans.strip() for ans in re.split(r'[、/，,]', answer_block.lower().replace(" ", ""))}
            answers_set.discard('')
            question_data["correct_answers"] = answers_set
            question_data["display_answer"] = answer_block
        elif '\n' in answer_block and len(re.split(r'\s+', answer_block.split('\n')[0].strip())) >= 2:
            question_data["type"] = "match"
            pairs = [re.split(r'\s+', line.strip(), 1) for line in answer_block.split('\n') if line.strip()]
            if pairs:
                question_data["left_items"] = [p[0] for p in pairs]
                question_data["right_items"] = [p[1] for p in pairs]
                question_data["solution_map"] = {p[0]: p[1] for p in pairs}
                question_data["display_answer"] = "\n".join([f"{k} -> {v}" for k, v in question_data["solution_map"].items()])
            else: continue
        elif "Các lựa chọn:" in block:
            question_data["type"] = "mcq"
            options_match = re.search(r'Các lựa chọn:\s*(.*?)\nĐáp án:', block, re.DOTALL)
            if not options_match: continue
            
            options_text = options_match.group(1).strip()
            options = [opt.strip() for opt in re.split(r'\s*[A-D][\.\．]\s*', options_text) if opt.strip()]
            question_data["options"] = options

            match = re.search(r'^\s*([A-D])\s*$', answer_block.strip())
            if match:
                correct_answer_char = match.group(1).upper()
                correct_index = ord(correct_answer_char) - ord('A')
                if 0 <= correct_index < len(options):
                    question_data["correct_answers"] = {options[correct_index]}
                    question_data["display_answer"] = f"{correct_answer_char}. {options[correct_index]}"
                else:
                    question_data["correct_answers"] = {answer_block}
                    question_data["display_answer"] = answer_block
            else:
                question_data["correct_answers"] = {answer_block}
                question_data["display_answer"] = answer_block
        else:
            question_data["type"] = "fill"
            answers_set = {ans.strip() for ans in re.split(r'[、/，,]', answer_block.lower().replace(" ", ""))}
            answers_set.discard('')
            question_data["correct_answers"] = answers_set
            question_data["display_answer"] = answer_block

        quiz_list.append(question_data)
    return quiz_list

def shuffle_and_reset():
    """Xáo trộn câu hỏi và reset toàn bộ tiến trình."""
    random.shuffle(st.session_state.quiz_data)
    
    st.session_state.num_questions = len(st.session_state.quiz_data)
    st.session_state.current_q_index = 0
    st.session_state.score = 0
    st.session_state.user_inputs = [{} if q.get('type') == 'match' else None for q in st.session_state.quiz_data]
    st.session_state.checked = [False] * st.session_state.num_questions
    st.session_state.is_correct = [False] * st.session_state.num_questions
    st.session_state.show_results_page = False

    # Xóa trạng thái xáo trộn cũ của các câu hỏi nối cặp
    keys_to_delete = [key for key in st.session_state if key.startswith('shuffled_')]
    for key in keys_to_delete:
        del st.session_state[key]
        
    init_question_state(0)

def initialize_session_state():
    st.session_state.quiz_data = parse_quiz_data(quiz_data_string)
    
    st.session_state.num_questions = len(st.session_state.quiz_data)
    st.session_state.current_q_index = 0
    st.session_state.score = 0
    st.session_state.user_inputs = [{} if q.get('type') == 'match' else None for q in st.session_state.quiz_data]
    st.session_state.checked = [False] * st.session_state.num_questions
    st.session_state.is_correct = [False] * st.session_state.num_questions
    st.session_state.show_results_page = False
    init_question_state(0)

def init_question_state(q_index):
    st.session_state.q_load_time = time.time()
    st.session_state.transition_at_time = None
    st.session_state.selected_left = None
    if q_index < len(st.session_state.quiz_data):
        q_data = st.session_state.quiz_data[q_index]
        if q_data.get('type') == 'match':
            if f'shuffled_left_{q_index}' not in st.session_state:
                shuffled_left = list(q_data['left_items']); random.shuffle(shuffled_left)
                st.session_state[f'shuffled_left_{q_index}'] = shuffled_left
                shuffled_right = list(q_data['right_items']); random.shuffle(shuffled_right)
                st.session_state[f'shuffled_right_{q_index}'] = shuffled_right

def goto_question(index):
    st.session_state.current_q_index = index
    st.session_state.show_results_page = False
    init_question_state(index)

def check_answer(q_index, user_input):
    q_data = st.session_state.quiz_data[q_index]
    st.session_state.user_inputs[q_index] = user_input
    st.session_state.checked[q_index] = True
    is_correct = False
    if user_input:
        q_type = q_data.get('type')
        if q_type in ['fill', 'image']:
            user_input_cleaned = user_input.strip().lower().replace(" ", "")
            user_parts = set(re.split(r'[、/，,]', user_input_cleaned))
            user_parts.discard('')
            is_correct = (user_parts == q_data.get('correct_answers'))
        elif q_type == 'mcq':
            is_correct = ({user_input} == q_data.get('correct_answers'))
        elif q_type == 'match':
            is_correct = (user_input == q_data.get('solution_map'))
    st.session_state.is_correct[q_index] = is_correct
    st.session_state.score = sum(st.session_state.is_correct)

def display_sidebar_navigation():
    st.sidebar.title("Điều hướng")
    st.sidebar.subheader(f"Điểm số: {st.session_state.score}/{st.session_state.num_questions}")
    
    # THÊM NÚT TRỘN CÂU HỎI
    st.sidebar.button("🔀 Trộn câu hỏi", use_container_width=True, on_click=shuffle_and_reset)
    
    st.sidebar.markdown("---")
    
    QUESTIONS_PER_ROW = 4
    num_rows = ceil(st.session_state.num_questions / QUESTIONS_PER_ROW)
    for row in range(num_rows):
        cols = st.sidebar.columns(QUESTIONS_PER_ROW)
        for col_index in range(QUESTIONS_PER_ROW):
            q_index = row * QUESTIONS_PER_ROW + col_index
            if q_index < st.session_state.num_questions:
                btn_label = f"{q_index + 1}"
                is_current = (q_index == st.session_state.current_q_index)
                btn_type = "primary" if is_current and not st.session_state.show_results_page else "secondary"
                if st.session_state.checked[q_index]:
                    icon = "✅" if st.session_state.is_correct[q_index] else "❌"
                    btn_label = f"{icon} {q_index + 1}"
                with cols[col_index]:
                    if st.button(btn_label, key=f"sidebar_btn_{q_index}", use_container_width=True, type=btn_type):
                        goto_question(q_index)
                        st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("Nộp bài & Xem Kết quả", use_container_width=True, type="primary"):
        st.session_state.show_results_page = True
        st.rerun()

def handle_match_selection(left_item=None, right_item=None):
    q_index = st.session_state.current_q_index
    q_data = st.session_state.quiz_data[q_index]
    user_pairs = st.session_state.user_inputs[q_index]
    solution_map = q_data['solution_map']
    if left_item:
        st.session_state.selected_left = left_item
        return
    if right_item and st.session_state.selected_left:
        selected_left = st.session_state.selected_left
        correct_right_partner = solution_map[selected_left]
        if right_item == correct_right_partner:
            user_pairs[selected_left] = right_item
            st.toast("Chính xác!", icon="✅")
            if len(user_pairs) == len(solution_map):
                check_answer(q_index, user_pairs)
        else:
            st.toast("Chưa đúng. Hãy thử lại!", icon="❌")
        st.session_state.selected_left = None

def display_question_content():
    q_index = st.session_state.current_q_index
    q_data = st.session_state.quiz_data[q_index]

    if st.session_state.get('transition_at_time') and time.time() > st.session_state.transition_at_time:
        st.session_state.transition_at_time = None
        if q_index < st.session_state.num_questions - 1: goto_question(q_index + 1)
        else: st.session_state.show_results_page = True
        st.rerun()
        return

    st.header(f"Câu hỏi {q_index + 1}/{st.session_state.num_questions}")
    timer_placeholder, progress_placeholder = st.empty(), st.empty()
    st.markdown(f"**{q_data.get('question', 'Lỗi: Không tìm thấy câu hỏi')}**")

    q_type = q_data.get('type')
    time_limit = MATCH_TIME_LIMIT if q_type == 'match' else DEFAULT_TIME_LIMIT
    time_left = time_limit - (time.time() - st.session_state.q_load_time)
    is_disabled = st.session_state.checked[q_index]
    
    user_input = None
    if q_type == 'image':
        try:
            st.image(q_data['image_path'])
        except Exception:
            st.error(f"Lỗi: Không thể tải ảnh tại '{q_data['image_path']}'. Hãy chắc chắn tệp tồn tại.")
        st.markdown("---")
        user_input = st.text_area("Nhập đáp án:", value=st.session_state.user_inputs[q_index] or "", key=f'input_{q_index}', disabled=is_disabled)
    elif q_type == 'match':
        st.markdown("---")
        user_pairs = st.session_state.user_inputs[q_index]
        left_col, right_col = st.columns(2)
        shuffled_left = st.session_state.get(f'shuffled_left_{q_index}', q_data['left_items'])
        shuffled_right = st.session_state.get(f'shuffled_right_{q_index}', q_data['right_items'])
        with left_col:
            for item in shuffled_left:
                is_selected = (st.session_state.selected_left == item)
                is_paired = item in user_pairs
                st.button(item, key=f"left_{item}", use_container_width=True, type="primary" if is_selected else "secondary", disabled=is_disabled or is_paired, on_click=handle_match_selection, args=(item, None))
        with right_col:
            for item in shuffled_right:
                is_paired = item in user_pairs.values()
                st.button(item, key=f"right_{item}", use_container_width=True, disabled=is_disabled or is_paired, on_click=handle_match_selection, args=(None, item))
        user_input = user_pairs
    elif q_type == 'fill':
        st.markdown("---")
        user_input = st.text_area("Nhập đáp án:", value=st.session_state.user_inputs[q_index] or "", key=f'input_{q_index}', disabled=is_disabled)
    elif q_type == 'mcq':
        st.markdown("---")
        options = q_data.get('options', [])
        default_index = options.index(st.session_state.user_inputs[q_index]) if st.session_state.user_inputs[q_index] in options else None
        user_input = st.radio("Chọn một đáp án:", options=options, index=default_index, key=f'input_{q_index}', disabled=is_disabled)

    st.markdown("---")
    if q_type not in ['match']:
        if st.button("KIỂM TRA", key=f'check_btn_{q_index}', disabled=is_disabled, type="primary"):
            check_answer(q_index, user_input)
            st.rerun()

    feedback_placeholder = st.empty()
    if is_disabled:
        if st.session_state.is_correct[q_index]: feedback_placeholder.success("✅ **CHÍNH XÁC!**")
        else: feedback_placeholder.error(f"❌ **CHƯA CHÍNH XÁC.** Đáp án đúng là:\n\n---\n\n{q_data.get('display_answer', '')}")
        if st.session_state.get('transition_at_time'):
            time_to_transition = st.session_state.transition_at_time - time.time()
            if time_to_transition > 0:
                timer_placeholder.info(f"Hết giờ! Tự động chuyển câu sau {int(time_to_transition) + 1} giây...")
                time.sleep(1); st.rerun()
    elif time_left <= 0:
        check_answer(q_index, user_input)
        st.session_state.transition_at_time = time.time() + 3
        st.rerun()
    else:
        time_display = max(0, int(time_left) + 1)
        timer_placeholder.info(f"⏰ **Thời gian còn lại:** {time_display} giây")
        progress_placeholder.progress(max(0.0, time_left / time_limit))
        time.sleep(1); st.rerun()

def display_results_page():
    # Top row: title on left, "Làm lại Quiz" button on the right
    left_col, right_col = st.columns([6, 1])
    with left_col:
        st.title("🎉 KẾT THÚC BÀI KIỂM TRA!")
        st.header(f"Tổng điểm: {st.session_state.score}/{st.session_state.num_questions}")
    with right_col:
        # Put the button at the top-right; use a small spacer to align vertically
        if st.button("Làm lại Quiz", type="primary"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    st.markdown("---")
    st.subheader("Chi tiết các câu trả lời:")

    for i, result in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Câu {i+1}:** {result.get('question', '')}")
        if result.get('type') == 'image':
            st.image(result['image_path'], width=150)
        
        status = "✅ Chính xác" if st.session_state.is_correct[i] else "❌ Sai"
        user_ans = st.session_state.user_inputs[i]
        
        if result.get('type') == 'match':
            user_ans_str = "\n".join([f"- {k} -> {v}" for k, v in user_ans.items()]) if user_ans else "(Chưa trả lời)"
            st.text(f"Câu trả lời của bạn:\n{user_ans_str}")
        else:
            user_ans_str = user_ans if user_ans else "(Chưa trả lời)"
            st.text(f"Câu trả lời của bạn: {user_ans_str}")
        st.text(f"Đáp án đúng:\n{result.get('display_answer', '')}")
        st.markdown(f"**Kết quả: {status}**")
        st.markdown("---")

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.title("HYQ TTQCS III")
    if 'quiz_data' not in st.session_state:
        initialize_session_state()
    display_sidebar_navigation()
    if st.session_state.show_results_page:
        display_results_page()
    else:
        display_question_content()

if __name__ == "__main__":
    main()