# KEY TO LIT 個人用スケジュール（試作）

## できること
- `index.html`: 手動で出演・販売情報を登録。週間予定、検索、ICS書き出し、SNS投稿URLの手動登録
- `collect.py`: ジュニア公式トップページに掲載されている公開告知からKEY TO LIT関連を抽出
- `schedule.json`: アプリの「今すぐ同期」から読み込める公開JSON
- GitHub Actions: 約6時間おきに収集（実行時刻は保証されません）

**重要：収集プログラムは告知の掲載日を「確認メモ」として記録し、出演日時・発売開始日時とは扱いません。** 公開HTMLから掲載日時を正確に取得できない予定は自動登録されません。サイトの構造変更で収集できなくなることもあります。InstagramとXの自動取得は未実装です。登録・変更・削除はすべて公式リンクで確認してください。

## GitHubで使う手順（PC）
1. GitHubアカウントを作る。
2. 新しい**Public**リポジトリ `kitelit-auto` を作り、このフォルダ内のファイルと `.github/workflows/update.yml` をアップロード。ZIPをそのままアップロードしない。
3. リポジトリの **Settings → Pages** で `Deploy from a branch` → `main` → `/ (root)` を選び Save。
4. **Actions → Update official announcements → Run workflow** で最初の収集を手動実行。
5. GitHub Pages のURL `https://ユーザー名.github.io/kitelit-auto/` でHTMLを開く。
6. HTMLの「公開JSONのURL」に `https://ユーザー名.github.io/kitelit-auto/schedule.json` と入力し「URL保存」→「今すぐ同期」。
7. iPhoneのSafariでHTMLを開き、共有→ホーム画面に追加。

公開リポジトリと公開Pagesでは登録したソースコード・JSONは全員から閲覧可能。手動登録したデータは基本的に各ブラウザのローカルストレージのみで、iPhoneとPC間で自動共有されない。

## ロック画面の注意
「カレンダー出力」は一度きりのICSファイルです。自動購読カレンダーでも、ネイティブiPhoneウィジェットでもありません。ロック画面で自動更新するには別途、購読可能なICSフィードの公開とiPhoneのカレンダー連携が必要です。iPhoneの純正ロック画面ウィジェットはAppleの表示仕様に従います。

## サイトの利用規約
公式サイトの閲覧条件、robots.txt、API利用規約を確認のうえ、過度に頻繁なアクセスは避けてください。SNS自動収集は正規のAPI・許諾が必要な場合があります。
