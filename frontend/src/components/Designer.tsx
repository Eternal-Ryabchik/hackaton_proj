import { useState } from 'react'
import { Button, Card, Form, Input, Select } from 'antd'
import axios from 'axios'

export default function Designer() {
  const [intent, setIntent] = useState('Построй ETL: csv + json по user_id, средний чек')
  const [plan, setPlan] = useState<any>(null)

  const planPipeline = async () => {
    const { data } = await axios.post('/api/pipeline/plan', { intent_text: intent })
    setPlan(data)
  }

  return (
    <Card title="Pipeline Designer">
      <Form layout="vertical">
        <Form.Item label="Намерение">
          <Input.TextArea rows={3} value={intent} onChange={e => setIntent(e.target.value)} />
        </Form.Item>
        <Button onClick={planPipeline}>Сгенерировать план</Button>
      </Form>
      <pre style={{ marginTop: 12 }}>{plan ? JSON.stringify(plan, null, 2) : 'Нет плана'}</pre>
    </Card>
  )
}


