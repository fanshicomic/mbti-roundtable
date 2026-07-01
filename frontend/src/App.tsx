import { Stage } from './components/Stage/Stage'
import { LogViewer } from './components/LogViewer/LogViewer'
import { Config } from './components/Config/Config'
import { UserSeat } from './components/UserSeat/UserSeat'

function App() {
  return (
    <div className="flex h-screen flex-col bg-black">
      <Config />
      <div className="flex flex-1 overflow-hidden">
        <div className="flex w-[70%] flex-col">
          <div className="flex-1 overflow-hidden">
            <Stage />
          </div>
          <UserSeat />
        </div>
        <div className="w-[30%] border-l border-neutral-800">
          <LogViewer />
        </div>
      </div>
    </div>
  )
}

export default App
