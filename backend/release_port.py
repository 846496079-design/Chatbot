import subprocess
import os

def release_port(port):
    """释放指定端口"""
    # 查找占用端口的进程
    result = subprocess.run(['netstat', '-ano', '|', 'findstr', f':{port}'], 
                          capture_output=True, text=True, shell=True)
    
    # 使用 PowerShell 来查找和终止进程
    ps_command = f"""
    $connections = Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue
    if ($connections) {{
        foreach ($conn in $connections) {{
            try {{
                Stop-Process -Id $conn.OwningProcess -Force -ErrorAction Stop
                Write-Host "已终止进程 $($conn.OwningProcess)"
            }} catch {{
                Write-Host "终止进程失败: $_"
            }}
        }}
    }} else {{
        Write-Host "端口 {port} 未被占用"
    }}
    """
    
    subprocess.run(['powershell', '-Command', ps_command], capture_output=True, text=True)
    print(f"尝试释放端口 {port}")

if __name__ == "__main__":
    release_port(8000)