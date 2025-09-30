import { useEffect, useMemo, useState } from 'react'
import { Card, Table, Tag } from 'antd'
import axios from 'axios'
import * as echarts from 'echarts'

export default function Monitoring() {
  const [runs, setRuns] = useState<any[]>([])

  const load = async () => {
    const { data } = await axios.get('/api/runs/recent?limit=50')
    setRuns(data.runs || [])
  }

  useEffect(() => { load() }, [])

  const columns = [
    { title: 'ID', dataIndex: 'id' },
    { title: 'Pipeline', dataIndex: 'pipeline' },
    { title: 'Status', dataIndex: 'status', render: (s: string) => <Tag color={s === 'success' ? 'green' : s === 'running' ? 'blue' : 'red'}>{s}</Tag> },
    { title: 'Started', dataIndex: 'started_at' },
    { title: 'Finished', dataIndex: 'finished_at' },
  ]

  return (
    <Card title="Recent Runs">
      <Table rowKey="id" dataSource={runs} columns={columns as any} pagination={{ pageSize: 10 }} />
    </Card>
  )
}


