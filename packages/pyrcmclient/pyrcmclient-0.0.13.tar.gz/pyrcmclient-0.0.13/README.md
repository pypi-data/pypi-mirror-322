# pyrcmclient

`pyrcmclient`は、I4S `RCM-Controller`のPythonクライアントです。Pythonから`DBリクエスト`や`RCMワークフロー`の実行などを簡単に行うことができます。

## 概要

Pythonを使用してRCM-Controllerの以下の機能をコールすることができます。

- **ログイン**: RCMアカウントにログインします
- **DBRequest**: データベースへのリクエストを送信し、データを操作することができます。
- **ファイル登録**: ファイルをRCMにアップロードします。
- **ファイル取得**: RCMからファイルをダウンロードします
- **RCM WorkFlow実行**: ワークフローの実行を簡潔なコードで行うことができます。
- **systemConfig**: RCM-Controllerの情報取得と設定変更

## インストール方法

以下のコマンドで`pyrcmclient`をインストールすることができます：

```sh
pip install pyrcmclient
```

## 使用方法

### DBRequestの例

以下に、データベースリクエストの簡単な使用例を示します：

```python
from i4srcm.client import RCMCNT_Client

client:RCMCNT_Client = RCMCNT_Client( "https://rcmfront", username="userName", passwd="passwd" )
if not client.login():
    print("failled to login")
    return
response = client.SEL2("/project[@tagid=1234]/template[name='abc']")
print(response)
```

### ワークフロー実行の例

RCM WorkFlowを実行するための例です：

```python
from i4srcm.client import RCMCNT_Client

client:RCMCNT_Client = RCMCNT_Client( "https://rcmfront", username="userName", passwd="passwd" )
if not client.login():
    print("failled to login")
    return

workflow_id = client.execute_template( "template name" )
workflow_result = client.get_workflow(workflow_id,wait=60)
print(workflow_result)
```

## 必要要件

- Python 3.11以上
- RCM-1024以降のバージョンのRCM-Controller

## ライセンス

このプロジェクトは[MITライセンス](LICENSE.txt)のもとで公開されています。

本モジュールの利用・運用の結果と起因する損害などについて開発元は一切の責任を負いません。

本モジュールについてのサポートは行いませんが、ご質問やご提案をいただければ開発の参考にさせて頂きます。

