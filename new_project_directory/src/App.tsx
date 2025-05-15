import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { getCurrent } from "@tauri-apps/api/window"; // 使用 getCurrent 替代 


import "./App.css";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [interval, setInterval] = useState(1000);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    // 获取初始状态
    async function fetchInitialState() {
      try {
        // 使用 getCurrent 检查 Tauri 环境是否就绪
        const currentWindow = getCurrent();
        if (currentWindow) {
          const status = await invoke<boolean>("get_status");
          const savedInterval = await invoke<number>("get_interval");

          setIsRunning(status);
          setInterval(savedInterval);
          setError(null);
        } else {
          setError("Tauri 环境未就绪");
        }
      } catch (error) {
        console.error("获取初始状态失败:", error);
        setError("获取初始状态失败");
      } finally {
        setLoading(false);
      }
    }

    fetchInitialState();
  }, []);

  async function toggleAutoPress() {
    try {
      if (!isRunning) {
        console.log("调用 start_auto_press，参数:", { intervalMs: interval });
        await invoke("start_auto_press", { 
          intervalMs: interval
        });
      } else {
        console.log("调用 stop_auto_press");
        await invoke("stop_auto_press");
      }
      
      setIsRunning(!isRunning);
      setError(null);
    } catch (error) {
      console.error("操作失败:", error);
      setError("操作失败，请重试");
    }
  }
  
  

  return (
    <main className="auto-space-container">
      <h1>自动空格按键工具</h1>
      <p className="description">
        此工具可以在Windows系统中自动按下空格键。
        可以设置间隔时间，并且可以随时开启或关闭。
      </p>

      {loading ? (
        <div className="loading">加载中...</div>
      ) : (
        <>
          {error && <div className="error-message">{error}</div>}
          
          <div className="control-group">
            <label htmlFor="interval-input">按键间隔 (毫秒):</label>
            <input
              id="interval-input"
              type="number"
              min="50"
              value={interval}
              onChange={(e) => setInterval(parseInt(e.target.value, 10))}
              disabled={isRunning}
            />
          </div>

          <button 
            className={`toggle-button ${isRunning ? 'running' : ''}`}
            onClick={toggleAutoPress}
          >
            {isRunning ? '停止' : '开始'}
          </button>

          <div className="status-indicator">
            状态: <span className={isRunning ? 'running' : 'stopped'}>
              {isRunning ? '运行中' : '已停止'}
            </span>
          </div>

          <footer className="footer">
            <p>
              提示: 应用程序最小化后仍会继续运行
            </p>
          </footer>
        </>
      )}
    </main>
  );
}

export default App;
