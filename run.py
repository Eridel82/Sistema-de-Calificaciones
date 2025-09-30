# Crear archivo de configuración para VS Code
import json
import os

# Crear carpeta .vscode si no existe
os.makedirs('sistema_calificaciones/.vscode', exist_ok=True)

# Configuración de VS Code para el proyecto
vscode_settings = {
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": True,
    "files.associations": {
        "*.py": "python"
    },
    "python.linting.enabled": True,
    "python.linting.pylintEnabled": True,
    "python.formatting.provider": "black",
    "editor.formatOnSave": True,
    "python.terminal.executeInFileDir": True
}

# Tareas de VS Code
vscode_tasks = {
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Ejecutar Sistema de Calificaciones",
            "type": "shell",
            "command": "python",
            "args": ["run.py"],
            "group": {
                "kind": "build",
                "isDefault": True
            },
            "presentation": {
                "echo": True,
                "reveal": "always",
                "focus": False,
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Instalar Dependencias",
            "type": "shell",
            "command": "pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build",
            "presentation": {
                "echo": True,
                "reveal": "always",
                "focus": False,
                "panel": "new"
            }
        },
        {
            "label": "Crear Entorno Virtual",
            "type": "shell",
            "command": "python",
            "args": ["-m", "venv", "venv"],
            "group": "build",
            "presentation": {
                "echo": True,
                "reveal": "always",
                "focus": False,
                "panel": "new"
            }
        }
    ]
}

# Configuración de launch para debugging
vscode_launch = {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Sistema Calificaciones",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}

# Guardar archivos de configuración
with open('sistema_calificaciones/.vscode/settings.json', 'w', encoding='utf-8') as f:
    json.dump(vscode_settings, f, indent=4, ensure_ascii=False)

with open('sistema_calificaciones/.vscode/tasks.json', 'w', encoding='utf-8') as f:
    json.dump(vscode_tasks, f, indent=4, ensure_ascii=False)

with open('sistema_calificaciones/.vscode/launch.json', 'w', encoding='utf-8') as f:
    json.dump(vscode_launch, f, indent=4, ensure_ascii=False)

print("✅ Archivos de configuración de VS Code creados:")
print("   - .vscode/settings.json")
print("   - .vscode/tasks.json") 
print("   - .vscode/launch.json")