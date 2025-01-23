# 插值保序回归的实现
import bisect
class InterpolationIsotonicRegression:
    def __init__(self, x_raw_thresholds, y_raw_thresholds):
        self.x_raw_thresholds = x_raw_thresholds
        self.y_raw_thresholds = y_raw_thresholds

        self.x_thresholds=[]
        self.y_thresholds=[]
        self.w = []
        self.b = []

        self._preprocess()
    
    def _preprocess(self):
        for index in range(len(self.y_raw_thresholds)-1):
            if self.y_raw_thresholds[index+1] == self.y_raw_thresholds[index]:
                continue
            else:
                self.x_thresholds.append(self.x_raw_thresholds[index])
                self.y_thresholds.append(self.y_raw_thresholds[index])
    
    @staticmethod
    def _calculate_k(diff, intercepts, right_intercepts):
        k = []
        for index in range(len(intercepts)):
            k.append((right_intercepts[index]-intercepts[index])/diff[index])
        return k

    @staticmethod
    def _calculate_intercept(c_value,diff_value,N_value,next_y,y):
        return (c_value*next_y-diff_value*N_value*y)/(c_value-diff_value*N_value)

    @staticmethod
    def _calculate_right_intercept(c_value,diff_value,N_value,y,intercept):
        return (diff_value*N_value*(y-intercept))/c_value+intercept 
        
    @staticmethod
    def _calculate_diff(x_boundary):
        diff = [x_boundary[i + 1] - x_boundary[i] for i in range(len(x_boundary) - 1)]
        return diff

    @staticmethod
    def _calculate_c_N(x_list, x_boundary):
        # 确保边界列表是排序的
        x_boundary = sorted(x_boundary)
        
        # 初始化结果列表，用于存储每个区间的处理结果
        c_value = []
        N_value = []
        
        # 遍历边界列表，形成区间并处理数据
        for i in range(len(x_boundary) - 1):
            left, right = x_boundary[i], x_boundary[i + 1]
            # 找到落在当前区间的所有x值
            group = [x for x in x_list if left <= x < right]
            
            # 如果该区间有元素，则进行处理
            if group:
                # 计算组内元素减去左边界后的和
                sum_adjusted = sum([x - left for x in group])
                sum_count = len(group)
                # 将结果存储在列表中，index为右边界
                c_value.append(sum_adjusted)
                N_value.append(sum_count)
        
        return c_value,N_value

    def train(self,x,y):
        diff = self._calculate_diff(self.x_thresholds)
        c_value,N_value = self._calculate_c_N(x,self.x_thresholds)

        intercepts = []
        right_intercepts = []
        
        #截距计算
        for index in range(len(diff)-1):
            if index == 0:
                left_intercept = min(self.y_thresholds[1],max(0,self._calculate_intercept(c_value[0],diff[0],N_value[0],self.y_thresholds[2],self.y_thresholds[1])))
            else:
                left_intercept = min(self.y_thresholds[index+1],max(right_intercepts[-1],self._calculate_intercept(c_value[index],diff[index],N_value[index],self.y_thresholds[index+2],self.y_thresholds[index+1])))
            right_intercept = self._calculate_right_intercept(c_value[index],diff[index],N_value[index],self.y_thresholds[index+1],left_intercept)
            right_intercepts.append(right_intercept)
            intercepts.append(left_intercept)
        # 最后一段特殊处理
        final_left_intercept = right_intercepts[-1]
        right_intercept = self._calculate_right_intercept(c_value[-1],diff[-1],N_value[-1],self.y_thresholds[-1],final_left_intercept)
        intercepts.append(final_left_intercept)
        right_intercepts.append(right_intercept)

        print("intercepts:{}".format(intercepts))
        print("right_intercepts:{}".format(right_intercepts))
        
        self.w = self._calculate_k(diff,intercepts,right_intercepts)
        self.b = intercepts

        # for i in range(len(self.x_thresholds)-1):
        #     self.w.append((self.y_thresholds[i+1]-self.y_thresholds[i])/(self.x_thresholds[i+1]-self.x_thresholds[i]))
        #     self.b.append(self.y_thresholds[i])
        
        
    def predict(self, data):
        #边界值处理
        if data <= 0:
            return 0
        if data >= self.x_thresholds[-1]:
            data = self.x_thresholds[-1]
        
        # 使用bisect_right找到右侧插入点
        index = bisect.bisect_right(self.x_thresholds[1:], data)
        # 超出右边界处理
        if index == len(self.x_thresholds[1:]):
            index -= 1
        w = self.w[index]
        b = self.b[index]
        x_left = self.x_thresholds[index]
        return w*(data-x_left)+b
    def get_w(self):
        return self.w
    def get_b(self):
        return self.b
    def get_x_thresholds(self):
        return self.x_thresholds
    def get_y_thresholds(self):
        return self.y_thresholds