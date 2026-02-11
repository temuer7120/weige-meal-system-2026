<template>
  <div class="menu-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>菜单管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddMenu">
          <el-icon><Plus /></el-icon>
          添加菜单
        </el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="菜单名称">
          <el-input v-model="searchForm.name" placeholder="请输入菜单名称" style="width: 200px"></el-input>
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
    
    <!-- 菜单列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>菜单列表</span>
          <span class="total-count">共 {{ menus.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="menus" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="菜单名称"></el-table-column>
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
        <el-table-column prop="restrictions" label="禁忌" width="150"></el-table-column>
        <el-table-column prop="suitable_for" label="适用人群" width="150"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditMenu(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDeleteMenu(scope.row.id)">删除</el-button>
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
    
    <!-- 添加/编辑菜单对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入菜单名称"></el-input>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入菜单描述"></el-input>
        </el-form-item>
        
        <el-form-item label="菜品组成" prop="dishes">
          <el-select
            v-model="formData.dishes"
            multiple
            placeholder="请选择菜品"
            style="width: 100%"
          >
            <el-option v-for="dish in dishes" :key="dish.id" :label="dish.name" :value="dish.id"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="formData.price" placeholder="请输入价格" type="number"></el-input>
        </el-form-item>
        
        <el-form-item label="禁忌" prop="restrictions">
          <el-input v-model="formData.restrictions" type="textarea" placeholder="请输入禁忌"></el-input>
        </el-form-item>
        
        <el-form-item label="适用人群" prop="suitable_for">
          <el-input v-model="formData.suitable_for" type="textarea" placeholder="请输入适用人群"></el-input>
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
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'MenuManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      status: ''
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 菜品列表
    const dishes = ref([
      { id: 1, name: '宫保鸡丁' },
      { id: 2, name: '麻婆豆腐' },
      { id: 3, name: '米饭' },
      { id: 4, name: '可乐' },
      { id: 5, name: '海鲜炒饭' }
    ])
    
    // 菜单数据
    const menus = ref([
      { id: 1, name: '营养早餐套餐', price: 88, status: 'active', restrictions: '无', suitable_for: '所有人群' },
      { id: 2, name: '健康午餐套餐', price: 128, status: 'active', restrictions: '无', suitable_for: '所有人群' },
      { id: 3, name: '海鲜晚餐套餐', price: 198, status: 'active', restrictions: '海鲜', suitable_for: '无海鲜过敏' }
    ])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加菜单')
    const formData = reactive({})
    const formRef = ref(null)
    
    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
      price: [{ required: true, message: '请输入价格', trigger: 'blur', type: 'number' }],
      status: [{ required: true, message: '请选择状态', trigger: 'blur' }],
      restrictions: [{ required: true, message: '请输入禁忌', trigger: 'blur' }],
      suitable_for: [{ required: true, message: '请输入适用人群', trigger: 'blur' }]
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.status = ''
    }
    
    // 处理添加菜单
    const handleAddMenu = () => {
      dialogTitle.value = '添加菜单'
      // 重置表单
      Object.assign(formData, {
        name: '',
        description: '',
        dishes: [],
        price: 0,
        restrictions: '',
        suitable_for: '',
        status: 'active'
      })
      dialogVisible.value = true
    }
    
    // 处理编辑菜单
    const handleEditMenu = (menu) => {
      dialogTitle.value = '编辑菜单'
      // 填充表单数据
      Object.assign(formData, { ...menu })
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
        // fetchMenus()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理删除菜单
    const handleDeleteMenu = (id) => {
      ElMessageBox.confirm('确定要删除该菜单吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除菜单', id)
        // 这里可以添加实际的删除逻辑
        // fetchMenus()
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入菜单')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出菜单')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      // 刷新数据
      // fetchMenus()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchMenus()
    }
    
    // 获取菜单数据
    const fetchMenus = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/menus')
        // menus.value = response.data
      } catch (error) {
        console.log('获取菜单数据失败', error)
      }
    }
    
    // 生命周期
    onMounted(() => {
      // 获取数据
      // fetchMenus()
    })
    
    return {
      searchForm,
      menus,
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
      handleAddMenu,
      handleEditMenu,
      handleSubmit,
      handleDeleteMenu,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.menu-management {
  padding: 20px;
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
