import { useEffect, useRef, useState } from 'react'
import { Button, Card, Input, Typography } from 'antd'
import axios from 'axios'

export default function Chat() {
  const [text, setText] = useState('Построй ETL, который очистит CSV...')
  const [intent, setIntent] = useState<any>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const [wsStatus, setWsStatus] = useState<'connecting'|'open'|'closed'>('connecting')
  const reconnectTimer = useRef<number | null>(null)

  const connect = () => {
    try {
      setWsStatus('connecting')
      const url = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host.replace('5173','8000') + '/ws'
      const ws = new WebSocket(url)
      wsRef.current = ws
      ws.onopen = () => setWsStatus('open')
      ws.onclose = () => {
        setWsStatus('closed')
        // авто‑reconnect через 2с
        if (reconnectTimer.current == null) {
          reconnectTimer.current = window.setTimeout(() => {
            reconnectTimer.current = null
            connect()
          }, 2000)
        }
      }
      ws.onerror = () => {
        try { ws.close() } catch {}
      }
      ws.onmessage = ev => console.log('WS:', ev.data)
    } catch (e) {
      setWsStatus('closed')
    }
  }

  useEffect(() => {
    connect()
    return () => {
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current)
        reconnectTimer.current = null
      }
      try { wsRef.current?.close() } catch {}
    }
  }, [])

  const send = () => {
    const ws = wsRef.current
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(text)
    } else {
      console.warn('WS not open, reconnecting...')
      connect()
    }
  }
  const parse = async () => {
    const { data } = await axios.post('/api/intent/parse', { text })
    setIntent(data)
  }

  return (
    <Card title="Chat & Intent">
      <Typography.Text type={wsStatus === 'open' ? 'success' : wsStatus === 'connecting' ? 'secondary' : 'danger'}>
        WS: {wsStatus}
      </Typography.Text>
      <Input.TextArea rows={4} value={text} onChange={e => setText(e.target.value)} />
      <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
        <Button onClick={send}>Send WS</Button>
        <Button type="primary" onClick={parse}>Parse Intent</Button>
      </div>
      <pre style={{ marginTop: 12 }}>{intent ? JSON.stringify(intent, null, 2) : 'No intent yet.'}</pre>
    </Card>
  )
}


