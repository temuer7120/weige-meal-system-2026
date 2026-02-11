<template>
  <div class="dish-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>菜品管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddDish">
          <el-icon><Plus /></el-icon>
          添加菜品
        </el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="菜品名称">
          <el-input v-model="searchForm.name" placeholder="请输入菜品名称" style="width: 200px"></el-input>
        </el-form-item>
        
        <el-form-item label="类别">
          <el-select v-model="searchForm.category" placeholder="请选择类别" style="width: 150px">
            <el-option label="肉菜" value="肉菜"></el-option>
            <el-option label="蔬菜" value="蔬菜"></el-option>
            <el-option label="汤品" value="汤品"></el-option>
            <el-option label="主食" value="主食"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" style="width: 150px">
            <el-option label="启用" value="active"></el-option>
            <el-option label="禁用" value="inactive"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 菜品列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>菜品列表</span>
          <span class="total-count">共 {{ dishes.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="dishes" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="菜品名称"></el-table-column>
        <el-table-column prop="category" label="类别" width="100"></el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
              {{ scope.row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="回奶风险" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.lactation_risk === '3'" type="danger">高</el-tag>
            <el-tag v-else-if="scope.row.lactation_risk === '2'" type="warning">中</el-tag>
            <el-tag v-else-if="scope.row.lactation_risk === '1'" type="info">低</el-tag>
            <el-tag v-else type="success">无</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditDish(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDeleteDish(scope.row.id)">删除</el-button>
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
    
    <!-- 添加/编辑菜品对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="菜品名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入菜品名称"></el-input>
        </el-form-item>
        
        <el-form-item label="类别" prop="category">
          <el-select v-model="formData.category" placeholder="请选择类别">
            <el-option label="肉菜" value="肉菜"></el-option>
            <el-option label="蔬菜" value="蔬菜"></el-option>
            <el-option label="汤品" value="汤品"></el-option>
            <el-option label="主食" value="主食"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入菜品描述"></el-input>
        </el-form-item>
        
        <el-form-item label="食材组成">
          <el-input v-model="formData.ingredients" type="textarea" placeholder="请输入食材组成"></el-input>
        </el-form-item>
        
        <el-form-item label="禁忌">
          <el-input v-model="formData.restrictions" type="textarea" placeholder="请输入禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="适用人群">
          <el-input v-model="formData.suitable_for" type="textarea" placeholder="请输入适用人群"></el-input>
        </el-form-item>
        
        <el-form-item label="禁忌人群">
          <el-input v-model="formData.not_suitable_for" type="textarea" placeholder="请输入禁忌人群"></el-input>
        </el-form-item>
        
        <el-form-item label="服务禁忌">
          <el-input v-model="formData.service_taboo" type="textarea" placeholder="请输入服务禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="回奶风险等级">
          <el-select v-model="formData.lactation_risk" placeholder="请选择回奶风险等级">
            <el-option label="无" value="0"></el-option>
            <el-option label="低" value="1"></el-option>
            <el-option label="中" value="2"></el-option>
            <el-option label="高" value="3"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="产后时期适配性">
          <el-input v-model="formData.post_partum_suitability" type="textarea" placeholder="请输入产后时期适配性"></el-input>
        </el-form-item>
        
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="formData.price" placeholder="请输入价格" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态">
            <el-option label="启用" value="active"></el-option>
            <el-option label="禁用" value="inactive"></el-option>
          </el-select>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'DishManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      category: '',
      status: ''
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 菜品数据
    const dishes = ref([
      { id: 1, name: '麻油猪肝', category: '肉菜', price: 38, status: 'active', lactation_risk: '0' },
      { id: 2, name: '麻油猪肉片', category: '肉菜', price: 35, status: 'active', lactation_risk: '0' },
      { id: 3, name: '麻油红苋菜', category: '蔬菜', price: 25, status: 'active', lactation_risk: '0' },
      { id: 4, name: '清炒牛心菜', category: '蔬菜', price: 20, status: 'active', lactation_risk: '0' },
      { id: 5, name: '麻油红菜头', category: '蔬菜', price: 22, status: 'active', lactation_risk: '0' },
      { id: 6, name: '虫草花鸡汤', category: '汤品', price: 45, status: 'active', lactation_risk: '0' },
      { id: 7, name: '小米粥', category: '主食', price: 15, status: 'active', lactation_risk: '0' },
      { id: 8, name: '南瓜百合小米粥', category: '主食', price: 18, status: 'active', lactation_risk: '0' },
      { id: 9, name: '薏仁粳米粥', category: '主食', price: 16, status: 'active', lactation_risk: '0' },
      { id: 10, name: '小米粥里少放糯米', category: '主食', price: 17, status: 'active', lactation_risk: '0' },
      { id: 11, name: '韭菜炒蛋', category: '蔬菜', price: 28, status: 'active', lactation_risk: '3' },
      { id: 12, name: '大麦茶', category: '饮品', price: 12, status: 'active', lactation_risk: '3' }
    ])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加菜品')
    const formData = reactive({})
    const formRef = ref(null)
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入菜品名称', trigger: 'blur' }],
      category: [{ required: true, message: '请选择类别', trigger: 'blur' }],
      price: [{ required: true, message: '请输入价格', trigger: 'blur', type: 'number' }],
      status: [{ required: true, message: '请选择状态', trigger: 'blur' }]
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.category = ''
      searchForm.status = ''
    }
    
    // 处理添加菜品
    const handleAddDish = () => {
      dialogTitle.value = '添加菜品'
      // 重置表单
      Object.assign(formData, {
        name: '',
        category: '',
        description: '',
        ingredients: '',
        restrictions: '',
        suitable_for: '',
        not_suitable_for: '',
        service_taboo: '',
        lactation_risk: '0',
        post_partum_suitability: '',
        price: 0,
        status: 'active'
      })
      dialogVisible.value = true
    }
    
    // 处理编辑菜品
    const handleEditDish = (dish) => {
      dialogTitle.value = '编辑菜品'
      // 填充表单数据
      Object.assign(formData, { ...dish })
      dialogVisible.value = true
    }
    
    // 处理提交
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        
        // 禁忌预警
        if (formData.lactation_risk === '3') {
          ElMessage.warning('警告：该菜品回奶风险高，哺乳期妇女应避免食用！')
        } else if (formData.lactation_risk === '2') {
          ElMessage.warning('警告：该菜品回奶风险中等，哺乳期妇女应谨慎食用！')
        } else if (formData.lactation_risk === '1') {
          ElMessage.info('提示：该菜品有轻微回奶风险，哺乳期妇女应适量食用！')
        }
        
        if (formData.restrictions) {
          ElMessage.warning(`警告：该菜品有禁忌：${formData.restrictions}`)
        }
        
        console.log('表单数据', formData)
        // 这里可以添加实际的提交逻辑
        dialogVisible.value = false
        // 刷新数据
        // fetchDishes()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理删除菜品
    const handleDeleteDish = (id) => {
      if (confirm('确定要删除该菜品吗？')) {
        console.log('删除菜品', id)
        // 这里可以添加实际的删除逻辑
        // fetchDishes()
      }
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入菜品')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出菜品')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      // 刷新数据
      // fetchDishes()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchDishes()
    }
    
    // 获取菜品数据
    const fetchDishes = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/dishes')
        // dishes.value = response.data
      } catch (error) {
        console.log('获取菜品数据失败', error)
      }
    }
    
    // 生命周期
    onMounted(() => {
      // 获取数据
      // fetchDishes()
    })
    
    return {
      searchForm,
      dishes,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      formData,
      formRef,
      formRules,
      handleSearch,
      resetSearch,
      handleAddDish,
      handleEditDish,
      handleSubmit,
      handleDeleteDish,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.dish-management {
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
