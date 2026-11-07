import json
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).parent
package = root/'installer-test/中文补丁 [测试]'
package.mkdir(parents=True,exist_ok=True)
for name in ['Install.cmd','Uninstall.cmd','Install-Chinese.ps1','Find-HereSphere.ps1','native-patch.json','build-report.json']:
    shutil.copyfile(root/'release'/name,package/name)
target = root/'installer-test/目录识别 [测试]/另一个磁盘的游戏库/steamapps/common/HereSphere 自定义名称'
for name in ['Install.cmd','Uninstall.cmd']:
    command = f'cmd.exe /d /s /c ""{package/name}" -GameDir "{target}""'
    result = subprocess.run(command,input=b'\r\n',capture_output=True,timeout=30)
    text = (result.stdout+result.stderr).decode('utf-8')
    assert str(target) in text, repr(text)
    assert '游戏目录：' in text and '????' not in text,repr(text)
    # The dummy installation must be refused, and CMD must retain the error code.
    assert result.returncode != 0,(name,result.returncode,text)
    print(json.dumps({'script':name,'utf8':'passed','chinese_path':'passed','error_exit_code':result.returncode},ensure_ascii=True))
