import { useState } from 'react'
import { Button, Card, Input, List, Typography } from 'antd'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export default function Assistant() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!message.trim()) return
    
    const userMessage: Message = {
      role: 'user',
      content: message,
      timestamp: new Date().toLocaleTimeString()
    }
    
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    
    try {
      const { data } = await axios.post('/api/chat/assistant', { message })
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Извините, произошла ошибка при обработке запроса.',
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
      setMessage('')
    }
  }

  return (
    <Card title="AI Ассистент по Data Engineering">
      <div style={{ height: 400, overflowY: 'auto', marginBottom: 16, border: '1px solid #d9d9d9', padding: 12 }}>
        <List
          dataSource={messages}
          renderItem={(msg) => (
            <List.Item style={{ border: 'none', padding: '8px 0' }}>
              <div style={{ width: '100%' }}>
                <Typography.Text strong style={{ color: msg.role === 'user' ? '#1890ff' : '#52c41a' }}>
                  {msg.role === 'user' ? 'Вы' : 'Ассистент'} ({msg.timestamp}):
                </Typography.Text>
                <div style={{ marginTop: 4, whiteSpace: 'pre-wrap' }}>{msg.content}</div>
              </div>
            </List.Item>
          )}
        />
      </div>
      
      <div style={{ display: 'flex', gap: 8 }}>
        <Input.TextArea
          rows={2}
          value={message}
          onChange={e => setMessage(e.target.value)}
          onPressEnter={sendMessage}
          placeholder="Задайте вопрос о data engineering, ETL, анализе данных..."
          disabled={loading}
        />
        <Button 
          type="primary" 
          onClick={sendMessage}
          loading={loading}
          disabled={!message.trim()}
        >
          Отправить
        </Button>
      </div>
    </Card>
  )
}
