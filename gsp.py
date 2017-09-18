import itertools
import datetime


class GSP(object):
    def __init__(self):
        self.queue = []

#----------------------------------------------------------#
#                     计算freq1                            #
#----------------------------------------------------------#
    def freq1(self, data, frequent_num):
        '''
        查找一项频繁项集，看的是一个项在整个data中出现的次数，而不是总共出现的次数 
        '''
        appear = ''
        freq1 = []
        appear_ele = []
        appear_ele2 = []
        for i in range(len(data)):
            appear = ''
            for j in range(len(data[i])):
                appear += data[i][j]
            appear_ele += list(set(appear))
            print(appear_ele)
        #print(appear_ele)
        appear_ele2 = list(set(appear_ele))
        print(appear_ele2)
        for item in appear_ele2:
            itmes = appear_ele.count(item)
            if itmes >= frequent_num:
                freq1.append(item)
        print('频繁1项集为:%s' % freq1)
        return freq1

#----------------------------------------------------------#
#                     计算freq_more                        #
#----------------------------------------------------------#
    def freq_more(self, data, freq1):
        '''
        由一项频繁集找到相应的二项以及多项频繁集
        '''
        queue = []  # 所有的备选序列放在这里面
        queue_new = []  # 最终结果在这里面
        top = 0  # 这个是queue_new的队尾标号
        times = 3  # times 用来对排列组合进行计数 
        while True:
            if (queue_new == []):  # 为空则代表这是第一次遍历
                for i in range(len(freq1)):
                    for j in range(i + 1, len(freq1)):
                        item = freq1[i] + freq1[j]
                        queue.append(item)  # 枚举所有可能出现的二项 即同时出现的二项
                for i in range(len(freq1)):
                    for j in range(len(freq1)):
                        if j != i:
                            item = freq1[i] + '->' + freq1[j]
                            queue.append(item)  # 第一次遍历后全部可能出现的情况 # 枚举非同时，含有时序信息的二项
                for i in range(len(queue)):
                    freq_item = self.isFreq(queue[i], data) 
                    if freq_item != 0:
                        queue_new.append(freq_item)
                queue = []  # 清空queue(备选序列)   # 以及为什么这里要清空queue

            # 以上部分OK
            if (queue_new != []):  # 后几次遍历时要把所有的情况写入空的queue中
                if top == len(queue_new) - 1:  # 表示没有新加入元素，那么终止 while 循环
                    print('频繁多项集为:%s' % queue_new)
                    break
                else:
                    ### 1 start 本部分是针对同时出现的频繁集
                    demo_list = []  # 专门放'AB','BF','AF'这样的频繁序列，后面将他们合成为更多成员的备选频繁序列
                    for i in range(top, len(queue_new)):
                        if '->' not in queue_new[i]:
                            demo_list.append(queue_new[i])
                    demo_string = self.List_to_String(
                        demo_list)  # 将列表中的元素拼接成字符串，诸如拼成'ABBFAF' 
                    demo_ele = "".join(set(demo_string))  # 删除串中的重复元素,输出'ABF'
                    if len(demo_ele) >= times:
                        if len(demo_ele) == times:  # 那么demo_ele是唯一的备选成员
                            queue.append(demo_ele)
                            times += 1
                        # 否则对备选字母进行排列组合，比如'ABCDE'，一共能排列出10钟情况，并把它们推入queue(待判断成员队列)
                        else:
                            combin = self.Combinations(demo_ele, times)
                            for i in range(len(combin)):
                                queue.append(combin[i])
                            times += 1
                    ### 1 end 
                    ###-----####至此已经把备选频繁寻列推入 queue ####-----###

                    queue = self.Make_time_queue(top, freq1, queue, queue_new)

                    ###-----#### 至此已经把 queue 放满了备选成员 ####-----###

                    top = len(queue_new)  # 更新队尾指针 top 的位置

                    # 在此之前更新top值 也就是下次循环时，使用top之后的值 top之后的值是n-1项

                    ###-----#### 检测 queue 中的备选序列是否频繁 ####-----###
                    for i in range(len(queue)):
                        freq_item = self.isFreq(
                            queue[i], data)  # ---->> isFreq
                        if freq_item != 0:  # 如果这个成员是频繁的
                            queue_new.append(freq_item)
                    queue = []

    # 将列表中的字母合并成字符串   # 这个函数可以省略
    def List_to_String(self, list):
        demo_string = ''

        for i in range(len(list)):
            demo_string = demo_string + list[i]
        return demo_string

    #demo_ele是待排列的字符串, times是将它们排列成几个元素
    def Combinations(self, item, times):
        demo_list = []
        combin = []
        element = ''

        for i in range(1, len(item) + 1):
            it = itertools.combinations(item, i)
            demo_list.append(list(it))
        demo_combin = demo_list[times - 1]
        for i in range(len(demo_combin)):
            for j in range(len(demo_combin[0])):
                element += demo_combin[i][j]
            combin.append(element)
            element = ''
        return combin # -> 在 item 中随机抽取times个字母组成一个项

    # 判断item是不是频繁的
    def isFreq(self, item, data):
        '''
        如果是比较复杂的带有时序信息的，要怎么判断是不是频繁项
        ，项集下标 + 1 数据集 + 1 需要从头开始进行查找计数
        '''
        num = 0

        if '->' not in item:  # 类似如'ABF'
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if self.isIn_Item(item, data, i, j) != 0:
                        num += 1
            if num >= 2:   # 支持度是2
                return item
            else:
                return 0
        else:  # 类似如‘D->B->A’
            item0 = item.split('->')   # 判断 D->B->A在事物中出现了多少次

            for i in range(len(data)):
                array = 0  # item 的下标
                j = 0 # data 的下标
                while True:
                    if array == len(item0) or j == len(data[i]):
                        break
                    if len(item0[array]) >= 2:  # 如果类似 'BA' 形式
                        if self.isIn_Item(item0[array], data, i, j) == 1:
                            array += 1
                            j += 1
                        else:
                            j += 1
                    else:
                        if item0[array] in data[i][j]:
                            array += 1
                            j += 1
                        else:
                            j += 1
                if array == len(item0):
                    num += 1
            if num >= 2:
                return item
            else:
                return 0

    # 判断 item 是否在 data[i][j]中
    def isIn_Item(self, item, data, i, j):
        '''
        OK
        '''
        demo_num = 0

        for k in range(len(item)):
            if item[k] in data[i][j]:   # data[i] (a string list) data[i][j] (a string)
                demo_num += 1
        if demo_num == len(item):
            return 1
        else:
            return 0

    # 创造新的备选时间序列
    def Make_time_queue(self, top, freq1, queue, queue_new):
        '''
        这个函数还需要多看看，其实就是拓展，加进一个之前不存在的项，作为候选项，以后再判断是不是频繁项
        '''
        for i in range(top, len(queue_new)):     # 在新的queue_new中找到一个     
            if '->' not in queue_new[i]:
                difference = self.Difference(queue_new[i], freq1)
                for j in range(len(difference)): # 在没有出现过的字母中，加入到时序序列中来
                    queue.append(difference[j] + '->' +
                                 queue_new[i])  # 诸如 'D->AB'
                    queue.append(queue_new[i] + '->' +
                                 difference[j])  # 诸如 'AB->D'
            else:
                difference = self.Difference(queue_new[i], freq1)
                for j in range(len(difference)):
                    # 诸如'B->A' 扩展成 'B->A->D'
                    queue.append(queue_new[i] + '->' + difference[j])  # 对已经出现的再拓展一次
        return queue

    # 寻找两个字符串中的不同字母，并提取出来 # 本函数可以使用set来进行 # 为什么要找到不同的字母 
    def Difference(self, item, freq1):
        '''
        本函数可以使用更简单的方法来进行
        '''
        demo_list = []

        if '->' not in item:
            for i in range(len(freq1)):
                if freq1[i] not in item:
                    demo_list.append(freq1[i])
        else:
            demo_item = item.split('->')  # 将诸如'A->B'拆分成 'A','B'
            demo_item_string = self.List_to_String(demo_item)  # 合并成'AB'
            for i in range(len(freq1)):
                if freq1[i] not in demo_item_string:
                    demo_list.append(freq1[i])
        return demo_list


#----------------------------------------------------------#
#                          test                           #
#----------------------------------------------------------#
data = {0: ['CD', 'ABC', 'ABF', 'ACDF'],
        1: ['ABF', 'E'],
        2: ['ABF'],
        3: ['DGH', 'BF', 'AGH']}
starttime = datetime.datetime.now()
s = GSP()
print(data)
freq1 = s.freq1(data, 2)
s.freq_more(data, freq1)
endtime = datetime.datetime.now()
print(endtime - starttime)
