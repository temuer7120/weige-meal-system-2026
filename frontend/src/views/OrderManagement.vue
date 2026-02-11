<template>
  <div class="order-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>订单管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddOrder">创建订单</el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="订单ID">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单ID" style="width: 150px"></el-input>
        </el-form-item>
        
        <el-form-item label="订单类型">
          <el-select v-model="searchForm.orderType" placeholder="请选择订单类型" style="width: 150px">
            <el-option label="餐食订单" value="meal"></el-option>
            <el-option label="服务订单" value="service"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="订单状态">
          <el-select v-model="searchForm.status" placeholder="请选择订单状态" style="width: 150px">
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="已确认" value="confirmed"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="客户名称">
          <el-select v-model="searchForm.customerName" placeholder="请选择客户名称" style="width: 200px">
            <el-option v-for="customer in customers" :key="customer.id" :label="customer.name" :value="customer.name"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 250px"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 订单列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>订单列表</span>
          <span class="total-count">共 {{ orders.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="id" label="订单ID" width="100"></el-table-column>
        <el-table-column label="订单类型" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.order_type === 'meal' ? 'success' : 'primary'">
              {{ scope.row.order_type === 'meal' ? '餐食订单' : '服务订单' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="customer_name" label="客户名称"></el-table-column>
        <el-table-column prop="booker_name" label="预定人" width="120"></el-table-column>
        <el-table-column prop="total_amount" label="金额" width="100">
          <template #default="scope">
            ¥{{ scope.row.total_amount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="支付方式" width="120"></el-table-column>
        <el-table-column prop="order_date" label="下单时间"></el-table-column>
        <el-table-column prop="delivery_date" label="配送/服务日期" width="150"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleViewOrder(scope.row)">查看</el-button>
            <el-button type="success" size="small" v-if="scope.row.status === 'pending'" @click="handleConfirmOrder(scope.row.id)">确认</el-button>
            <el-button type="warning" size="small" v-if="scope.row.payment_status === 'pending'" @click="handlePayOrder(scope.row)">支付</el-button>
            <el-button type="danger" size="small" v-if="scope.row.status === 'pending'" @click="handleCancelOrder(scope.row.id)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        />
      </div>
    </el-card>
    
    <!-- 订单详情对话框 -->
    <el-dialog
      title="订单详情"
      :visible.sync="detailDialogVisible"
      width="800px"
    >
      <div class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单ID">{{ selectedOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="订单类型">{{ selectedOrder.order_type === 'meal' ? '餐食订单' : '服务订单' }}</el-descriptions-item>
          <el-descriptions-item label="客户名称">{{ selectedOrder.customer_name }}</el-descriptions-item>
          <el-descriptions-item label="预定人">{{ selectedOrder.booker_name }}</el-descriptions-item>
          <el-descriptions-item label="预定人角色">{{ selectedOrder.booker_role }}</el-descriptions-item>
          <el-descriptions-item label="服务员工">{{ selectedOrder.service_employee_name }}</el-descriptions-item>
          <el-descriptions-item label="总金额">¥{{ selectedOrder.total_amount }}</el-descriptions-item>
          <el-descriptions-item label="支付状态">{{ selectedOrder.payment_status === 'paid' ? '已支付' : '待支付' }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ selectedOrder.payment_method || '未支付' }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">{{ getStatusText(selectedOrder.status) }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ selectedOrder.order_date }}</el-descriptions-item>
          <el-descriptions-item label="配送/服务日期">{{ selectedOrder.delivery_date }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ selectedOrder.start_time }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ selectedOrder.end_time }}</el-descriptions-item>
          <el-descriptions-item label="时长">{{ selectedOrder.duration }}小时</el-descriptions-item>
          <el-descriptions-item label="配送地址">{{ selectedOrder.delivery_address || '无' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedOrder.notes || '无' }}</el-descriptions-item>
          <el-descriptions-item label="评价" :span="2">{{ selectedOrder.feedback || '无' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 订单项目 -->
        <h3 style="margin-top: 20px; margin-bottom: 10px">订单项目</h3>
        <el-table :data="selectedOrder.items" style="width: 100%">
          <el-table-column prop="item_type" label="项目类型" width="100"></el-table-column>
          <el-table-column prop="name" label="项目名称"></el-table-column>
          <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
          <el-table-column prop="price" label="单价" width="100">
            <template #default="scope">
              ¥{{ scope.row.price }}
            </template>
          </el-table-column>
          <el-table-column prop="subtotal" label="小计" width="100">
            <template #default="scope">
              ¥{{ scope.row.subtotal }}
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 支付对话框 -->
    <el-dialog
      title="订单支付"
      :visible.sync="payDialogVisible"
      width="500px"
    >
      <div class="pay-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="订单ID">{{ payOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ payOrder.total_amount }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">{{ payOrder.payment_status === 'paid' ? '已支付' : '待支付' }}</el-descriptions-item>
        </el-descriptions>
        
        <h3 style="margin-top: 20px; margin-bottom: 10px">选择支付方式</h3>
        <el-radio-group v-model="paymentMethod">
          <el-radio label="wechat">微信支付</el-radio>
          <el-radio label="alipay">支付宝</el-radio>
          <el-radio label="bank">银行卡支付</el-radio>
        </el-radio-group>
        
        <div class="pay-qr" v-if="paymentMethod === 'wechat'">
          <h4 style="margin-top: 20px; margin-bottom: 10px">微信支付二维码</h4>
          <div class="qr-code">
            <img src="https://via.placeholder.com/200" alt="微信支付二维码">
          </div>
          <p style="text-align: center; margin-top: 10px">请扫描二维码支付</p>
        </div>
        
        <div class="pay-qr" v-else-if="paymentMethod === 'alipay'">
          <h4 style="margin-top: 20px; margin-bottom: 10px">支付宝二维码</h4>
          <div class="qr-code">
            <img src="https://via.placeholder.com/200" alt="支付宝二维码">
          </div>
          <p style="text-align: center; margin-top: 10px">请扫描二维码支付</p>
        </div>
        
        <div class="bank-form" v-else-if="paymentMethod === 'bank'">
          <h4 style="margin-top: 20px; margin-bottom: 10px">银行卡信息</h4>
          <el-form :model="bankForm" :rules="bankRules" ref="bankFormRef" label-width="100px">
            <el-form-item label="银行卡号" prop="cardNumber">
              <el-input v-model="bankForm.cardNumber" placeholder="请输入银行卡号"></el-input>
            </el-form-item>
            <el-form-item label="持卡人" prop="cardHolder">
              <el-input v-model="bankForm.cardHolder" placeholder="请输入持卡人姓名"></el-input>
            </el-form-item>
            <el-form-item label="有效期" prop="expiryDate">
              <el-input v-model="bankForm.expiryDate" placeholder="请输入有效期，如：12/26"></el-input>
            </el-form-item>
            <el-form-item label="CVV码" prop="cvv">
              <el-input v-model="bankForm.cvv" placeholder="请输入CVV码" style="width: 150px"></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="payDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handlePaymentSubmit">确认支付</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 创建订单对话框 -->
    <el-dialog
      title="创建订单"
      :visible.sync="createDialogVisible"
      width="800px"
    >
      <el-form :model="createOrderForm" :rules="createOrderRules" ref="createOrderFormRef" label-width="100px">
        <el-form-item label="订单类型" prop="order_type">
          <el-select v-model="createOrderForm.order_type" placeholder="请选择订单类型">
            <el-option label="餐食订单" value="meal"></el-option>
            <el-option label="服务订单" value="service"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="客户姓名" prop="customer_id">
          <el-select v-model="createOrderForm.customer_id" placeholder="请选择客户姓名" @change="handleCustomerChange">
            <el-option v-for="customer in customers" :key="customer.id" :label="customer.name" :value="customer.id"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="客户禁忌" v-if="selectedCustomer.dietary_restrictions">
          <el-alert
            :title="'饮食禁忌：' + selectedCustomer.dietary_restrictions"
            type="warning"
            :closable="false"
          />
        </el-form-item>
        
        <el-form-item label="服务禁忌" v-if="selectedCustomer.service_restrictions && selectedCustomer.service_restrictions !== '无'">
          <el-alert
            :title="'服务禁忌：' + selectedCustomer.service_restrictions"
            type="warning"
            :closable="false"
          />
        </el-form-item>
        
        <el-form-item label="产后时期" v-if="selectedCustomer.delivery_date">
          <el-alert
            :title="'产后时期：' + calculatePostpartumPeriod(selectedCustomer.delivery_date)"
            type="info"
            :closable="false"
          />
        </el-form-item>
        
        <el-form-item label="预定人" prop="booker_name">
          <el-input v-model="createOrderForm.booker_name" placeholder="请输入预定人姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="预定人角色" prop="booker_role">
          <el-select v-model="createOrderForm.booker_role" placeholder="请选择预定人角色">
            <el-option label="客户" value="customer"></el-option>
            <el-option label="员工" value="employee"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="服务员工" prop="service_employee_id">
          <el-select v-model="createOrderForm.service_employee_id" placeholder="请选择服务员工">
            <el-option label="张三" value="1"></el-option>
            <el-option label="李四" value="2"></el-option>
            <el-option label="王五" value="3"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="配送/服务日期" prop="delivery_date">
          <el-date-picker v-model="createOrderForm.delivery_date" type="date" placeholder="请选择日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="开始时间" prop="start_time">
          <el-time-picker v-model="createOrderForm.start_time" placeholder="请选择开始时间" style="width: 100%"></el-time-picker>
        </el-form-item>
        
        <el-form-item label="结束时间" prop="end_time">
          <el-time-picker v-model="createOrderForm.end_time" placeholder="请选择结束时间" style="width: 100%"></el-time-picker>
        </el-form-item>
        
        <el-form-item label="配送地址" prop="delivery_address">
          <el-input v-model="createOrderForm.delivery_address" type="textarea" placeholder="请输入配送地址"></el-input>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="createOrderForm.notes" type="textarea" placeholder="请输入备注"></el-input>
        </el-form-item>
        
        <el-form-item label="订单项目" prop="items">
          <el-table :data="createOrderForm.items" style="width: 100%">
            <el-table-column prop="item_type" label="项目类型" width="100">
              <template #default="scope">
                <el-select v-model="scope.row.item_type" placeholder="请选择类型">
                  <el-option label="菜品" value="dish"></el-option>
                  <el-option label="菜单" value="menu"></el-option>
                  <el-option label="服务" value="service"></el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="item_id" label="项目名称">
              <template #default="scope">
                <el-select v-model="scope.row.item_id" placeholder="请选择项目" @change="handleItemChange(scope.row)">
                  <el-option v-for="dish in dishes" :key="dish.id" :label="dish.name" :value="dish.id" v-if="scope.row.item_type === 'dish'"></el-option>
                  <el-option v-for="menu in menus" :key="menu.id" :label="menu.name" :value="menu.id" v-if="scope.row.item_type === 'menu'"></el-option>
                  <el-option v-for="service in services" :key="service.id" :label="service.name" :value="service.id" v-if="scope.row.item_type === 'service'"></el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="100">
              <template #default="scope">
                <el-input v-model.number="scope.row.quantity" type="number" min="1"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="单价" width="100">
              <template #default="scope">
                <el-input v-model.number="scope.row.price" type="number" min="0"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="subtotal" label="小计" width="100">
              <template #default="scope">
                ¥{{ (scope.row.quantity || 0) * (scope.row.price || 0) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button type="danger" size="small" @click="removeOrderItem(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-button type="primary" size="small" @click="addOrderItem" style="margin-top: 10px">添加项目</el-button>
        </el-form-item>
        
        <el-form-item label="总金额" prop="total_amount">
          <el-input v-model.number="createOrderForm.total_amount" placeholder="请输入总金额" type="number"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateOrderSubmit">创建订单</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../services/api'

export default {
  name: 'OrderManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      orderId: '',
      orderType: '',
      status: '',
      customerName: '',
      dateRange: []
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 入住客户列表
    const customers = ref([
      { id: 1, name: '张三', dietary_restrictions: '海鲜过敏', service_restrictions: '无', health_status: '健康' },
      { id: 2, name: '李四', dietary_restrictions: '辛辣食物', service_restrictions: '无', health_status: '健康' },
      { id: 3, name: '王五', dietary_restrictions: '无', service_restrictions: '无', health_status: '健康' },
      { id: 4, name: '赵六', dietary_restrictions: '乳糖不耐', service_restrictions: '无', health_status: '健康' },
      { id: 5, name: '孙七', dietary_restrictions: '花生过敏', service_restrictions: '无', health_status: '健康' }
    ])
    
    // 菜品列表
    const dishes = ref([
      { id: 1, name: '宫保鸡丁', price: 48, restrictions: '辛辣', suitable_for: '无禁忌' },
      { id: 2, name: '麻婆豆腐', price: 38, restrictions: '辛辣', suitable_for: '无禁忌' },
      { id: 3, name: '米饭', price: 5, restrictions: '无', suitable_for: '无禁忌' },
      { id: 4, name: '可乐', price: 12, restrictions: '含咖啡因', suitable_for: '无禁忌' },
      { id: 5, name: '海鲜炒饭', price: 58, restrictions: '海鲜', suitable_for: '无海鲜过敏' }
    ])
    
    // 菜单列表
    const menus = ref([
      { id: 1, name: '营养早餐套餐', price: 88, restrictions: '无', suitable_for: '所有人群' },
      { id: 2, name: '健康午餐套餐', price: 128, restrictions: '无', suitable_for: '所有人群' },
      { id: 3, name: '海鲜晚餐套餐', price: 198, restrictions: '海鲜', suitable_for: '无海鲜过敏' }
    ])
    
    // 服务列表
    const services = ref([
      { id: 1, name: '母婴护理', price: 298, restrictions: '无', suitable_for: '产妇和婴儿' },
      { id: 2, name: '老人陪护', price: 258, restrictions: '无', suitable_for: '老年人' },
      { id: 3, name: '康复护理', price: 398, restrictions: '无', suitable_for: '康复期病人' }
    ])
    
    // 选中的客户
    const selectedCustomer = ref({})
    
    // 创建订单对话框
    const createDialogVisible = ref(false)
    const createOrderForm = reactive({
      order_type: 'meal',
      customer_id: '',
      booker_name: '',
      booker_role: 'customer',
      service_employee_id: '',
      delivery_date: '',
      start_time: '',
      end_time: '',
      delivery_address: '',
      notes: '',
      items: [],
      total_amount: 0
    })
    const createOrderFormRef = ref(null)
    
    const createOrderRules = {
      order_type: [{ required: true, message: '请选择订单类型', trigger: 'blur' }],
      customer_id: [{ required: true, message: '请选择客户姓名', trigger: 'blur' }],
      booker_name: [{ required: true, message: '请输入预定人姓名', trigger: 'blur' }],
      booker_role: [{ required: true, message: '请选择预定人角色', trigger: 'blur' }],
      service_employee_id: [{ required: true, message: '请选择服务员工', trigger: 'blur' }],
      delivery_date: [{ required: true, message: '请选择配送/服务日期', trigger: 'blur' }],
      start_time: [{ required: true, message: '请选择开始时间', trigger: 'blur' }],
      end_time: [{ required: true, message: '请选择结束时间', trigger: 'blur' }],
      items: [{ required: true, message: '请添加订单项目', trigger: 'blur' }],
      total_amount: [{ required: true, message: '请输入总金额', trigger: 'blur', type: 'number' }]
    }
    
    // 订单数据
    const orders = ref([
      {
        id: 1001,
        order_type: 'meal',
        customer_name: '张三',
        booker_name: '张三',
        booker_role: 'customer',
        service_employee_name: '李四',
        total_amount: 128,
        status: 'completed',
        payment_status: 'paid',
        payment_method: 'wechat',
        order_date: '2026-02-09 10:30',
        delivery_date: '2026-02-09',
        start_time: '12:00',
        end_time: '13:00',
        duration: 1,
        delivery_address: '北京市朝阳区XX街道XX小区XX号楼XX单元XX室',
        notes: '不要辣',
        feedback: '菜品味道很好，配送及时',
        items: [
          { item_type: 'dish', name: '宫保鸡丁', quantity: 1, price: 48, subtotal: 48 },
          { item_type: 'dish', name: '麻婆豆腐', quantity: 1, price: 38, subtotal: 38 },
          { item_type: 'dish', name: '米饭', quantity: 2, price: 5, subtotal: 10 },
          { item_type: 'dish', name: '可乐', quantity: 1, price: 12, subtotal: 12 }
        ]
      },
      {
        id: 1002,
        order_type: 'service',
        customer_name: '李四',
        booker_name: '王五',
        booker_role: 'employee',
        service_employee_name: '赵六',
        total_amount: 298,
        status: 'confirmed',
        payment_status: 'pending',
        payment_method: '',
        order_date: '2026-02-09 09:15',
        delivery_date: '2026-02-10',
        start_time: '14:00',
        end_time: '16:00',
        duration: 2,
        delivery_address: '北京市海淀区XX街道XX小区XX号楼XX单元XX室',
        notes: '需要专业的母婴护理服务',
        feedback: '',
        items: [
          { item_type: 'service', name: '母婴护理', quantity: 1, price: 298, subtotal: 298 }
        ]
      },
      {
        id: 1003,
        order_type: 'meal',
        customer_name: '王五',
        booker_name: '王五',
        booker_role: 'customer',
        service_employee_name: '李四',
        total_amount: 88,
        status: 'completed',
        payment_status: 'paid',
        payment_method: 'alipay',
        order_date: '2026-02-09 08:45',
        delivery_date: '2026-02-09',
        start_time: '09:30',
        end_time: '10:30',
        duration: 1,
        delivery_address: '北京市西城区XX街道XX小区XX号楼XX单元XX室',
        notes: '早餐，要清淡',
        feedback: '早餐很丰富，味道不错',
        items: [
          { item_type: 'menu', name: '营养早餐套餐', quantity: 1, price: 88, subtotal: 88 }
        ]
      }
    ])
    
    // 对话框相关
    const detailDialogVisible = ref(false)
    const selectedOrder = ref({})
    
    const payDialogVisible = ref(false)
    const payOrder = ref({})
    const paymentMethod = ref('wechat')
    
    const bankForm = reactive({
      cardNumber: '',
      cardHolder: '',
      expiryDate: '',
      cvv: ''
    })
    const bankFormRef = ref(null)
    
    const bankRules = {
      cardNumber: [{ required: true, message: '请输入银行卡号', trigger: 'blur' }],
      cardHolder: [{ required: true, message: '请输入持卡人姓名', trigger: 'blur' }],
      expiryDate: [{ required: true, message: '请输入有效期', trigger: 'blur' }],
      cvv: [{ required: true, message: '请输入CVV码', trigger: 'blur' }]
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'pending': return 'warning'
        case 'confirmed': return 'primary'
        case 'completed': return 'success'
        case 'cancelled': return 'danger'
        default: return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'pending': return '待处理'
        case 'confirmed': return '已确认'
        case 'completed': return '已完成'
        case 'cancelled': return '已取消'
        default: return '未知'
      }
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.orderId = ''
      searchForm.orderType = ''
      searchForm.status = ''
      searchForm.customerName = ''
      searchForm.dateRange = []
    }
    
    // 处理查看订单
    const handleViewOrder = (order) => {
      selectedOrder.value = { ...order }
      detailDialogVisible.value = true
    }
    
    // 处理客户变更
    const handleCustomerChange = (customerId) => {
      const customer = customers.value.find(c => c.id === customerId)
      if (customer) {
        selectedCustomer.value = { ...customer }
      } else {
        selectedCustomer.value = {}
      }
    }
    
    // 处理项目变更
    const handleItemChange = (item) => {
      if (item.item_type === 'dish') {
        const dish = dishes.value.find(d => d.id === item.item_id)
        if (dish) {
          item.price = dish.price
          // 检查客户饮食禁忌
          if (selectedCustomer.value.dietary_restrictions && dish.restrictions) {
            const customerRestrictions = selectedCustomer.value.dietary_restrictions.split('、')
            const dishRestrictions = dish.restrictions.split('、')
            const hasConflict = customerRestrictions.some(cr => dishRestrictions.includes(cr))
            if (hasConflict) {
              ElMessage.warning(`警告：该菜品包含客户饮食禁忌内容！`)
            }
          }
        }
      } else if (item.item_type === 'menu') {
        const menu = menus.value.find(m => m.id === item.item_id)
        if (menu) {
          item.price = menu.price
          // 检查客户饮食禁忌
          if (selectedCustomer.value.dietary_restrictions && menu.restrictions) {
            const customerRestrictions = selectedCustomer.value.dietary_restrictions.split('、')
            const menuRestrictions = menu.restrictions.split('、')
            const hasConflict = customerRestrictions.some(cr => menuRestrictions.includes(cr))
            if (hasConflict) {
              ElMessage.warning(`警告：该菜单包含客户饮食禁忌内容！`)
            }
          }
        }
      } else if (item.item_type === 'service') {
        const service = services.value.find(s => s.id === item.item_id)
        if (service) {
          item.price = service.price
          // 检查客户服务禁忌
          if (selectedCustomer.value.service_restrictions && service.restrictions) {
            const customerRestrictions = selectedCustomer.value.service_restrictions.split('、')
            const serviceRestrictions = service.restrictions.split('、')
            const hasConflict = customerRestrictions.some(cr => serviceRestrictions.includes(cr))
            if (hasConflict) {
              ElMessage.warning(`警告：该服务包含客户服务禁忌内容！`)
            }
          }
        }
      }
      // 更新总金额
      updateTotalAmount()
    }
    
    // 添加订单项目
    const addOrderItem = () => {
      createOrderForm.items.push({
        item_type: 'dish',
        item_id: '',
        quantity: 1,
        price: 0
      })
    }
    
    // 删除订单项目
    const removeOrderItem = (index) => {
      createOrderForm.items.splice(index, 1)
      // 更新总金额
      updateTotalAmount()
    }
    
    // 更新总金额
    const updateTotalAmount = () => {
      createOrderForm.total_amount = createOrderForm.items.reduce((total, item) => {
        return total + (item.quantity || 0) * (item.price || 0)
      }, 0)
    }
    
    // 处理添加订单
    const handleAddOrder = () => {
      // 重置表单
      Object.assign(createOrderForm, {
        order_type: 'meal',
        customer_id: '',
        booker_name: '',
        booker_role: 'customer',
        service_employee_id: '',
        delivery_date: '',
        start_time: '',
        end_time: '',
        delivery_address: '',
        notes: '',
        items: [],
        total_amount: 0
      })
      selectedCustomer.value = {}
      createDialogVisible.value = true
    }
    
    // 处理创建订单提交
    const handleCreateOrderSubmit = async () => {
      if (!createOrderFormRef.value) return
      
      try {
        await createOrderFormRef.value.validate()
        
        // 检查所有项目的禁忌内容
        let hasConflict = false
        let conflictItems = []
        
        createOrderForm.items.forEach(item => {
          if (item.item_type === 'dish') {
            const dish = dishes.value.find(d => d.id === item.item_id)
            if (dish && selectedCustomer.value.dietary_restrictions && dish.restrictions) {
              const customerRestrictions = selectedCustomer.value.dietary_restrictions.split('、')
              const dishRestrictions = dish.restrictions.split('、')
              const hasDishConflict = customerRestrictions.some(cr => dishRestrictions.includes(cr))
              if (hasDishConflict) {
                hasConflict = true
                conflictItems.push(`菜品：${dish.name}`)
              }
            }
          } else if (item.item_type === 'menu') {
            const menu = menus.value.find(m => m.id === item.item_id)
            if (menu && selectedCustomer.value.dietary_restrictions && menu.restrictions) {
              const customerRestrictions = selectedCustomer.value.dietary_restrictions.split('、')
              const menuRestrictions = menu.restrictions.split('、')
              const hasMenuConflict = customerRestrictions.some(cr => menuRestrictions.includes(cr))
              if (hasMenuConflict) {
                hasConflict = true
                conflictItems.push(`菜单：${menu.name}`)
              }
            }
          } else if (item.item_type === 'service') {
            const service = services.value.find(s => s.id === item.item_id)
            if (service && selectedCustomer.value.service_restrictions && service.restrictions) {
              const customerRestrictions = selectedCustomer.value.service_restrictions.split('、')
              const serviceRestrictions = service.restrictions.split('、')
              const hasServiceConflict = customerRestrictions.some(cr => serviceRestrictions.includes(cr))
              if (hasServiceConflict) {
                hasConflict = true
                conflictItems.push(`服务：${service.name}`)
              }
            }
          }
        })
        
        if (hasConflict) {
          ElMessageBox.confirm(
            `订单中包含客户禁忌内容：\n${conflictItems.join('\n')}\n是否继续创建？`,
            '警告',
            {
              confirmButtonText: '继续',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).then(() => {
            submitOrder()
          }).catch(() => {
            // 取消创建
          })
        } else {
          submitOrder()
        }
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 提交订单
    const submitOrder = () => {
      console.log('创建订单', createOrderForm)
      // 这里可以添加实际的提交逻辑
      createDialogVisible.value = false
      ElMessage.success('订单创建成功！')
      // 刷新数据
      // fetchOrders()
    }
    
    // 处理确认订单
    const handleConfirmOrder = (orderId) => {
      console.log('确认订单', orderId)
      // 这里可以添加实际的确认订单逻辑
    }
    
    // 处理取消订单
    const handleCancelOrder = (orderId) => {
      console.log('取消订单', orderId)
      // 这里可以添加实际的取消订单逻辑
    }
    
    // 处理支付订单
    const handlePayOrder = (order) => {
      payOrder.value = { ...order }
      paymentMethod.value = 'wechat'
      payDialogVisible.value = true
    }
    
    // 处理支付提交
    const handlePaymentSubmit = async () => {
      if (paymentMethod.value === 'bank' && bankFormRef.value) {
        try {
          await bankFormRef.value.validate()
        } catch (error) {
          console.log('验证失败', error)
          return
        }
      }
      
      console.log('支付方式', paymentMethod.value)
      console.log('订单ID', payOrder.value.id)
      // 这里可以添加实际的支付逻辑
      payDialogVisible.value = false
      // 刷新数据
      // fetchOrders()
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入订单')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出订单')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      // 刷新数据
      // fetchOrders()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchOrders()
    }
    
    // 获取订单数据
    const fetchOrders = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/orders')
        // orders.value = response.data
      } catch (error) {
        console.log('获取订单数据失败', error)
      }
    }
    
    // 计算产后时期
    const calculatePostpartumPeriod = (deliveryDate) => {
      if (!deliveryDate) return '未知'
      
      const delivery = new Date(deliveryDate)
      const now = new Date()
      const diffTime = Math.abs(now - delivery)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays <= 7) {
        return '产后1周'
      } else if (diffDays <= 28) {
        return '产后2-4周'
      } else if (diffDays <= 180) {
        return '产后5-26周'
      } else {
        return '哺乳期'
      }
    }
    
    // 生命周期
    onMounted(() => {
      // 获取数据
      // fetchOrders()
    })
    
    return {
      searchForm,
      orders,
      customers,
      dishes,
      menus,
      services,
      currentPage,
      pageSize,
      total,
      detailDialogVisible,
      selectedOrder,
      payDialogVisible,
      payOrder,
      paymentMethod,
      bankForm,
      bankFormRef,
      bankRules,
      createDialogVisible,
      createOrderForm,
      createOrderFormRef,
      createOrderRules,
      selectedCustomer,
      calculatePostpartumPeriod,
      getStatusType,
      getStatusText,
      handleSearch,
      resetSearch,
      handleViewOrder,
      handleAddOrder,
      handleConfirmOrder,
      handleCancelOrder,
      handlePayOrder,
      handlePaymentSubmit,
      handleCreateOrderSubmit,
      handleCustomerChange,
      handleItemChange,
      addOrderItem,
      removeOrderItem,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.order-management {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-count {
  font-size: 14px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.order-detail {
  padding: 10px 0;
}

.qr-code {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.qr-code img {
  width: 200px;
  height: 200px;
}

.bank-form {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .el-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .el-form-item {
    margin-bottom: 0;
  }
  
  .el-descriptions {
    font-size: 14px;
  }
  
  .el-descriptions-item {
    padding: 8px;
  }
}
</style>
