// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use std::thread;
use std::time::Duration;
use once_cell::sync::Lazy;
use tauri::AppHandle;
use enigo::KeyboardControllable;

static AUTO_PRESSING: AtomicBool = AtomicBool::new(false);
static INTERVAL_MS: Lazy<Mutex<u64>> = Lazy::new(|| Mutex::new(1000));

#[tauri::command]
async fn start_auto_press(interval_ms: u64, _app_handle: AppHandle) -> Result<(), String>{
    // 更新间隔时间
    if let Ok(mut current_interval) = INTERVAL_MS.lock() {
        *current_interval = interval_ms;
    }
    
    if AUTO_PRESSING.load(Ordering::SeqCst) {
        return Ok(());
    }
    
    AUTO_PRESSING.store(true, Ordering::SeqCst);
    
    // 使用标准线程库创建线程，避免tokio的Send要求
    thread::spawn(move || {
        let mut enigo = enigo::Enigo::new();
        
        while AUTO_PRESSING.load(Ordering::SeqCst) {
            // 获取当前间隔时间
            let current_interval = match INTERVAL_MS.lock() {
                Ok(interval) => *interval,
                Err(_) => 1000, // 默认值
            };
            
            // 按下空格键
            enigo.key_click(enigo::Key::Space);
            
            // 休眠指定时间
            thread::sleep(Duration::from_millis(current_interval));
        }
    });
    
    Ok(())
}

#[tauri::command]
async fn stop_auto_press(_app_handle: AppHandle) -> Result<(), String> {
    AUTO_PRESSING.store(false, Ordering::SeqCst);
    Ok(())
}

#[tauri::command]
async fn get_status() -> bool {
    AUTO_PRESSING.load(Ordering::SeqCst)
}

#[tauri::command]
async fn get_interval() -> u64 {
    match INTERVAL_MS.lock() {
        Ok(interval) => *interval,
        Err(_) => 1000, // 默认值
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            start_auto_press,
            stop_auto_press,
            get_status,
            get_interval
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
