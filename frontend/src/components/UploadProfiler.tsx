import { useState } from 'react'
import { Button, Card, Upload } from 'antd'
import type { UploadFile } from 'antd/es/upload/interface'
import axios from 'axios'

export default function UploadProfiler() {
  const [files, setFiles] = useState<UploadFile[]>([])
  const [result, setResult] = useState<any>(null)

  const handleUpload = async () => {
    const form = new FormData()
    files.forEach(f => {
      if (f.originFileObj) form.append('files', f.originFileObj)
    })
    const { data } = await axios.post('/api/upload/profile', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    setResult(data)
  }

  return (
    <Card title="Upload CSV/JSON and Profile">
      <Upload multiple beforeUpload={() => false} onChange={({ fileList }) => setFiles(fileList)}>
        <Button>Select Files</Button>
      </Upload>
      <Button type="primary" onClick={handleUpload} style={{ marginTop: 12 }}>Profile</Button>
      <pre style={{ marginTop: 16, maxHeight: 300, overflow: 'auto' }}>{
        result ? JSON.stringify(result, null, 2) : 'No results yet.'
      }</pre>
    </Card>
  )
}


