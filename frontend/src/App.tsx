import { Layout, Tabs, Typography } from 'antd'
import UploadProfiler from './components/UploadProfiler'
import Chat from './components/Chat'
import PipelinePreview from './components/PipelinePreview'
import Monitoring from './components/Monitoring'
import Recommendations from './components/Recommendations'
import Designer from './components/Designer'
import Assistant from './components/Assistant'

const { Header, Content } = Layout

export default function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ color: 'white', fontWeight: 600 }}>DataEngineer AI</Header>
      <Content style={{ padding: 24 }}>
        <Tabs
          items={[
            { key: 'upload', label: 'Upload & Profile', children: <UploadProfiler /> },
            { key: 'chat', label: 'Chat & Intent', children: <Chat /> },
            { key: 'pipeline', label: 'Pipeline Preview', children: <PipelinePreview /> },
            { key: 'monitoring', label: 'Monitoring', children: <Monitoring /> },
            { key: 'reco', label: 'Recommendations', children: <Recommendations /> },
            { key: 'designer', label: 'Designer', children: <Designer /> },
            { key: 'assistant', label: 'AI Assistant', children: <Assistant /> },
          ]}
        />
        <Typography.Paragraph type="secondary">
          MVP: profiling, intent stub, pipeline plan/run, WebSocket echo.
        </Typography.Paragraph>
      </Content>
    </Layout>
  )
}


