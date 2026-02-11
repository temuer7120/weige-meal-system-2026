<template>
  <div class="customer-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>客户管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddCustomer">添加客户</el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="客户姓名">
          <el-input v-model="searchForm.name" placeholder="请输入客户姓名" style="width: 200px"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话">
          <el-input v-model="searchForm.phone" placeholder="请输入联系电话" style="width: 200px"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 客户列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>客户列表</span>
          <span class="total-count">共 {{ customers.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="customers" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="客户姓名"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="150"></el-table-column>
        <el-table-column prop="gender" label="性别" width="80"></el-table-column>
        <el-table-column prop="age" label="年龄" width="80"></el-table-column>
        <el-table-column label="产后时期" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.delivery_date" type="info">{{ calculatePostpartumPeriod(scope.row.delivery_date) }}</el-tag>
            <span v-else>未设置</span>
          </template>
        </el-table-column>
        <el-table-column label="饮食禁忌" width="180">
          <template #default="scope">
            <el-tooltip :content="scope.row.dietary_restrictions || '无'" placement="top">
              <span>{{ (scope.row.dietary_restrictions || '无').length > 10 ? (scope.row.dietary_restrictions.substring(0, 10) + '...') : (scope.row.dietary_restrictions || '无') }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="服务禁忌" width="180">
          <template #default="scope">
            <el-tooltip :content="scope.row.service_restrictions || '无'" placement="top">
              <span>{{ (scope.row.service_restrictions || '无').length > 10 ? (scope.row.service_restrictions.substring(0, 10) + '...') : (scope.row.service_restrictions || '无') }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="过敏史" width="180">
          <template #default="scope">
            <el-tooltip :content="scope.row.allergies || '无'" placement="top">
              <span>{{ (scope.row.allergies || '无').length > 10 ? (scope.row.allergies.substring(0, 10) + '...') : (scope.row.allergies || '无') }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="宝宝信息" width="180">
          <template #default="scope">
            <el-tooltip :content="scope.row.baby_name ? `${scope.row.baby_name} (${scope.row.baby_gender || '性别未知'})` : '无'" placement="top">
              <span>{{ scope.row.baby_name || '无' }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditCustomer(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDeleteCustomer(scope.row.id)">删除</el-button>
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
    
    <!-- 添加/编辑客户对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="客户姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入客户姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        
        <el-form-item label="性别" prop="gender">
          <el-select v-model="formData.gender" placeholder="请选择性别">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="年龄" prop="age">
          <el-input v-model.number="formData.age" placeholder="请输入年龄" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="分娩日期">
          <el-date-picker v-model="formData.delivery_date" type="date" placeholder="请选择分娩日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="入住日期">
          <el-date-picker v-model="formData.check_in_date" type="date" placeholder="请选择入住日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="退房日期">
          <el-date-picker v-model="formData.check_out_date" type="date" placeholder="请选择退房日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="健康状况">
          <el-input v-model="formData.health_status" type="textarea" placeholder="请输入健康状况"></el-input>
        </el-form-item>
        
        <el-form-item label="饮食禁忌" prop="dietary_restrictions">
          <el-input v-model="formData.dietary_restrictions" type="textarea" placeholder="请输入饮食禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="服务禁忌">
          <el-input v-model="formData.service_restrictions" type="textarea" placeholder="请输入服务禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="饮食偏好">
          <el-input v-model="formData.preferences" type="textarea" placeholder="请输入饮食偏好"></el-input>
        </el-form-item>
        
        <el-form-item label="过敏史">
          <el-input v-model="formData.allergies" type="textarea" placeholder="请输入过敏史"></el-input>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="formData.notes" type="textarea" placeholder="请输入备注"></el-input>
        </el-form-item>
        
        <el-form-item label="产后时期" v-if="formData.delivery_date">
          <el-tag type="info">{{ calculatePostpartumPeriod(formData.delivery_date) }}</el-tag>
        </el-form-item>
        
        <!-- 宝宝信息 -->
        <el-form-item label="宝宝姓名">
          <el-input v-model="formData.baby_name" placeholder="请输入宝宝姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="宝宝性别">
          <el-select v-model="formData.baby_gender" placeholder="请选择宝宝性别">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="宝宝出生日期">
          <el-date-picker v-model="formData.baby_birth_date" type="date" placeholder="请选择宝宝出生日期" style="width: 100%"></el-date-picker>
        </el-form-item>
        
        <el-form-item label="宝宝健康状况">
          <el-input v-model="formData.baby_health_status" type="textarea" placeholder="请输入宝宝健康状况"></el-input>
        </el-form-item>
        
        <el-form-item label="宝宝特殊需求">
          <el-input v-model="formData.baby_special_needs" type="textarea" placeholder="请输入宝宝特殊需求"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'CustomerManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      phone: ''
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 客户数据
    const customers = ref([
      {
        id: 1,
        name: '张三',
        phone: '13800138000',
        gender: '女',
        age: 30,
        delivery_date: '2026-01-15',
        check_in_date: '2026-01-16',
        check_out_date: '2026-02-16',
        health_status: '健康',
        dietary_restrictions: '海鲜过敏',
        service_restrictions: '无',
        preferences: '清淡饮食',
        allergies: '海鲜',
        notes: 'VIP客户',
        baby_name: '张宝宝',
        baby_gender: '男',
        baby_birth_date: '2026-01-15',
        baby_health_status: '健康',
        baby_special_needs: '无'
      },
      {
        id: 2,
        name: '李四',
        phone: '13900139000',
        gender: '女',
        age: 25,
        delivery_date: '2026-01-20',
        check_in_date: '2026-01-21',
        check_out_date: '2026-02-21',
        health_status: '健康',
        dietary_restrictions: '辛辣食物',
        service_restrictions: '无',
        preferences: '温补饮食',
        allergies: '无',
        notes: '新客户',
        baby_name: '李宝宝',
        baby_gender: '女',
        baby_birth_date: '2026-01-20',
        baby_health_status: '健康',
        baby_special_needs: '无'
      }
    ])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加客户')
    const formData = reactive({})
    const formRef = ref(null)
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
      gender: [{ required: true, message: '请选择性别', trigger: 'blur' }],
      age: [{ required: true, message: '请输入年龄', trigger: 'blur', type: 'number' }],
      dietary_restrictions: [{ required: true, message: '请输入饮食禁忌', trigger: 'blur' }]
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.phone = ''
    }
    
    // 处理添加客户
    const handleAddCustomer = () => {
      dialogTitle.value = '添加客户'
      // 重置表单
      Object.assign(formData, {
        name: '',
        phone: '',
        gender: '',
        age: 0,
        delivery_date: '',
        check_in_date: '',
        check_out_date: '',
        health_status: '',
        dietary_restrictions: '',
        service_restrictions: '',
        preferences: '',
        allergies: '',
        notes: '',
        baby_name: '',
        baby_gender: '',
        baby_birth_date: '',
        baby_health_status: '',
        baby_special_needs: ''
      })
      dialogVisible.value = true
    }
    
    // 处理编辑客户
    const handleEditCustomer = (customer) => {
      dialogTitle.value = '编辑客户'
      // 填充表单数据
      Object.assign(formData, { ...customer })
      dialogVisible.value = true
    }
    
    // 处理提交
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        console.log('表单数据', formData)
        // 这里可以添加实际的提交逻辑
        dialogVisible.value = false
        // 刷新数据
        // fetchCustomers()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理删除客户
    const handleDeleteCustomer = (id) => {
      ElMessageBox.confirm('确定要删除该客户吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除客户', id)
        // 这里可以添加实际的删除逻辑
        // fetchCustomers()
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入客户')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出客户')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      // 刷新数据
      // fetchCustomers()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchCustomers()
    }
    
    // 获取客户数据
    const fetchCustomers = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/customers')
        // customers.value = response.data
      } catch (error) {
        console.log('获取客户数据失败', error)
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
      // fetchCustomers()
    })
    
    return {
      searchForm,
      customers,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      formData,
      formRef,
      formRules,
      calculatePostpartumPeriod,
      handleSearch,
      resetSearch,
      handleAddCustomer,
      handleEditCustomer,
      handleSubmit,
      handleDeleteCustomer,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.customer-management {
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
}
</style>