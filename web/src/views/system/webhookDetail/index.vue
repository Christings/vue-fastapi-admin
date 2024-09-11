<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import { router } from '@/router'
import api from '@/api'

defineOptions({ name: 'WebhookDetail' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

queryItems.value = { webhook_id: router.currentRoute.value.query.id }

onMounted(() => {
  $table.value?.handleSearch()
})

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
    title: '测试结果',
    key: 'ret',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
]
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="Webhook Result列表">
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getWebhookTests"
    >
    </CrudTable>
  </CommonPage>
</template>
