<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NInputNumber, NPopconfirm, NTreeSelect } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'

defineOptions({ name: 'Webhook管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: 'API',
  initForm: {},
  doCreate: api.createWebhook,
  doUpdate: api.updateWebhook,
  doDelete: api.deleteWebhook,
  refresh: () => $table.value?.handleSearch(),
})

const webhookOption = ref([])
const isDisabled = ref(false)

onMounted(() => {
  $table.value?.handleSearch()
  api.getWebhooks().then((res) => (webhookOption.value = res.data))
})

const webhookRules = {
  project: [
    {
      required: true,
      message: '请输入项目名称',
      trigger: ['input', 'blur', 'change'],
    },
  ],
}

async function addWebhooks() {
  isDisabled.value = false
  handleAdd()
}

const columns = [
  {
    title: '项目名称',
    key: 'project',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'webhook名称',
    key: 'name',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'webhook地址',
    key: 'webhook',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                console.log('row', row.id)
                handleEdit(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/webhook/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ webhook_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/webhook/delete']]
              ),
            default: () => h('div', {}, '确定删除该webhook吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="Webhook列表">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/webhook/create'"
          class="float-right mr-15"
          type="primary"
          @click="addWebhooks"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建Webhook
        </NButton>
      </div>
    </template>
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getWebhooks"
    >
      <template #queryBar>
        <QueryBarItem label="项目名称" :label-width="80">
          <NInput
            v-model:value="queryItems.project"
            clearable
            type="text"
            placeholder="请输入项目名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="webhookRules"
      >
        <NFormItem label="项目名称" path="project">
          <NInput v-model:value="modalForm.project" clearable placeholder="请输入项目名称" />
        </NFormItem>
        <NFormItem label="webhook名称" path="name">
          <NInput v-model:value="modalForm.name" clearable placeholder="请输入webhook名称" />
        </NFormItem>
        <NFormItem label="Webhook" path="webhook">
          <NInput v-model:value="modalForm.webhook" type="textarea" clearable />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
