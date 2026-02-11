<template>
  <div class="calendar-container">
    <el-card class="calendar-card">
      <template #header>
        <div class="calendar-header">
          <h2>服务日历</h2>
          <div class="view-controls">
            <el-radio-group v-model="currentView" @change="switchView">
              <el-radio-button label="week">周历</el-radio-button>
              <el-radio-button label="month">日历</el-radio-button>
            </el-radio-group>
            <el-radio-group v-model="eventFilter" style="margin-left: 40px">
              <el-radio-button label="all">全部</el-radio-button>
              <el-radio-button label="meal">餐单</el-radio-button>
              <el-radio-button label="service">服务</el-radio-button>
            </el-radio-group>
          </div>
        </div>
      </template>
      
      <!-- 日历导航 -->
      <div class="calendar-navigation">
        <el-button type="primary" @click="prevPeriod">
          <el-icon><ArrowLeft /></el-icon>
          {{ currentView === 'week' ? '上周' : '上月' }}
        </el-button>
        <el-button type="primary" @click="today">
          <el-icon><Position /></el-icon>
          今天
        </el-button>
        <el-button type="primary" @click="nextPeriod">
          {{ currentView === 'week' ? '下周' : '下月' }}
          <el-icon><ArrowRight /></el-icon>
        </el-button>
        <div class="current-period" v-if="currentView === 'week'">
          {{ weekStart.format('YYYY-MM-DD') }} 至 {{ weekEnd.format('YYYY-MM-DD') }}
        </div>
        <div class="current-period" v-else>
          {{ currentDate.format('YYYY年MM月') }}
        </div>
      </div>
      
      <!-- 周历视图 -->
      <div class="week-view" v-if="currentView === 'week'">
        <div class="week-header">
          <div class="day-header" v-for="day in weekDays" :key="day.date">
            <div class="day-date">{{ day.date.format('MM-DD') }}</div>
            <div class="day-week">{{ day.weekday }}</div>
          </div>
        </div>
        <div class="week-content">
          <div class="day-column" v-for="day in weekDays" :key="day.date">
            <div class="day-events">
              <div 
                v-for="event in getDayEvents(day.date)" 
                :key="event.id"
                class="event-item"
                :class="event.type"
                @click="showEventDetail(event)"
              >
                <div class="event-time">{{ event.time }}</div>
                <div class="event-title">{{ event.title }}</div>
                <div class="event-customer">{{ event.customer }}</div>
              </div>
              <div class="no-events" v-if="getDayEvents(day.date).length === 0">
                无安排
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 日历视图 -->
      <div class="month-view" v-else>
        <div class="month-header">
          <div class="weekday-header" v-for="weekday in weekdays" :key="weekday">
            {{ weekday }}
          </div>
        </div>
        <div class="month-grid">
          <div 
            v-for="day in monthDays" 
            :key="day.date"
            class="month-day"
            :class="{ 'other-month': !isCurrentMonth(day.date), 'today': isToday(day.date) }"
            @click="selectDate(day.date)"
          >
            <div class="day-number">{{ day.date.date() }}</div>
            <div class="day-events-month">
              <div 
                v-for="event in getDayEvents(day.date)" 
                :key="event.id"
                class="event-item-month"
                :class="event.type"
                @click.stop="showEventDetail(event)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 事件详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      :title="selectedEvent ? selectedEvent.title : '事件详情'"
      width="500px"
    >
      <div v-if="selectedEvent" class="event-detail">
        <el-descriptions :column="1">
          <el-descriptions-item label="日期">
            {{ selectedEvent.date }}
          </el-descriptions-item>
          <el-descriptions-item label="时间">
            {{ selectedEvent.time }}
          </el-descriptions-item>
          <el-descriptions-item label="客户">
            {{ selectedEvent.customer }}
          </el-descriptions-item>
          <el-descriptions-item label="类型">
            {{ selectedEvent.type === 'meal' ? '餐食安排' : '服务预定' }}
          </el-descriptions-item>
          <el-descriptions-item label="详情">
            {{ selectedEvent.detail }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedEvent.status === 'confirmed' ? 'success' : 'warning'">
              {{ selectedEvent.status === 'confirmed' ? '已确认' : '待确认' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDetailDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import dayjs from 'dayjs'
import { ArrowLeft, ArrowRight, Position } from '@element-plus/icons-vue'

export default {
  name: 'CalendarView',
  setup() {
    // 状态管理
    const currentDate = ref(dayjs())
    const currentView = ref('week')
    const eventFilter = ref('all')
    const showDetailDialog = ref(false)
    const selectedEvent = ref(null)
    
    // 周几显示
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    
    // 计算周开始和结束日期
    const weekStart = computed(() => {
      return currentDate.value.startOf('week')
    })
    
    const weekEnd = computed(() => {
      return currentDate.value.endOf('week')
    })
    
    // 生成周历的日期数组
    const weekDays = computed(() => {
      const days = []
      let current = weekStart.value
      for (let i = 0; i < 7; i++) {
        days.push({
          date: current,
          weekday: weekdays[current.day()]
        })
        current = current.add(1, 'day')
      }
      return days
    })
    
    // 生成日历的日期数组
    const monthDays = computed(() => {
      const days = []
      const firstDay = currentDate.value.startOf('month')
      const lastDay = currentDate.value.endOf('month')
      
      // 添加上月的日期
      let start = firstDay.startOf('week')
      
      // 生成整个月的日期
      for (let i = 0; i < 42; i++) { // 6 rows * 7 days
        days.push({
          date: start
        })
        start = start.add(1, 'day')
      }
      
      return days
    })
    
    // 模拟事件数据
    const events = ref([
      {
        id: 1,
        date: dayjs().format('YYYY-MM-DD'),
        time: '08:00',
        title: '早餐',
        customer: '张女士',
        type: 'meal',
        detail: '小米粥、鸡蛋、包子',
        status: 'confirmed'
      },
      {
        id: 2,
        date: dayjs().format('YYYY-MM-DD'),
        time: '12:00',
        title: '午餐',
        customer: '张女士',
        type: 'meal',
        detail: '鸡汤、米饭、蔬菜',
        status: 'confirmed'
      },
      {
        id: 3,
        date: dayjs().format('YYYY-MM-DD'),
        time: '15:00',
        title: '产后修复',
        customer: '张女士',
        type: 'service',
        detail: '产后修复按摩',
        status: 'confirmed'
      },
      {
        id: 4,
        date: dayjs().add(1, 'day').format('YYYY-MM-DD'),
        time: '08:00',
        title: '早餐',
        customer: '李女士',
        type: 'meal',
        detail: '豆浆、油条、鸡蛋',
        status: 'confirmed'
      },
      {
        id: 5,
        date: dayjs().add(1, 'day').format('YYYY-MM-DD'),
        time: '12:00',
        title: '午餐',
        customer: '李女士',
        type: 'meal',
        detail: '排骨汤、米饭、蔬菜',
        status: 'confirmed'
      }
    ])
    
    // 获取指定日期的事件
    const getDayEvents = (date) => {
      const dateStr = date.format('YYYY-MM-DD')
      let filteredEvents = events.value.filter(event => event.date === dateStr)
      
      // 根据过滤条件筛选事件
      if (eventFilter.value === 'meal') {
        filteredEvents = filteredEvents.filter(event => event.type === 'meal')
      } else if (eventFilter.value === 'service') {
        filteredEvents = filteredEvents.filter(event => event.type === 'service')
      }
      
      return filteredEvents
    }
    
    // 切换视图
    const switchView = () => {
      // 视图切换时的逻辑
    }
    
    // 导航到上一周期
    const prevPeriod = () => {
      if (currentView.value === 'week') {
        currentDate.value = currentDate.value.subtract(1, 'week')
      } else {
        currentDate.value = currentDate.value.subtract(1, 'month')
      }
    }
    
    // 导航到下一周期
    const nextPeriod = () => {
      if (currentView.value === 'week') {
        currentDate.value = currentDate.value.add(1, 'week')
      } else {
        currentDate.value = currentDate.value.add(1, 'month')
      }
    }
    
    // 回到今天
    const today = () => {
      currentDate.value = dayjs()
    }
    
    // 检查是否是当前月份
    const isCurrentMonth = (date) => {
      return date.month() === currentDate.value.month() && date.year() === currentDate.value.year()
    }
    
    // 检查是否是今天
    const isToday = (date) => {
      return date.isSame(dayjs(), 'day')
    }
    
    // 选择日期
    const selectDate = (date) => {
      currentDate.value = date
      if (currentView.value === 'week') {
        // 切换到包含所选日期的周
        currentDate.value = date.startOf('week')
      }
    }
    
    // 显示事件详情
    const showEventDetail = (event) => {
      selectedEvent.value = event
      showDetailDialog.value = true
    }
    
    // 初始化
    onMounted(() => {
      // 可以在这里加载真实数据
      console.log('服务日历初始化')
    })
    
    return {
      currentDate,
      currentView,
      eventFilter,
      weekStart,
      weekEnd,
      weekDays,
      monthDays,
      weekdays,
      showDetailDialog,
      selectedEvent,
      switchView,
      prevPeriod,
      nextPeriod,
      today,
      isCurrentMonth,
      isToday,
      selectDate,
      getDayEvents,
      showEventDetail
    }
  }
}
</script>

<style scoped>
.calendar-container {
  padding: 20px;
}

.calendar-card {
  margin-bottom: 20px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-header h2 {
  margin: 0;
  color: #333;
}

.view-controls {
  margin-left: 20px;
}

.calendar-navigation {
  display: flex;
  align-items: center;
  margin: 20px 0;
  gap: 10px;
}

.current-period {
  margin-left: 20px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

/* 周历视图 */
.week-view {
  margin-top: 20px;
}

.week-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}

.day-header {
  text-align: center;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.day-date {
  font-weight: bold;
  font-size: 14px;
}

.day-week {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.week-content {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
  min-height: 400px;
}

.day-column {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.day-events {
  padding: 10px;
  min-height: 380px;
}

.event-item {
  padding: 8px;
  margin-bottom: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.event-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.event-item.meal {
  background-color: #ecf5ff;
  border-left: 4px solid #409eff;
}

.event-item.service {
  background-color: #f0f9eb;
  border-left: 4px solid #67c23a;
}

.event-time {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.event-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 4px;
}

.event-customer {
  font-size: 12px;
  color: #909399;
}

.no-events {
  text-align: center;
  color: #909399;
  font-size: 14px;
  margin-top: 20px;
}

/* 日历视图 */
.month-view {
  margin-top: 20px;
}

.month-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #ebeef5;
  margin-bottom: 1px;
}

.weekday-header {
  padding: 10px;
  text-align: center;
  background-color: #f5f7fa;
  font-weight: bold;
  color: #333;
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #ebeef5;
  min-height: 400px;
}

.month-day {
  background-color: #fff;
  padding: 10px;
  min-height: 100px;
  cursor: pointer;
  transition: all 0.3s;
}

.month-day:hover {
  background-color: #f5f7fa;
}

.month-day.other-month {
  background-color: #fafafa;
}

.month-day.today {
  background-color: #ecf5ff;
  border: 1px solid #409eff;
}

.day-number {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.other-month .day-number {
  color: #c0c4cc;
}

.today .day-number {
  color: #409eff;
}

.day-events-month {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.event-item-month {
  padding: 4px;
  font-size: 12px;
  border-radius: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}

.event-item-month.meal {
  background-color: #ecf5ff;
  color: #409eff;
}

.event-item-month.service {
  background-color: #f0f9eb;
  color: #67c23a;
}

/* 事件详情 */
.event-detail {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .week-content {
    min-height: 300px;
  }
  
  .day-events {
    min-height: 280px;
  }
}

@media (max-width: 768px) {
  .calendar-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .view-controls {
    margin-left: 0;
  }
  
  .calendar-navigation {
    flex-wrap: wrap;
  }
  
  .week-content {
    font-size: 12px;
  }
  
  .event-item {
    padding: 6px;
  }
}
</style>