<template>
  <div class="taboo-rule-management">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>禁忌规则管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="handleAddRule">添加规则</el-button>
        <el-button @click="handleImport">导入</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="规则名称">
          <el-input v-model="searchForm.name" placeholder="请输入规则名称" style="width: 200px"></el-input>
        </el-form-item>
        
        <el-form-item label="规则类型">
          <el-select v-model="searchForm.ruleType" placeholder="请选择规则类型" style="width: 150px">
            <el-option label="饮食禁忌" value="饮食禁忌"></el-option>
            <el-option label="服务禁忌" value="服务禁忌"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="适用时期">
          <el-select v-model="searchForm.period" placeholder="请选择适用时期" style="width: 150px">
            <el-option label="产后1周" value="产后1周"></el-option>
            <el-option label="产后2-4周" value="产后2-4周"></el-option>
            <el-option label="哺乳期" value="哺乳期"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 规则列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="list-header">
          <span>规则列表</span>
          <span class="total-count">共 {{ rules.length }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="rules" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="rule_name" label="规则名称"></el-table-column>
        <el-table-column prop="rule_type" label="规则类型" width="120"></el-table-column>
        <el-table-column prop="severity_level" label="严重程度" width="100">
          <template #default="scope">
            <el-tag :type="getSeverityType(scope.row.severity_level)">
              {{ scope.row.severity_level }}级
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applicable_period" label="适用时期" width="150"></el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditRule(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDeleteRule(scope.row.id)">删除</el-button>
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
    
    <!-- 添加/编辑规则对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="800px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="120px">
        <el-form-item label="规则名称" prop="rule_name">
          <el-input v-model="formData.rule_name" placeholder="请输入规则名称"></el-input>
        </el-form-item>
        
        <el-form-item label="规则类型" prop="rule_type">
          <el-select v-model="formData.rule_type" placeholder="请选择规则类型">
            <el-option label="饮食禁忌" value="饮食禁忌"></el-option>
            <el-option label="服务禁忌" value="服务禁忌"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="规则描述">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入规则描述"></el-input>
        </el-form-item>
        
        <el-form-item label="严重程度" prop="severity_level">
          <el-select v-model="formData.severity_level" placeholder="请选择严重程度">
            <el-option label="1级 (低)" value="1"></el-option>
            <el-option label="2级 (中低)" value="2"></el-option>
            <el-option label="3级 (中)" value="3"></el-option>
            <el-option label="4级 (中高)" value="4"></el-option>
            <el-option label="5级 (高)" value="5"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="适用时期" prop="applicable_period">
          <el-input v-model="formData.applicable_period" placeholder="请输入适用时期，如：产后1周、哺乳期等"></el-input>
        </el-form-item>
        
        <el-form-item label="相关食材">
          <el-select v-model="formData.related_ingredients" multiple placeholder="请选择相关食材">
            <el-option v-for="ingredient in ingredients" :key="ingredient.id" :label="ingredient.name" :value="ingredient.id"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="相关菜品">
          <el-select v-model="formData.related_dishes" multiple placeholder="请选择相关菜品">
            <el-option v-for="dish in dishes" :key="dish.id" :label="dish.name" :value="dish.id"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="例外情况">
          <el-input v-model="formData.exception_conditions" type="textarea" placeholder="请输入例外情况"></el-input>
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
import api from '../services/api'

export default {
  name: 'TabooRuleManagement',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      ruleType: '',
      period: ''
    })
    
    // 分页信息
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    
    // 规则数据
    const rules = ref([
      {
        id: 1,
        rule_name: '海鲜过敏禁忌',
        rule_type: '饮食禁忌',
        description: '对海鲜过敏的客户应避免食用海鲜类食材和菜品',
        severity_level: 5,
        applicable_period: '所有时期',
        related_ingredients: '["5"]',
        related_dishes: '["5"]',
        exception_conditions: '无'
      },
      {
        id: 2,
        rule_name: '辛辣食物禁忌',
        rule_type: '饮食禁忌',
        description: '产后1周内的客户应避免食用辛辣食物',
        severity_level: 3,
        applicable_period: '产后1周',
        related_ingredients: '[]',
        related_dishes: '["1", "2"]',
        exception_conditions: '无'
      },
      {
        id: 3,
        rule_name: '回奶食物禁忌',
        rule_type: '饮食禁忌',
        description: '哺乳期的客户应避免食用回奶食物',
        severity_level: 4,
        applicable_period: '哺乳期',
        related_ingredients: '["6", "7"]',
        related_dishes: '[]',
        exception_conditions: '无'
      }
    ])
    
    // 食材列表
    const ingredients = ref([
      { id: 1, name: '西红柿' },
      { id: 2, name: '鸡蛋' },
      { id: 3, name: '猪肉' },
      { id: 4, name: '大米' },
      { id: 5, name: '胡萝卜' },
      { id: 6, name: '韭菜' },
      { id: 7, name: '大麦茶' }
    ])
    
    // 菜品列表
    const dishes = ref([
      { id: 1, name: '宫保鸡丁' },
      { id: 2, name: '麻婆豆腐' },
      { id: 3, name: '米饭' },
      { id: 4, name: '可乐' },
      { id: 5, name: '海鲜炒饭' }
    ])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加规则')
    const formData = reactive({})
    const formRef = ref(null)
    
    // 表单验证规则
    const formRules = {
      rule_name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
      rule_type: [{ required: true, message: '请选择规则类型', trigger: 'blur' }],
      severity_level: [{ required: true, message: '请选择严重程度', trigger: 'blur' }],
      applicable_period: [{ required: true, message: '请输入适用时期', trigger: 'blur' }]
    }
    
    // 获取严重程度类型
    const getSeverityType = (level) => {
      switch (level) {
        case 1: return 'info'
        case 2: return 'success'
        case 3: return 'warning'
        case 4: return 'danger'
        case 5: return 'danger'
        default: return 'info'
      }
    }
    
    // 处理搜索
    const handleSearch = () => {
      console.log('搜索条件', searchForm)
      // 这里可以添加实际的搜索逻辑
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.name = ''
      searchForm.ruleType = ''
      searchForm.period = ''
    }
    
    // 处理添加规则
    const handleAddRule = () => {
      dialogTitle.value = '添加规则'
      // 重置表单
      Object.assign(formData, {
        rule_name: '',
        rule_type: '',
        description: '',
        severity_level: '',
        applicable_period: '',
        related_ingredients: [],
        related_dishes: [],
        exception_conditions: ''
      })
      dialogVisible.value = true
    }
    
    // 处理编辑规则
    const handleEditRule = (rule) => {
      dialogTitle.value = '编辑规则'
      // 填充表单数据
      Object.assign(formData, { ...rule })
      // 解析相关食材和菜品
      if (rule.related_ingredients) {
        formData.related_ingredients = JSON.parse(rule.related_ingredients)
      } else {
        formData.related_ingredients = []
      }
      if (rule.related_dishes) {
        formData.related_dishes = JSON.parse(rule.related_dishes)
      } else {
        formData.related_dishes = []
      }
      dialogVisible.value = true
    }
    
    // 处理提交
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        // 处理相关食材和菜品
        const submitData = { ...formData }
        submitData.related_ingredients = JSON.stringify(formData.related_ingredients)
        submitData.related_dishes = JSON.stringify(formData.related_dishes)
        console.log('表单数据', submitData)
        // 这里可以添加实际的提交逻辑
        dialogVisible.value = false
        ElMessage.success('规则保存成功！')
        // 刷新数据
        // fetchRules()
      } catch (error) {
        console.log('验证失败', error)
      }
    }
    
    // 处理删除规则
    const handleDeleteRule = (id) => {
      ElMessageBox.confirm('确定要删除该规则吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除规则', id)
        // 这里可以添加实际的删除逻辑
        // fetchRules()
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 处理导入
    const handleImport = () => {
      console.log('导入规则')
      // 这里可以添加实际的导入逻辑
    }
    
    // 处理导出
    const handleExport = () => {
      console.log('导出规则')
      // 这里可以添加实际的导出逻辑
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      // 刷新数据
      // fetchRules()
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      // 刷新数据
      // fetchRules()
    }
    
    // 获取规则数据
    const fetchRules = async () => {
      try {
        // 这里可以添加实际的数据获取逻辑
        // const response = await api.get('/taboo-rules')
        // rules.value = response.data
      } catch (error) {
        console.log('获取规则数据失败', error)
      }
    }
    
    // 生命周期
    onMounted(() => {
      // 获取数据
      // fetchRules()
    })
    
    return {
      searchForm,
      rules,
      ingredients,
      dishes,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      formData,
      formRef,
      formRules,
      getSeverityType,
      handleSearch,
      resetSearch,
      handleAddRule,
      handleEditRule,
      handleSubmit,
      handleDeleteRule,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.taboo-rule-management {
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