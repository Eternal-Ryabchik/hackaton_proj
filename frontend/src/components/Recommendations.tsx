import { useState } from 'react'
import { Button, Card, Form, Input, Select } from 'antd'
import axios from 'axios'

export default function Recommendations() {
  const [profileJson, setProfileJson] = useState('')
  const [reco, setReco] = useState<any>(null)
  const [ddl, setDdl] = useState<string>('')

  const runReco = async () => {
    const profile = JSON.parse(profileJson || '{}')
    const { data } = await axios.post('/api/reco/storage', { profile })
    setReco(data)
  }

  const genDDL = async () => {
    const columns_info = (JSON.parse(profileJson || '{}').columns_info) || {}
    const system = (reco?.system || 'postgres')
    const { data } = await axios.post('/api/ddl/generate', {
      system,
      table: system === 'ClickHouse' ? 'default.generated_table' : 'public.generated_table',
      columns_info,
    })
    setDdl(data.ddl)
  }

  return (
    <Card title="Рекомендации по хранению и DDL">
      <Form layout="vertical">
        <Form.Item label="Вставьте profile (из Upload & Profile)">
          <Input.TextArea rows={6} value={profileJson} onChange={e => setProfileJson(e.target.value)} />
        </Form.Item>
        <Button onClick={runReco} type="primary">Рассчитать рекомендации</Button>
        {reco && <pre style={{ marginTop: 12 }}>{JSON.stringify(reco, null, 2)}</pre>}
        {reco && <Button style={{ marginTop: 8 }} onClick={genDDL}>Сгенерировать DDL</Button>}
        {ddl && <pre style={{ marginTop: 12 }}>{ddl}</pre>}
      </Form>
    </Card>
  )
}


