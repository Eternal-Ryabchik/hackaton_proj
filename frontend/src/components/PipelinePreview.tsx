import { useMemo, useState } from 'react'
import { Button, Card } from 'antd'
import axios from 'axios'
import * as echarts from 'echarts'
import { useEffect, useRef } from 'react'

export default function PipelinePreview() {
  const [plan, setPlan] = useState<any>(null)
  const [run, setRun] = useState<any>(null)
  const chartRef = useRef<HTMLDivElement | null>(null)
  const chart = useRef<echarts.EChartsType | null>(null)

  const planPipeline = async () => {
    const { data } = await axios.post('/api/pipeline/plan', { intent_text: 'etl по user_id' })
    setPlan(data)
  }

  const runPipeline = async () => {
    const { data } = await axios.post('/api/pipeline/run', { intent_text: 'etl по user_id' })
    setRun(data)
  }

  const graphOption = useMemo(() => {
    const steps = plan?.steps || []
    const nodes = steps.map((s: any, i: number) => ({ id: String(i), name: s.op }))
    const edges = steps.slice(1).map((_: any, i: number) => ({ source: String(i), target: String(i + 1) }))
    return {
      tooltip: {},
      series: [{
        type: 'graph',
        layout: 'force',
        roam: true,
        data: nodes,
        edges: edges,
        label: { show: true }
      }]
    }
  }, [plan])

  useEffect(() => {
    if (!chartRef.current) return
    chart.current = echarts.init(chartRef.current)
    const c = chart.current
    const observer = new ResizeObserver(() => c.resize())
    observer.observe(chartRef.current)
    return () => { observer.disconnect(); c.dispose() }
  }, [])

  useEffect(() => {
    if (chart.current && plan) chart.current.setOption(graphOption as any)
  }, [graphOption, plan])

  return (
    <Card title="Pipeline Plan & Run">
      <div style={{ display: 'flex', gap: 8 }}>
        <Button onClick={planPipeline}>Plan</Button>
        <Button type="primary" onClick={runPipeline}>Run</Button>
      </div>
      <div ref={chartRef} style={{ height: 300, marginTop: 12, background: '#fff' }} />
      <pre style={{ marginTop: 12 }}>{plan ? JSON.stringify(plan, null, 2) : 'No plan yet.'}</pre>
      <pre style={{ marginTop: 12 }}>{run ? JSON.stringify(run, null, 2) : 'No run yet.'}</pre>
    </Card>
  )
}


