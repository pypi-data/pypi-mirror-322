from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any
import yaml
import os
from fastapi import Request
import logging
import subprocess
import json

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

_LOGGER = logging.getLogger(__name__)

app = FastAPI()

# Templates 설정
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


class Dashboard(BaseModel):
    name: str
    template_id: str
    labels: List[str]
    template_type: str
    dashboards: List[Dict[str, Any]]


class RunSubprocessRequest(BaseModel):
    environment: str
    dashboard: Dashboard


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/dashboard-generator")
async def create_dashboard(dashboard: Dashboard):
    # YAML 파일로 변환
    dashboard_data = dashboard.dict()
    yaml_data = yaml.dump(dashboard_data, default_flow_style=False, allow_unicode=True)

    # 파일 경로 설정
    file_path = os.path.expanduser(f"~/.spaceone/dashboard/{dashboard.template_id}.yml")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # YAML 파일 저장
    with open(file_path, 'w') as file:
        file.write(yaml_data)

    return {"message": "Dashboard created successfully", "file_path": file_path}

@app.post("/call-dashboard-api")
async def call_dashboard_api(dashboard: Dashboard):
    return {"message": "Dashboard API called successfully"}

@app.get("/dashboard-generator")
async def read_dashboard():
    return {"message": "Dashboard data will be here"}

@app.get("/environment-files")
async def list_environment_files():
    # 환경 파일 경로 설정
    env_dir = os.path.expanduser("~/.spaceone/environments")
    _LOGGER.info(f"Environment directory: {env_dir}")
    
    # 디렉토리 존재 여부 확인 및 생성
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        _LOGGER.info(f"Created environment directory: {env_dir}")

    # .yml 확장자 파일 목록 가져오기
    try:
        files = [f[:-4] for f in os.listdir(env_dir) if f.endswith('.yml') or f.endswith('.yaml')]
        _LOGGER.info(f"Environment files: {files}")
    except FileNotFoundError:
        return {"error": "Environment directory not found"}
    
    return {"files": files}

@app.post("/run-create-template-by-subprocess")
async def run_create_template_by_subprocess(request: RunSubprocessRequest):
    try:
        _LOGGER.info(f"Running subprocess with environment: {request.environment}, dashboard: {request.dashboard}")
        
        # subprocess 실행
        result = subprocess.run(
            ['spacectl', 'config', 'environment', '-s', request.environment],
            capture_output=True,
            text=True
        )
        _LOGGER.info(f"Subprocess output: {result.stdout}")
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
        
        result = subprocess.run(
            ['spacectl', 'exec', 'register', 'repository.DashboardTemplate', '-j', request.dashboard.model_dump_json()],
            capture_output=True,
            text=True
        )
        _LOGGER.info(f"Subprocess output: {result.stdout}")
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
        
        return {"message": "Subprocess executed successfully", "output": result.stdout}
    except Exception as e:
        _LOGGER.error(f"Error executing subprocess: {str(e)}")
        return {"error": "Failed to execute subprocess"}

@app.get("/list-dashboard-templates-by-subprocess")
async def list_dashboard_templates_by_subprocess():
    try:
        _LOGGER.info("Listing dashboard templates using subprocess")
        
        # subprocess 실행
        result = subprocess.run(
            ['spacectl', 'list', 'repository.DashboardTemplate', '--minimal', '-o', 'json'],
            capture_output=True,
            text=True
        )
        
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
            return {"error": "Failed to list dashboard templates", "details": result.stderr}
        
        if not result.stdout.strip():
            _LOGGER.error("Subprocess returned empty output")
            return {"error": "No output from subprocess"}
        
        try:
            result = result.stdout.split(">")
            result = result[-1]
            _LOGGER.info(f"Subprocess output: {result}")
            json_result = json.loads(result)
            _LOGGER.info(f"Subprocess output: {json_result}")
            return {"templates": json_result}
        except json.JSONDecodeError as e:
            _LOGGER.error(f"JSON decode error: {str(e)}")
            return {"error": "Failed to decode JSON", "details": str(e)}
    except Exception as e:
        _LOGGER.error(f"Error listing dashboard templates: {str(e)}")
        return {"error": "Failed to list dashboard templates"}

@app.get("/delete-dashboard-template")
async def delete_dashboard_template(template_id: str):
    try:
        result = subprocess.run(['spacectl', 'exec', 'deregister', 'repository.DashboardTemplate','-p', f'template_id={template_id}'], capture_output=True, text=True)
        return {"message": "Dashboard template deleted successfully", "output": result.stdout}
    except Exception as e:
        _LOGGER.error(f"Error deleting dashboard template: {str(e)}")
        return {"error": "Failed to delete dashboard template"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
